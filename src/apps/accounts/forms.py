from allauth.account.forms import SignupForm
from django.forms import ModelForm, TextInput, Textarea
from .models import Customer, Address, CustomUser
from django import forms


class MyCustomSignupForm(SignupForm):
    class Meta:
        model = CustomUser

    def save(self, request):
        """
        طبق عملیات این متد،
        اگر کاربر قبل از اینکه ثبت نام کند کتابی به سبدخرید خود اضافه کرده باشد،
        بعد از ثبت نام سبد خریدش حفظ می شود
        """
        user = super(MyCustomSignupForm, self).save(request)
        try:
            device = request.COOKIES['device']
            customer = Customer.objects.get(username=device)
            basket = customer.basket
            basket.customer = user
            basket.save()
            customer.delete()
        except:
            pass
        user.save()
        return user


# فرم ویرایش کاربران
class CustomUserChangeForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'phone_number')

        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control w-50 m-1',
                                           'placeholder': 'نام ...'}),
            'last_name': TextInput(attrs={'class': 'form-control m-1 w-50',
                                          'placeholder': 'نام خانوادگی ...'}),
            'email': TextInput(attrs={'class': 'form-control m-1 w-50',
                                      'placeholder': 'ایمیل ...'}),
            'phone_number': TextInput(attrs={'class': 'form-control m-1  w-50', 'rows': 3,
                                             'placeholder': 'شماره موبایل ...'}),
        }
        labels = {key: '' for key in ['first_name', 'last_name',
                                      'email', 'phone_number']}  # removing the labels


# فرم ثبت نام کاربران
class CustomUserCreationForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'phone_number')


# فرم های مربوط به آدرس

class AddressCreationForm(ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        exclude = ['customer']

        widgets = {
            'country': TextInput(attrs={'class': 'form-control w-50 m-1',
                                        'placeholder': 'کشور ...'}),
            'state': TextInput(attrs={'class': 'form-control m-1 w-50',
                                      'placeholder': 'استان ...'}),
            'city': TextInput(attrs={'class': 'form-control m-1 w-50',
                                     'placeholder': 'شهر ...'}),
            'text': Textarea(attrs={'class': 'form-control m-1', 'rows': 3,
                                    'placeholder': 'آدرس ...'}),
            'zip_code': TextInput(attrs={'class': 'form-control m-1 w-50',
                                         'placeholder': 'کدپستی ...'}),
            # 'default': forms.BooleanField(),
        }
        labels = {key: '' for key in ['country', 'state',
                                      'city', 'text',
                                      'zip_code']}  # removing the labels


class AddressChangeForm(ModelForm):
    class Meta:
        model = Address
        fields = '__all__'
        exclude = ['customer']

        widgets = {
            'country': TextInput(attrs={'class': 'form-control w-50 m-1',
                                        'placeholder': 'کشور ...'}),
            'state': TextInput(attrs={'class': 'form-control m-1 w-50',
                                      'placeholder': 'استان ...'}),
            'city': TextInput(attrs={'class': 'form-control m-1 w-50',
                                     'placeholder': 'شهر ...'}),
            'text': Textarea(attrs={'class': 'form-control m-1', 'rows': 3,
                                    'placeholder': 'آدرس ...'}),
            'zip_code': TextInput(attrs={'class': 'form-control m-1 w-50',
                                         'placeholder': 'کدپستی ...'}),
            # 'default': forms.BooleanField(),
        }
        labels = {key: '' for key in ['country', 'state',
                                      'city', 'text',
                                      'zip_code']}  # removing the labels
