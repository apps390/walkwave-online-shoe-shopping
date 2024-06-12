"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from cart import views

app_name = 'cart'
urlpatterns = [
    path('addtocart/<int:p>', views.add_to_cart, name='adcrt'),
    path('viewcart', views.view_cart, name='vwcrt'),
    path('qntadd/<int:p>/<int:s>', views.quantity_add, name='qntyadd'),
    path('qntrmv/<int:p>/<int:s>', views.quantity_remove, name='qntyrmv'),
    path('rmvitm/<int:p>/<int:s>', views.remove_item, name='rmvitem'),
    path('checkout', views.checkout, name='chkout'),
    path('initiate_pay/', views.initiate_payment,name='initiate_pymnt'),
    path('pymnt_status',views.payment_complete,name='complete_pymnt')


]
