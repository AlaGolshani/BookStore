from django.forms import ModelForm, TextInput, NumberInput, DateTimeInput
from .models import CashDiscount, PercentageDiscount, CodeDiscount


# فرم های ایجاد تخفیف

class CashDiscountCreationForm(ModelForm):
    class Meta:
        model = CashDiscount
        fields = '__all__'
        exclude = ['creator']

        widgets = {
            'amount': NumberInput(attrs={'class': 'form-control w-50 m-1 m-auto',
                                         'placeholder': 'چند تومان؟ ...'}),
            'started': DateTimeInput(attrs={'class': 'form-control m-1 w-50 m-auto',
                                            'placeholder': 'زمان شروع ...'}),
            'expired': DateTimeInput(attrs={'class': 'form-control m-1 w-50 m-auto',
                                            'placeholder': 'زمان پایان ...'}),
        }
        labels = {key: '' for key in ['amount', 'started', 'expired']}  # removing the labels


class PercentageDiscountCreationForm(ModelForm):
    class Meta:
        model = PercentageDiscount
        fields = '__all__'
        exclude = ['creator']

        widgets = {
            'percentage': NumberInput(attrs={'class': 'form-control w-50 m-1 m-auto',
                                             'placeholder': 'چند درصد؟ ...'}),
            'started': DateTimeInput(attrs={'class': 'form-control m-1 w-50 m-auto',
                                            'placeholder': 'زمان شروع ...'}),
            'expired': DateTimeInput(attrs={'class': 'form-control m-1 w-50 m-auto',
                                            'placeholder': 'زمان پایان ...'}),

            'max_amount': NumberInput(attrs={'class': 'form-control w-50 m-1 m-auto',
                                             'placeholder': 'حداکثر مقدار تخفیف (تومان) ...'}),
        }
        labels = {key: '' for key in ['percentage', 'started',
                                      'expired', 'max_amount']}  # removing the labels


class CodeDiscountCreationForm(ModelForm):
    class Meta:
        model = CodeDiscount
        fields = '__all__'
        exclude = ['creator']

        widgets = {
            'code': TextInput(attrs={'class': 'form-control w-50 m-1 m-auto',
                                     'placeholder': 'کد تخفیف ...'}),
            'percentage': NumberInput(attrs={'class': 'form-control w-50 m-1 m-auto',
                                             'placeholder': 'چند درصد؟ ...'}),
            'started': DateTimeInput(attrs={'class': 'form-control m-1 w-50 m-auto',
                                            'placeholder': 'زمان شروع ...'}),
            'expired': DateTimeInput(attrs={'class': 'form-control m-1 w-50 m-auto',
                                            'placeholder': 'زمان پایان ...'}),

            'max_amount': NumberInput(attrs={'class': 'form-control w-50 m-1 m-auto',
                                             'placeholder': 'حداکثر مقدار تخفیف (تومان) ...'}),
        }
        labels = {key: '' for key in ['code', 'percentage', 'started',
                                      'expired', 'max_amount']}  # removing the labels


# فرم های ویرایش تخفیف

class CashDiscountChangeForm(ModelForm):
    class Meta:
        model = CashDiscount
        fields = '__all__'
        exclude = ['creator']


class PercentageDiscountChangeForm(ModelForm):
    class Meta:
        model = PercentageDiscount
        fields = '__all__'
        exclude = ['creator']


class CodeDiscountChangeForm(ModelForm):
    class Meta:
        model = CodeDiscount
        fields = '__all__'
        exclude = ['creator']
