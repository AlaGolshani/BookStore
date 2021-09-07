from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import *
from apps.accounts.mixins import StaffRequiredMixin


class CashDiscountCreateView(StaffRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = CashDiscountCreationForm
    success_url = reverse_lazy('home')
    template_name = 'discount/discount_create.html'

    def form_valid(self, form):
        """
        یوزری که ریکوئست را ارسال کرده به عنوان ایجاد کننده تخفیف ذخیره شود
        """
        form.instance.creator = self.request.user
        return super(CashDiscountCreateView, self).form_valid(form)


class PercentageDiscountCreateView(StaffRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = PercentageDiscountCreationForm
    success_url = reverse_lazy('home')
    template_name = 'discount/discount_create.html'

    def form_valid(self, form):
        """
        یوزری که ریکوئست را ارسال کرده به عنوان ایجاد کننده تخفیف ذخیره شود
        """
        form.instance.creator = self.request.user
        return super(PercentageDiscountCreateView, self).form_valid(form)


class CodeDiscountCreateView(StaffRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = CodeDiscountCreationForm
    success_url = reverse_lazy('home')
    template_name = 'discount/discount_create.html'

    def form_valid(self, form):
        """
        یوزری که ریکوئست را ارسال کرده به عنوان ایجاد کننده تخفیف ذخیره شود
        """
        form.instance.creator = self.request.user
        return super(CodeDiscountCreateView, self).form_valid(form)
