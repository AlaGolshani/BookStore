from django.contrib.admin.options import InlineModelAdmin
from django.db import models

from ..accounts.models import CustomUser
from ..discount.models import CashDiscount, PercentageDiscount
from django.utils.text import slugify
from .utils import get_random_code
from django.shortcuts import reverse

# مدل دسته بندی کتاب ها
from ..extensions.utils import jalali_converter


class Category(models.Model):
    class Meta:
        verbose_name: 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'
        ordering = ['pk']

    name = models.CharField('نام', max_length=128, unique=True)
    slug = models.SlugField('اسلاگ', unique=True, allow_unicode=True, editable=False)
    creator = models.ForeignKey(CustomUser, blank=True, null=True,
                                on_delete=models.SET_NULL,
                                verbose_name='ایجاد کننده')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super(Category, self).save(*args, **kwargs)


# مدل کتاب
class Book(models.Model):
    class Meta:
        verbose_name: 'کتاب'
        verbose_name_plural = 'کتاب ها'
        ordering = ['created']

    title = models.CharField('عنوان', max_length=128)
    price = models.PositiveIntegerField('قیمت')
    categories = models.ManyToManyField(Category, verbose_name='دسته بندی ها')
    author = models.CharField('نویسنده', max_length=128)
    summary = models.TextField('خلاصه', blank=True, null=True)
    quantity = models.PositiveIntegerField('موجودی')  # موجودی کتاب در انبار
    image = models.ImageField('عکس', upload_to='books/', blank=True, null=True)
    created = models.DateTimeField('زمان ایجاد', auto_now_add=True)
    cash_discount = models.ForeignKey(CashDiscount, on_delete=models.SET_NULL,
                                      blank=True, null=True,
                                      verbose_name='تخفیف نقدی')
    percentage_discount = models.ForeignKey(PercentageDiscount,
                                            on_delete=models.SET_NULL,
                                            blank=True, null=True,
                                            verbose_name='تخفیف درصدی')
    slug = models.SlugField('اسلاگ', unique=True, allow_unicode=True, editable=False)
    creator = models.ForeignKey(CustomUser, blank=True, null=True,
                                on_delete=models.SET_NULL,
                                verbose_name='ایجاد کننده')

    def j_created(self):
        return jalali_converter(self.created)

    @property
    def imageURL(self):
        """
        آدرس عکس کتاب را برمی گرداند
        """
        try:
            url = self.image.url
        except:
            url = ''
        return url

    @property
    def get_price(self):
        """
        قیمت کتاب را با درنظر گرفتن تخفیف ها برمی گرداند
        """
        total = self.price

        # بررسی تاریخ انقضای تخفیف درصورت وجود آن

        try:  # بررسی و محاسبه تخفیف نقدی
            if self.cash_discount.is_valid:
                cash_dis = self.cash_discount.amount
            else:
                raise AssertionError
        except:
            cash_dis = 0

        try:  # بررسی و محاسبه تخفیف درصدی
            if self.percentage_discount.is_valid:
                percentage_dis = self.percentage_discount.percentage
                percentage_dis = self.price * percentage_dis / 100
                if self.percentage_discount.max_amount < percentage_dis:
                    percentage_dis = self.percentage_discount.max_amount
            else:
                raise AssertionError
        except:
            percentage_dis = 0

        if cash_dis > total:
            total = 0
        else:
            total -= cash_dis  # اعمال تخفیف نقدی
            total -= percentage_dis  # اعمال تخفیف درصدی

        return int(total)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', kwargs={'slug': self.slug})

    def get_add_to_order_url(self):
        return reverse('add_to_order', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):

        # ذخیره اسلاگ
        if not self.slug:
            to_slug = slugify(self.title, allow_unicode=True)
            ex = Book.objects.filter(slug=to_slug).exists()
            while ex:
                to_slug = slugify(to_slug + "-" + str(get_random_code()), allow_unicode=True)
                ex = Book.objects.filter(slug=to_slug).exists()
            self.slug = to_slug
        super(Book, self).save(*args, **kwargs)
