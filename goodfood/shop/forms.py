from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Order


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = User
        fields = ("username", "email", )

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'phone']
        labels = {'address': 'Адрес', 'phone': 'Телефон'}
