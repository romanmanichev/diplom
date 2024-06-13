from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('create/', views.CreateView.as_view(), name='create'),
    path('theme/', views.ThemeView.as_view(), name='theme'),
]