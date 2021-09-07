from django.forms import ModelForm
from .models import CashDiscount, PercentageDiscount, CodeDiscount


# فرم های ایجاد تخفیف

class CashDiscountCreationForm(ModelForm):
    class Meta:
        model = CashDiscount
        fields = '__all__'
        exclude = ['creator']


class PercentageDiscountCreationForm(ModelForm):
    class Meta:
        model = PercentageDiscount
        fields = '__all__'
        exclude = ['creator']


class CodeDiscountCreationForm(ModelForm):
    class Meta:
        model = CodeDiscount
        fields = '__all__'
        exclude = ['creator']


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
