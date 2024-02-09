from django.db import models
from ..extensions.utils import jalali_converter
from ..product.models import Book
from ..discount.models import CodeDiscount
from ..accounts.models import Address, Customer


# مدل سبد خرید
class ShoppingBasket(models.Model):
    class Meta:
        verbose_name: 'سبد خرید'
        verbose_name_plural = 'سبد های خرید'

    customer = models.OneToOneField(Customer,
                                    on_delete=models.CASCADE,
                                    related_name='basket',
                                    blank=True,
                                    null=True,
                                    verbose_name='مشتری')


# مدل سفارش
class Order(models.Model):
    class Meta:
        verbose_name: 'سفارش'
        verbose_name_plural = 'سفارش ها'
        ordering = ('-ordered',)

    STATUSES = [
        ('P', 'در انتظار پرداخت'),
        ('S', 'درحال ارسال'),
        ('D', 'تحویل داده شده')
    ]
    shopping_basket = models.ForeignKey(ShoppingBasket,
                                        on_delete=models.CASCADE,
                                        related_name='orders',
                                        verbose_name='سبد خرید')
    address = models.ForeignKey(Address,
                                on_delete=models.DO_NOTHING,
                                related_name='orders',
                                blank=True, null=True,
                                verbose_name='آدرس')
    discount_code = models.ForeignKey(CodeDiscount,
                                      on_delete=models.SET_NULL,
                                      blank=True, null=True,
                                      verbose_name='کد تخفیف')
    status = models.CharField('وضعیت', max_length=1,
                              choices=STATUSES,
                              default=STATUSES[0][0])
    ordered = models.DateTimeField('زمان ثبت سفارش', blank=True, null=True)

    # def j_ordered(self):
    #     return jalali_converter(self.ordered)

    @property
    def get_total_discount(self) -> int:
        """
        مقدار کل تخفیف را برمی گرداند
        """
        return self.get_original_price - self.get_price

    @property
    def get_original_price(self) -> int:
        """
        مبلغ کل سفارش بدون درنظر گرفتن تخفیف ها را برمی گرداند
        """
        order_items = self.order_items.all()
        total = sum([item.get_original_price for item in order_items])
        return int(total)

    @property
    def get_price(self) -> int:
        """
        مبلغ کل سفارش با درنظر گرفتن تخفیف ها را برمی گرداند
        """
        order_items = self.order_items.all()
        total = sum([item.get_price for item in order_items])

        try:
            if self.discount_code.is_valid:
                percentage = self.discount_code.percentage
                if (self.get_original_price * percentage / 100) > self.discount_code.max_amount:
                    discount = self.discount_code.max_amount
                else:
                    discount = total * percentage / 100
            else:
                raise AssertionError
        except:
            discount = 0

        total -= discount
        return int(total)

    @property
    def get_items_count(self) -> int:
        """
        تعداد کل کالا ها را برمی گرداند
        """
        order_items = self.order_items.all()
        total = sum([item.item_count for item in order_items])
        return total


# مدل هر ردیف از سفارش
class OrderItem(models.Model):
    class Meta:
        verbose_name: 'آیتم سفارش'
        verbose_name_plural = 'آیتم های سفارش'
        ordering = ['pk']

    order = models.ForeignKey(Order, on_delete=models.CASCADE,
                              related_name='order_items',
                              verbose_name='سفارش')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='کتاب')
    item_count = models.PositiveIntegerField('تعداد', default=0)

    @property
    def get_original_price(self) -> int:
        """
        قیمت کل آیتم را بدون درنظر گرفتن تخفیف ها برمی گرداند
        """
        return self.book.price * self.item_count

    @property
    def get_price(self) -> int:
        """
        قیمت کل آیتم را با درنظر گرفتن تخفیف ها برمی گرداند
        """
        return self.book.get_price * self.item_count

    def __str__(self):
        return f"{self.item_count} of {self.book.title}"
