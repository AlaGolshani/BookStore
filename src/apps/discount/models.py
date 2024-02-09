from django.db import models
from django.core.validators import MaxValueValidator
from django.utils import timezone
from ..extensions.utils import jalali_converter

# مدل تخفیف نقدی (برای کتاب ها تعریف می شود)
from apps.accounts.models import CustomUser


class CashDiscount(models.Model):
    class Meta:
        verbose_name: 'تخفیف نقدی'
        verbose_name_plural = 'تخفیف های نقدی'

    amount = models.PositiveIntegerField('مقدار (تومان)',
                                         validators=[MaxValueValidator(200000)])  # مقدار تخفیف به تومان
    started = models.DateTimeField('زمان شروع')
    expired = models.DateTimeField('زمان پایان')
    creator = models.ForeignKey(CustomUser, blank=True, null=True,
                                on_delete=models.SET_NULL,
                                verbose_name='ایجاد کننده')

    # def j_started(self):
    #     return jalali_converter(self.started)
    #
    # j_started.short_description = 'زمان شروع'
    #
    # def j_expired(self):
    #     return jalali_converter(self.expired)
    #
    # j_started.short_description = 'زمان پایان'


    @property
    def is_valid(self) -> bool:
        """
        بررسی تاریخ انقضای تخفیف
        """
        if self.started < timezone.now() < self.expired:
            return True
        return False

    def __str__(self):
        return f'{self.amount}T'


# مدل تخفیف درصدی (برای کتاب ها تعریف می شود)
class PercentageDiscount(models.Model):
    class Meta:
        verbose_name: 'تخفیف درصدی'
        verbose_name_plural = 'تخفیف های درصدی'

    percentage = models.PositiveIntegerField('درصد')  # مقدار درصد تخفیف
    started = models.DateTimeField('زمان شروع')
    expired = models.DateTimeField('زمان پایان')
    max_amount = models.PositiveIntegerField('حداکثر مقدار تخفیف (تومان)')
    creator = models.ForeignKey(CustomUser, blank=True, null=True,
                                on_delete=models.SET_NULL,
                                verbose_name='ایجاد کننده')

    # def j_started(self):
    #     return jalali_converter(self.started)
    #
    # def j_expired(self):
    #     return jalali_converter(self.expired)

    @property
    def is_valid(self) -> bool:
        """
        بررسی تاریخ انقضای تخفیف
        """
        if self.started < timezone.now() < self.expired:
            return True
        return False

    def __str__(self):
        return f'{self.percentage}%'


# مدل تخفیف امتیازی (توسط مشتری روی سبد خرید اعمال می شود)
class CodeDiscount(models.Model):
    class Meta:
        verbose_name: 'کد تخفیف'
        verbose_name_plural = 'کد های تخفیف'

    code = models.CharField('کد تخفیف', max_length=100)  # کد تخفیف
    percentage = models.PositiveIntegerField('درصد')  # مقدار درصد تخفیف
    started = models.DateTimeField('زمان شروع')
    expired = models.DateTimeField('زمان پایان')
    max_amount = models.PositiveIntegerField('حداکثر مقدار تخفیف (تومان)')
    creator = models.ForeignKey(CustomUser, blank=True, null=True,
                                on_delete=models.SET_NULL,
                                verbose_name='ایجاد کننده')

    # def j_started(self):
    #     return jalali_converter(self.started)
    #
    # def j_expired(self):
    #     return jalali_converter(self.expired)

    @property
    def is_valid(self) -> bool:
        """
        بررسی تاریخ انقضای تخفیف
        """
        if self.started < timezone.now() < self.expired:
            return True
        return False

    def __str__(self):
        return f'{self.percentage}%'
