import jdatetime
from allauth.account.forms import default_token_generator
from allauth.account.utils import user_pk_to_url_str
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView, CreateView, DeleteView
from django.views.generic.base import View
from apps.accounts.forms import (CustomUserChangeForm,
                                 AddressChangeForm,
                                 AddressCreationForm)
from apps.accounts.models import Customer, Address, Admin
from apps.accounts.mixins import SuperUserRequiredMixin
from ..product.models import Book
from ..shoppingbasket.models import Order


# ویو های مربوط به مشتریان

class CustomerEditProfile(LoginRequiredMixin, UpdateView):
    model = Customer
    form_class = CustomUserChangeForm
    template_name = 'account/customer/profile_edit.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super(CustomerEditProfile, self).get_context_data(**kwargs)
        addresses = Address.objects.filter(customer=self.request.user)
        context["addresses"] = addresses
        context["uidb36"] = user_pk_to_url_str(self.request.user)
        temp_key = default_token_generator.make_token(self.request.user)
        context["key"] = temp_key
        return context


class OrderHistory(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            context = {
                'orders': request.user.basket.orders
            }
        except:
            context = {'orders': None}
        return render(request, 'account/customer/order_history.html', context)


# ویو های مربوط به آدرس مشتریان

class CreateAddress(LoginRequiredMixin, CreateView):
    model = Address
    form_class = AddressCreationForm
    template_name = 'account/address/address_create.html'

    def get_success_url(self):
        customer = self.request.user
        # if 'checkout' in self.request.META.get('HTTP_REFERER'):
        #     order = Order.objects.get(created=customer, status='P')
        #     return reverse_lazy('checkout', kwargs={'pk': order.pk})
        return reverse_lazy('accounts:edit', kwargs={'pk': customer.pk})

    def form_valid(self, form):
        """
        کاربری که ریکوئست را ارسال کرده به عنوان صاحب آدرس ذخیره می شود
        آدرس دیفالت بررسی می شود
        """
        form = form.save(commit=False)
        form.customer = self.request.user
        if Address.objects.filter(customer=form.customer).count() > 0 and form.default is True:
            try:
                previous_default_address = Address.objects.get(customer=form.customer, default=True)
                previous_default_address.default = False
                previous_default_address.save()
            except:
                pass
        elif Address.objects.filter(customer=form.customer).count() == 0:
            form.default = True
        form.save()
        return super(CreateAddress, self).form_valid(form)


class EditAddress(LoginRequiredMixin, UpdateView):
    model = Address
    form_class = AddressChangeForm
    template_name = 'account/address/address_update.html'

    def get_success_url(self):
        customer_id = self.request.user.pk
        return reverse_lazy('accounts:edit', kwargs={'pk': customer_id})

    def form_valid(self, form):
        """
        کاربری که ریکوئست را ارسال کرده به عنوان صاحب آدرس ذخیره شود
        آدرس دیفالت هم چک شود
        """
        form = form.save()
        if form.default is True and Address.objects.filter(customer=form.customer).count() > 0:
            try:
                previous_default_address = Address.objects.exclude(id=form.id).get(customer=form.customer, default=True)
                previous_default_address.default = False
                previous_default_address.save()
            except:
                pass
        if form.default is False and not Address.has_default(form.customer):
            form.default = True
        form.save()
        return super(EditAddress, self).form_valid(form)


class DeleteAddress(LoginRequiredMixin, DeleteView):
    model = Address
    template_name = 'account/address/address_confirm_delete.html'

    def get_success_url(self):
        customer_id = self.request.user.pk
        return reverse_lazy('accounts:edit', kwargs={'pk': customer_id})

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if Address.objects.filter(customer=self.object.customer).count() == 1:
            raise Http404("حداقل یک آدرس برای حساب کاربری باید وجود داشته باشد.")
        else:
            return super(DeleteAddress, self).delete(
                request, *args, **kwargs)


# ویو مربوط به گزارش گیری مدیر
class Report(SuperUserRequiredMixin, LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        orders = Order.objects.all()
        income = 0
        for order in orders:
            income += order.get_price
        today = jdatetime.datetime.today()
        context = {
            'customers_num': Customer.objects.filter(is_staff=False).count(),
            'staffs_num': Customer.objects.filter(is_staff=True, is_superuser=False).count(),
            'admins_num': Admin.objects.filter(is_superuser=True).count(),
            'orders_num': Order.objects.filter(Q(status='S') | Q(status='D')).count(),
            'discounts_num': Book.objects.filter(Q(cash_discount__isnull=False) |
                                                 Q(percentage_discount__isnull=False)).count(),
            'no_discounts_num': Book.objects.filter(Q(cash_discount__isnull=True),
                                                    Q(percentage_discount__isnull=True)).count(),
            'income': income,
            'today': today,
        }
        return render(request, 'account/admin/report.html', context)
