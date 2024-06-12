from django.shortcuts import render
from django.http import HttpResponse
from shop.models import Product,Category,Sub_category
from django.db.models import Q

# Create your views here.
def search(request):
    if request.method == "POST":
        query = request.POST['search']
        prdt=Product.objects.filter( Q(product_name__icontains=query) | Q(category__category_name__icontains=query)|Q(Sub_category__sub_category_name__icontains=query))
        if(prdt):
            cnt=Product.objects.filter(Q(product_name__icontains=query) | Q(category__category_name__icontains=query)|Q(Sub_category__sub_category_name__icontains=query)).count()
            return render(request, 'search.html', {'prdt':prdt,'cnt':cnt})
        else:
            return HttpResponse('no result')

    return render(request, 'search.html')
