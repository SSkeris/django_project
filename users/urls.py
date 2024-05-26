from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateView, email_verification, reset_password

app_name = UsersConfig.name
# пути для страниц на сайте
urlpatterns = [
                path('login/', LoginView.as_view(template_name='login.html'), name='login'),
                path('logout/', LogoutView.as_view(), name='logout'),
                path('register/', UserCreateView.as_view(), name='register'),
                path('email-confirm/<str:token>/', email_verification, name='email-confirm'),
                path("reset_password/", reset_password, name="reset_password"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
