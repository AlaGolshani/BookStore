from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.text import slugify


class CustomUser(AbstractUser):
    phone_number = models.CharField('شماره تلفن همراه', max_length=11, blank=True, null=True)
    device = models.CharField('دستگاه', max_length=300, blank=True, null=True)
    slug = models.SlugField('اسلاگ', unique=True, editable=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(str(self.username))
        super(CustomUser, self).save(*args, **kwargs)


class Customer(CustomUser):
    class Meta:
        proxy = True
        verbose_name: 'مشتری'
        verbose_name_plural = 'مشتریان'


class Staff(CustomUser):
    class Meta:
        proxy = True
        verbose_name: 'کارمند'
        verbose_name_plural = 'کارمندان'


class Admin(CustomUser):
    class Meta:
        proxy = True
        verbose_name: 'مدیر'
        verbose_name_plural = 'مدیران'


class Address(models.Model):
    class Meta:
        verbose_name: 'آدرس'
        verbose_name_plural = 'آدرس ها'
        ordering = ['pk']

    country = models.CharField('کشور', max_length=50, default='ایران')
    state = models.CharField('استان', max_length=50, default='تهران')
    city = models.CharField('شهر', max_length=50, default='تهران')
    text = models.TextField('آدرس', )
    zip_code = models.CharField('کد پستی', max_length=10, blank=True, null=True)
    default = models.BooleanField('آدرس پیش فرض', default=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='addresses',
                                 blank=True, null=True,
                                 verbose_name='مشتری')

    @staticmethod
    def has_default(customer) -> bool:
        for address in Address.objects.filter(customer=customer):
            if address.default is True:
                return True
        return False

    def __str__(self):
        city = self.city or ''
        state = self.state or ''
        return f"{state}-{city}-{self.text}"

    def save(self, *args, **kwargs):
        if Address.objects.count() == 0:
            self.default = True
        super(Address, self).save(*args, **kwargs)
