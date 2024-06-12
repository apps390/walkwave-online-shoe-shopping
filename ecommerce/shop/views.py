from django.shortcuts import render
from shop.models import Category, Sub_category, Banner, Brand, Product, Size, Color
from django.db.models import Q
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required()
def show_category(request, n):
    c = Category.objects.get(id=n)
    s = Sub_category.objects.filter(category=c)
    b = Banner.objects.get(category=c)
    selected_brand_id = request.GET.get('brand')
    selected_color_id = request.GET.get('color')
    selected_price_range = request.GET.get('price_range')
    p = Product.objects.filter(category=c)
    if selected_brand_id:
        selected_brand = Brand.objects.get(id=selected_brand_id)
        p = p.filter(brand=selected_brand)
    if selected_color_id:
        selected_color = Color.objects.get(id=selected_color_id)
        p = p.filter(color=selected_color)
    if selected_price_range:
        if selected_price_range == 'increase':
            p = p.order_by('product_price')
        else:
            p = p.order_by('-product_price')
    br = Brand.objects.filter(categories=c)
    color = Color.objects.filter(categories=c)
    return render(request, 'categories.html', {'s': s, 'c': c, 'b': b, 'br': br, 'color': color, 'p': p})

def sub_category(request,n):
    sb=Sub_category.objects.get(id=n)
    pr = Product.objects.filter(Sub_category=sb)
    br = Brand.objects.filter(sub_categories=sb)
    color = Color.objects.filter(sub_categories=sb)
    selected_brand_id = request.GET.get('brand')
    selected_color_id = request.GET.get('color')
    selected_price_range = request.GET.get('price_range')
    if selected_brand_id:
        selected_brand = Brand.objects.get(id=selected_brand_id)
        pr = pr.filter(brand=selected_brand)
    if selected_color_id:
        selected_color = Color.objects.get(id=selected_color_id)
        pr = pr.filter(color=selected_color)
    if selected_price_range:
        if selected_price_range == 'increase':
            pr = pr.order_by('product_price')
        else:
            pr = pr.order_by('-product_price')
    return render(request, 'subcategory.html', {'pr': pr,'sb':sb,'br': br, 'color': color})

def productdetails(request, n):
    p = Product.objects.get(id=n)
    s = Size.objects.filter(product=p)
    related_products = Product.objects.filter(Sub_category=p.Sub_category).exclude(id=n)[:3]
    return render(request, 'productdetails.html', {'p': p, 's': s, 'related_products': related_products})
