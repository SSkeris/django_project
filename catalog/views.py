from django.forms import inlineformset_factory
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from pytils.translit import slugify

from catalog.forms import ProductForm, VersionForm
from catalog.models import Product, Version


# контроллеры для сайта


class ProductListView(ListView):
    """Класс для отображения списка товаров"""
    model = Product

    def get_queryset(self, *args, **kwargs):
        """Фильтрует товары по статусу is_active"""
        queryset = super().get_queryset().order_by(*args, **kwargs)
        queryset = queryset.filter(is_active=True)
        return queryset


class ProductDetailView(DetailView):
    """Класс для отображения детальной информации о товаре"""
    model = Product

    def get_object(self, queryset=None):
        """
        Переопределяем метод для получения количества просмотров.

        Получает объект Product по первичному ключу, увеличивает счетчик просмотров на 1,
        сохраняет изменения и возвращает объект.

        Parameters:
        queryset (QuerySet, optional):
        Набор объектов, из которого получается объект. По умолчанию None, что означает использование
        стандартного набора объектов модели.

        Returns:
        object: Объект Product с увеличенным счетчиком просмотров.
        """
        self.object = super().get_object(queryset)
        self.object.viewed += 1
        self.object.save()
        return self.object


class ProductCreateView(CreateView):
    """Класс для создания нового товара"""
    model = Product
    form_class = ProductForm
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
    form_class = ProductForm
    success_url = reverse_lazy('product_list')

    def get_success_url(self):
        """Перенаправляет на страницу с обновленным товаром"""
        return reverse('product_detail', args=[self.object.pk])

    def get_context_data(self, **kwargs):
        """
        Этот метод используется для предоставления контекстных данных для ProductUpdateView и включает
        форму для управления связанными объектами Version.
        Параметры:
        kwargs (словарь): дополнительные ключевые аргументы, передаваемые методу.
        Возвращает:
        dict: словарь, содержащий контекстные данные для шаблона.
        Контекстные данные включают форму для управления связанными объектами Version.
        Если метод запроса POST, форма заполняется данными из запроса. Если метод запроса не POST,
        форма заполняется данными из текущего объекта Product.
        """
        context_data = super().get_context_data(**kwargs)
        VersionFormSet = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
        if self.request.method == 'POST':
            context_data['formset'] = VersionFormSet(self.request.POST, instance=self.object)
        else:
            context_data['formset'] = VersionFormSet(instance=self.object)
        return context_data

    def form_valid(self, form):
        """
        Этот метод вызывается, когда форма и набор форм действительны. Он сохраняет данные формы и набора форм, а затем перенаправляет на успешный URL.
        Параметры:
        form (Form): объект формы, содержащий проверенные данные.
        formset (InlineFormSet): объект набора форм, содержащий проверенные данные.
        Возвращает:
        HttpResponseRedirect: перенаправление на успешный URL.
        """
        context_data = self.get_context_data()
        formset = context_data['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))
        # """Переопределяем метод для обновления slug"""
        # if form.is_valid():
        #     new_product = form.save()
        #     new_product.slug = slugify(new_product.name)
        #     new_product.save()
        # return super().form_valid(form)


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
