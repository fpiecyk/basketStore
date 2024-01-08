from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.ItemsListView.as_view(), name='shop'),
    path('add_to_cart/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('cart_update/', views.CartUpdateView.as_view(), name='cart_update'),
    path('cart_display/', views.CartDisplayView.as_view(), name='cart_display'),
    path('order_confirmation/', views.OrderCreateView.as_view(), name='order_confirmation'),
    path('order_list/', views.OrderListView.as_view(), name='order_list'),
    path('product_detail/<int:pk>', views.ProductDetailView.as_view(), name='product_detail'),
    path('wishlist/', views.WishListView.as_view(), name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', views.AddToWishlistView.as_view(), name='add_to_wishlist'),
    path('remove-from-wishlist/<int:product_id>/', views.RemoveFromWishlistView.as_view(), name='remove_from_wishlist'),
    path('discard_wishlist/', views.DiscardWishlistView.as_view(), name='discard_wishlist'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)