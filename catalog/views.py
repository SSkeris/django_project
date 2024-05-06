from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from pytils.translit import slugify

from catalog.models import Product


# контроллеры для сайта


class ProductListView(ListView):
    """Класс для отображения списка товаров"""
    model = Product

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset().order_by(*args, **kwargs)
        queryset = queryset.filter(is_active=True)
        return queryset


class ProductDetailView(DetailView):
    """Класс для отображения детальной информации о товаре"""
    model = Product

    def get_object(self, queryset=None):
        """Переопределяем метод для получения количества просмотров"""
        self.object = super().get_object(queryset)
        self.object.viewed += 1
        self.object.save()
        return self.object


class ProductCreateView(CreateView):
    """Класс для создания нового товара"""
    model = Product
    fields = ('name', 'description', 'image', 'category', 'price')
    success_url = reverse_lazy('product_list')

    def form_valid(self, form):
        if form.is_valid():
            new_product = form.save()
            new_product.slug = slugify(new_product.name)
            new_product.save()
        return super().form_valid(form)


class ProductUpdateView(UpdateView):
    """Класс для обновления товара"""
    model = Product
    fields = ('name', 'description', 'image', 'category', 'price')
    success_url = reverse_lazy('product_list')

    def get_success_url(self):
        """Перенаправляет на страницу с обновленным товаром"""
        return reverse('product_detail', args=[self.object.pk])

    def form_valid(self, form):
        """Переопределяем метод для обновления slug"""
        if form.is_valid():
            new_product = form.save()
            new_product.slug = slugify(new_product.name)
            new_product.save()
        return super().form_valid(form)


class ProductDeleteView(DeleteView):
    """Класс для удаления товара"""
    model = Product
    success_url = reverse_lazy('product_list')


# при переходе на CBV "context" в данном случае меняется на {'object_list': products}'}, по этому необходимо
# этот параметр изменить на странице в templates, а именно в product_list.html
# так же заменяются адреса в url-ах приложения
# название и путь к шаблону
# app_name/<model_name>_<action>
# catalog/product_list.html


# FBV вариант
# def product_list(request):
#     """Выводит список товаров на сайте"""
#     products = Product.objects.all()
#     context = {'products': products}
#     return render(request, 'catalog/product_list.html', context)

# FBV вариант
# def product_detail(request, pk):
#     product_pk = Product.objects.get(pk=pk)
#     context = {'product': product_pk}
#     return render(request, 'catalog/product_detail.html', context)


def contacts(request):
    """Принимает контактные данные от пользователя с сайта"""
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')
        print(f'Ваше сообщение: {name}, {phone}, {message}')
        with open('write.txt', 'wt', encoding='UTF-8') as file:
            file.write(f'Ваше сообщение: {name}, {phone}, {message}')

    return render(request, 'catalog/contacts.html')


def toggle_active(request, pk):
    """Переключает активность товара"""
    product_item = get_object_or_404(Product, pk=pk)
    if product_item.is_active:
        product_item.is_active = False
    else:
        product_item.is_active = True
    product_item.save()
    return redirect('product_list')
