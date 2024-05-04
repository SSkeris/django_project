from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from catalog.models import Product


# контроллеры для сайта


class ProductListView(ListView):
    """Класс для отображения списка товаров"""
    model = Product


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


class ProductUpdateView(UpdateView):
    """Класс для обновления товара"""
    model = Product
    fields = ('name', 'description', 'image', 'category', 'price')
    success_url = reverse_lazy('product_list')

    def get_success_url(self):
        return reverse_lazy('product_detail', args=[self.object.pk])


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
