from apps.product.models import Category


def global_context(request):
    categories = Category.objects.all()
    context = {'categories': categories, }
    return context
