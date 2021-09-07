from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import DeleteView
from .models import *


class Cart(View):
    def get(self, request, *args, **kwargs):
        try:
            assert not request.user.is_anonymous
            customer = request.user
        except:
            device = request.COOKIES['device']
            if Customer.objects.filter(username=device).exists():
                customer = Customer.objects.get(username=device)
            else:
                customer = Customer.objects.create(device=device, username=device)

        # customer = request.user

        # ایجاد سبد خرید در صورت لزوم
        basket, created = ShoppingBasket.objects.get_or_create(customer=customer)

        try:
            order = Order.objects.get(shopping_basket=basket, status='P')
            context = {'order': order}
        except:
            context = {'order': None}

        return render(request, 'shoppingbasket/cart.html', context)

    def post(self, request, *args, **kwargs):
        # اعمال کردن تخفیف روی سبد خرید
        if request.is_ajax():
            discount_code = request.POST['discount']
            qs = CodeDiscount.objects.filter(code__exact=discount_code)

            if qs.exists():
                discount_obj = CodeDiscount.objects.get(code__exact=discount_code)
                if discount_obj.is_valid:
                    try:
                        assert not request.user.is_anonymous
                        customer = request.user
                    except:
                        device = request.COOKIES['device']
                        if Customer.objects.filter(username=device).exists():
                            customer = Customer.objects.get(username=device)
                        else:
                            customer = Customer.objects.create(device=device, username=device)

                    basket, created = ShoppingBasket.objects.get_or_create(customer=customer)
                    order = Order.objects.get(shopping_basket=basket, status='P')

                    # ثبت کد تخفیف برای این سفارش و ذخیره آن
                    order.discount_code = discount_obj
                    order.save()
                    return JsonResponse(
                        {
                            'valid': True,
                            'total_price': order.get_price,
                            'total_discount': order.get_total_discount,
                            'message': f'{order.discount_code.percentage} درصد تخفیف اعمال شد.',
                        },
                        status=200
                    )
                else:
                    return JsonResponse(
                        {
                            'valid': False,
                            'message': 'کد تخفیف منقضی شده است.',
                        },
                        status=200,
                    )

            return JsonResponse(
                {
                    'valid': False,
                    'message': 'کد تخفیف نامعتبر است.',
                },
                status=200
            )


class PreviousCart(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        order = Order.objects.get(pk=pk)
        context = {'order': order}
        return render(request, 'shoppingbasket/cart.html', context)


class DeleteItemView(DeleteView):
    model = OrderItem
    success_url = reverse_lazy('cart')
    template_name = 'shoppingbasket/cart.html'

    def post(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            order_item = OrderItem.objects.get(pk=pk)
            order_item.book.quantity += order_item.item_count
            order_item.book.save()
            super().post(request, pk, *args, **kwargs)
            return JsonResponse(
                {
                    'order_original_price': order_item.order.get_original_price,
                    'total_discount': order_item.order.get_total_discount,
                    'order_price': order_item.order.get_price,
                    'items_count': order_item.order.get_items_count,
                }
            )


class CounterInput(View):
    def post(self, request, pk, *args, **kwargs):
        if request.is_ajax():
            counter = request.POST['counter']
            order_item = OrderItem.objects.get(pk=pk)
            if counter == '+':
                if order_item.book.quantity < 1:
                    return JsonResponse({'valid': False,
                                         'message': f'موجودی این کتاب {order_item.item_count} عدد می باشد.',
                                         }, status=200)
                order_item.item_count += 1
                order_item.book.quantity -= 1
            else:
                order_item.item_count -= 1
                order_item.book.quantity += 1
            order_item.save()
            order_item.book.save()
            return JsonResponse(
                {
                    'valid': True,
                    'item_price': order_item.get_price,
                    'order_original_price': order_item.order.get_original_price,
                    'total_discount': order_item.order.get_total_discount,
                    'order_price': order_item.order.get_price,
                    'items_count': order_item.order.get_items_count,
                },
                status=200
            )


class Checkout(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        addresses = Address.objects.filter(customer=request.user)
        context = {
            'addresses': addresses,
            'order_pk': kwargs['order_pk']
        }
        return render(request, 'shoppingbasket/checkout.html', context)

    def post(self, request, *args, **kwargs):
        address_pk = request.POST['address_pk']
        address = Address.objects.get(pk=address_pk)
        order = Order.objects.get(pk=kwargs['order_pk'])
        order.address = address
        order.status = 'S'
        order.ordered = timezone.now()
        order.save()
        return redirect(reverse_lazy('accounts:orders'))
