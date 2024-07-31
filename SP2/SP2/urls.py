from django.contrib import admin
from django.urls import path, include
from weather import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),
    path('get_weather/', views.get_weather, name='get_weather'),
    path('history/', views.search_history, name='search_history'),
]