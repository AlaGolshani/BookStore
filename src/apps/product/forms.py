from django.forms import ModelForm
from .models import Book, Category


# فرم ثبت کتاب
class BookCreationForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        exclude = ['created', 'slug', ]
        exclude = ['creator']


# فرم ویرایش کتاب
class BookChangeForm(ModelForm):
    class Meta:
        model = Book
        fields = '__all__'
        exclude = ['created', 'slug', 'creator']


# فرم ثبت دسته بندی
class CategoryCreationForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        exclude = ['creator']
