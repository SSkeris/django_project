from django.shortcuts import render

from catalog.models import Product


# контроллеры для сайта

def product_list(request):
    """Выводит список товаров на сайте"""
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'catalog/product_list.html', context)


def product_detail(request, pk):
    product_pk = Product.objects.get(pk=pk)
    context = {'product': product_pk}
    return render(request, 'catalog/product_detail.html', context)


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
