from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from catalog.views import product_list, contacts, product_detail

# пути для страниц на сайте
urlpatterns = [
                  path('', product_list, name='product_list'),
                  path('catalog/<int:pk>/', product_detail, name='product_detail'),
                  path('contacts/', contacts)
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
