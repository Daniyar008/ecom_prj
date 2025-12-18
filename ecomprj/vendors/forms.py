from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User
from vendors.models import Vendor
from goods.models import Product, Category


class VendorRegisterForm(UserCreationForm):
    """Форма регистрации вендора"""

    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"placeholder": "Имя пользователя", "class": "form-control"}
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Пароль", "class": "form-control"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Подтвердите пароль", "class": "form-control"}
        )
    )

    # Vendor fields
    shop_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"placeholder": "Название магазина", "class": "form-control"}
        ),
    )
    shop_description = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Описание магазина",
                "class": "form-control",
                "rows": 3,
            }
        ),
    )
    contact = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={"placeholder": "Контактный телефон", "class": "form-control"}
        ),
    )
    address = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={"placeholder": "Адрес", "class": "form-control"}),
    )

    class Meta:
        model = User
        fields = ["username", "email"]


class VendorLoginForm(forms.Form):
    """Форма входа вендора"""

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email", "class": "form-control"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Пароль", "class": "form-control"}
        )
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            from django.contrib.auth import authenticate

            self.user_cache = authenticate(
                self.request, username=email, password=password
            )
            if self.user_cache is None:
                raise forms.ValidationError("Неверный email или пароль")

            if not self.user_cache.is_vendor:
                raise forms.ValidationError(
                    "Этот аккаунт не является аккаунтом продавца"
                )

        return self.cleaned_data

    def get_user(self):
        return getattr(self, "user_cache", None)


class VendorProfileForm(forms.ModelForm):
    """Форма редактирования профиля вендора"""

    class Meta:
        model = Vendor
        fields = [
            "title",
            "image",
            "cover_image",
            "description",
            "address",
            "contact",
            "chat_resp_time",
            "shipping_on_time",
            "authentic_rating",
            "days_return",
            "warranty_period",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "address": forms.TextInput(attrs={"class": "form-control"}),
            "contact": forms.TextInput(attrs={"class": "form-control"}),
            "chat_resp_time": forms.TextInput(attrs={"class": "form-control"}),
            "shipping_on_time": forms.TextInput(attrs={"class": "form-control"}),
            "authentic_rating": forms.TextInput(attrs={"class": "form-control"}),
            "days_return": forms.TextInput(attrs={"class": "form-control"}),
            "warranty_period": forms.TextInput(attrs={"class": "form-control"}),
        }


class VendorProductForm(forms.ModelForm):
    """Форма добавления/редактирования товара вендором"""

    class Meta:
        model = Product
        fields = [
            "title",
            "image",
            "description",
            "category",
            "price",
            "old_price",
            "specifications",
            "type",
            "stock_count",
            "life",
            "mfd",
            "tags",
            "in_stock",
            "digital",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Название товара"}
            ),
            "price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Цена"}
            ),
            "old_price": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "Старая цена"}
            ),
            "type": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Тип товара"}
            ),
            "stock_count": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Количество на складе"}
            ),
            "life": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Срок годности"}
            ),
            "mfd": forms.DateTimeInput(
                attrs={"class": "form-control", "type": "datetime-local"}
            ),
            "category": forms.Select(attrs={"class": "form-control"}),
            "in_stock": forms.CheckboxInput(attrs={"class": "form-check-input"}),
            "digital": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.all()
        self.fields["category"].empty_label = "Выберите категорию"
