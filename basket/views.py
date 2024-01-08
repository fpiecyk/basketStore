from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView, CreateView
from authManager.models import CustomUser
from basket.forms import ShippingAddressForm
from basket.models import Products, Category, Order, OrderItem, WishList


class ItemsListView(ListView):
    model = Products
    template_name = 'basket/shop.html'
    context_object_name = 'products'
    paginate_by = 9

    def get_queryset(self):
        queryset = Products.get_all_products()

        # Filter by category
        category_id = self.request.GET.get("category")
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # Filter by price range
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.get_all_categories()
        context['prod_amount'] = self.get_queryset().count()

        selected_categories = self.request.GET.getlist('category')
        context['selected_categories'] = selected_categories

        return context


class ProductDetailView(DetailView):
    model = Products
    template_name = 'basket/product_detail.html'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        product_id = self.kwargs['pk']
        return get_object_or_404(Products, id=product_id)


class CartUpdateView(LoginRequiredMixin, View):
    login_url = 'authManager/login_user/'

    def post(self, request):
        product_id = request.POST.get('product')
        action = request.POST.get('action')

        if product_id and action:
            try:
                product = Products.objects.get(id=product_id)

                if action == 'add':
                    cart = request.session.get('cart', {})
                    cart[product_id] = cart.get(product_id, 0) + 1
                    cart.pop('null', None)
                    request.session['cart'] = cart
                    messages.success(request, f"{product.name} added to your cart.")
                    print(cart)
                    print(product.name)

                elif action == 'remove':
                    cart = request.session.get('cart', {})
                    if cart.get(product_id, 0) > 0:
                        cart[product_id] -= 1
                        if cart[product_id] == 0:
                            del cart[product_id]
                        request.session['cart'] = cart
                        messages.success(request, f"{product.name} removed from your cart.")
                    else:
                        messages.warning(request, f"{product.name} is not in your cart.")

                elif action == 'clear':
                    cart = request.session.get('cart', {})
                    if cart.get(product_id, 0) > 0:
                        del cart[product_id]
                        request.session['cart'] = cart
                        messages.success(request, f"{product.name} removed from your cart.")
                    else:
                        messages.warning(request, f"{product.name} is not in your cart.")
                    print(cart)
            except Products.DoesNotExist:
                messages.warning(request, "Product not found.")

        return redirect('cart_display')


class CartDisplayView(LoginRequiredMixin, View):
    login_url = '/authManager/login/'

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')

        cart = request.session.get('cart')
        if cart:
            product_ids = list(request.session.get('cart').keys())
            products = Products.objects.filter(id__in=product_ids)

            user = CustomUser.objects.get(username=request.user)
            default_address = user.address

            form = ShippingAddressForm(initial={'address': default_address})
            context = {"products": products, 'cart': cart, "form": form}
            return render(request, 'basket/cart.html', context)
        return render(request, "basket/cart.html")


class AddToCartView(LoginRequiredMixin, View):
    login_url = '/authManager/login/'

    def post(self, request):
        product = request.POST.get('product')
        cart = request.session.get('cart')

        if cart:
            quantity = cart.get(product)
            if quantity:
                cart[product] = quantity + 1

            else:
                cart[product] = 1
        else:
            cart = {product: 1}

        request.session['cart'] = cart

        return redirect('shop')


class OrderCreateView(View):
    template_name = 'basket/order_confirmation.html'

    def get(self, request):
        cart = request.session.get("cart")
        product_ids = list(cart.keys())
        products = Products.objects.filter(id__in=product_ids)

        user = CustomUser.objects.get(username=request.user)
        default_address = user.address
        print(default_address)

        form = ShippingAddressForm(initial={'address': default_address})

        context = {"products": products, "form": form}
        return render(request, self.template_name, context)

    def post(self, request):
        cart = request.session.get('cart')
        product_ids = list(cart.keys())
        products = Products.objects.filter(id__in=product_ids)

        username = request.user
        user = CustomUser.objects.get(username=username)

        form = ShippingAddressForm(request.POST)

        if form.is_valid():
            new_order = Order.objects.create(customer=user, address=form.cleaned_data['address'])

            orders = []

            for product in products:
                order_quantity = cart.get(str(product.id), 0)
                if order_quantity > 0:
                    order_item = OrderItem(
                        order=new_order,
                        product=product,
                        total_price=product.price * order_quantity,
                        quantity=order_quantity
                    )
                    orders.append(order_item)

            # Save all order items in one bulk
            OrderItem.objects.bulk_create(orders)

            # Update order instance total price
            new_order.place_order()

            # Clear the cart after creating the orders
            request.session['cart'] = {}

            context = {'order': new_order}
            return render(request, self.template_name, context)

        context = {"products": products, "form": form}
        return render(request, self.template_name, context)


class OrderListView(ListView):
    model = Order
    template_name = 'basket/order_list.html'
    context_object_name = 'orders'
    paginate_by = 5

    def get_queryset(self):

        username = self.request.user
        user = CustomUser.objects.get(username=username)
        return Order.objects.filter(customer=user).order_by('-id')  # Adjust the filtering as needed


class AddToWishlistView(LoginRequiredMixin, View):
    login_url = '/authManager/login/'

    def get(self, request, product_id):
        product = Products.objects.get(id=product_id)
        username = request.user
        customer = CustomUser.objects.get(username=username)

        item_added = WishList.objects.filter(product=product_id, customer=customer).exists()

        if item_added:
            message = f"Item {product.name} is already on your Wish list"
            items = WishList.objects.filter(customer=customer).order_by('-added')
            return render(request, "basket/wishlist.html", {"message": message, "items": items})
        else:
            try:
                wishlist = WishList(
                    customer=customer,
                    product=product
                )
                wishlist.save()
            except Exception as e:
                print(f"Error occurred: {e}")
                return render(request, 'basket/product_detail.html')

            return redirect('wishlist')


class RemoveFromWishlistView(View):
    def get(self, request, product_id):
        username = request.user
        customer = CustomUser.objects.get(username=username)
        product = WishList.objects.get(product=product_id, customer=customer)
        product.delete()
        return redirect("wishlist")


class DiscardWishlistView(LoginRequiredMixin, View):
    def get(self, request):
        username = request.user
        customer = CustomUser.objects.get(username=username)
        WishList.objects.filter(customer=customer).delete()

        return redirect('wishlist')


class WishListView(LoginRequiredMixin, ListView):
    model = WishList
    template_name = 'basket/wishlist.html'
    context_object_name = 'items'

    def get_queryset(self):
        username = self.request.user
        user = CustomUser.objects.get(username=username)
        return WishList.objects.filter(customer=user).order_by('-added')
