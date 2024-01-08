from django.forms import ModelForm

from basket.models import Order


class ShippingAddressForm(ModelForm):
    class Meta:
        model = Order
        fields = ['address']
        labels = {
            "address": "Please specify shipping address"
        }