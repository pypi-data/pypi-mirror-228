
from django import forms
from django.utils.translation import gettext_lazy as _

from orders.models import Order


class CheckoutForm(forms.ModelForm):

    city = forms.CharField(
        label=_('City'),
        required=False
    )

    warehouse = forms.CharField(
        label=_('Warehouse'),
        required=False
    )

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']
        if mobile.startswith('+3800'):
            raise forms.ValidationError(
                _('Phone number could not start with `+3800`'))
        return mobile

    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'middle_name', 'payment_method',
            'delivery_method', 'mobile', 'comment'
        ]
