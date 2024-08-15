from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from url_shortener.views import URLListView, URLCreateView, URLRedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', URLListView.as_view(), name='url-list'),
    path('create/', URLCreateView.as_view(), name='url-create'),
    path('<slug:short_url>/', URLRedirectView.as_view(), name='url-redirect'),
]