from django import forms
from .models import Product


class ProductForm(forms.ModelForm):

    class Meta:

        model = Product

        fields = [
            'name',
            'category',
            'price',
            'description',
            'image',
            'image_2',
            'image_3'
        ]

        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Product name'
            }),

            'category': forms.Select(attrs={
                'class': 'form-input'
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': 'Product price'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-input',
                'placeholder': 'Product description',
                'rows': 5
            }),

            'image': forms.ClearableFileInput(attrs={
                'class': 'form-input'
            }),

            'image_2': forms.ClearableFileInput(attrs={
                'class': 'form-input'
            }),

            'image_3': forms.ClearableFileInput(attrs={
                'class': 'form-input'
            }),
        }


class CheckoutForm(forms.Form):

    customer_name = forms.CharField(
        max_length=200,
        label='Full Name',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Your full name'
        })
    )

    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-input',
            'placeholder': 'Your email'
        })
    )

    phone = forms.CharField(
        max_length=20,
        label='Phone Number',
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': '03XXXXXXXXX'
        })
    )

    address = forms.CharField(
        label='Delivery Address',
        widget=forms.Textarea(attrs={
            'class': 'form-input',
            'placeholder': 'Your complete delivery address',
            'rows': 4
        })
    )
