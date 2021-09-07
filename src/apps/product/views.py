from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, UpdateView, DeleteView
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView
from apps.accounts.mixins import StaffRequiredMixin
from .forms import CategoryCreationForm, BookChangeForm, BookCreationForm
from .models import Book
from ..accounts.models import Customer
from ..shoppingbasket.models import Order, OrderItem, ShoppingBasket


class BookDetailView(DetailView):
    model = Book
    template_name = 'product/book/book_detail.html'

    # @method_decorator(login_required)
    def post(self, request, slug, *args, **kwargs):
        product = Book.objects.get(slug=slug)

        # بررسی موجودی کتاب
        if product.quantity == 0:
            return JsonResponse({'valid': False}, status=200)
        else:
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

            # ایجاد سفارشات در صورت لزوم
            order, created = Order.objects.get_or_create(shopping_basket=basket, status='P')
            order_item, created = OrderItem.objects.get_or_create(order=order, book=product)

            # ذخیره تعداد کتاب
            order_item.item_count = 1
            order_item.book.quantity -= 1
            order_item.book.save()
            order_item.save()

            return JsonResponse({'valid': True}, status=200)


class CategoryCreateView(StaffRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = CategoryCreationForm
    success_url = reverse_lazy('home')
    template_name = 'product/category/category_create.html'

    def form_valid(self, form):
        """
        کاربری که ریکوئست را ارسال کرده به عنوان ایجاد کننده دسته بندی ذخیره شود
        """
        category = form.save(commit=False)
        category.creator = self.request.user
        return super(CategoryCreateView, self).form_valid(form)


class BookCreateView(StaffRequiredMixin, LoginRequiredMixin, CreateView):
    form_class = BookCreationForm
    success_url = reverse_lazy('home')
    template_name = 'product/book/book_create.html'

    def form_valid(self, form):
        """
        کاربری که ریکوئست را ارسال کرده به عنوان ایجاد کننده کتاب ذخیره شود
        """
        book = form.save(commit=False)
        book.creator = self.request.user
        return super(BookCreateView, self).form_valid(form)


class BookUpdateView(StaffRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Book
    form_class = BookChangeForm
    success_url = reverse_lazy('home')
    template_name = 'product/book/book_update.html'


class BookDeleteView(StaffRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('home')
    template_name = 'product/book/book_confirm_delete.html'

    # def post(self, request, *args, **kwargs):
    #     if request.is_ajax():
    #         book = Book.objects.get(slug__exact=kwargs.get('slug'))
    #         book.delete()
    #         super(BookDeleteView).post(request, *args, **kwargs)
    #         return JsonResponse({'valid': True}, status=200)
