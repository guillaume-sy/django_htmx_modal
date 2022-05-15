from django.urls import path
from . import views
from .views import FactoryTableModalView

urlpatterns = [
    path('factory_modal/', FactoryTableModalView.as_view(), name='factory_modal'),
    path('index/', views.product_index, name='product_index'),
    path('product_form/', views.product_form, name='product_form'),
]
