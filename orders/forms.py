from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address', 'phone', 'postal_code', 'city']
        labels = {
            "first_name": "Имя ", "last_name": "Фамилия ", "email": "Email ", "address": "Адрес ", "phone": "Номер телефона ", "postal_code": "Почтовый индекс ", "city": "Город "
        }