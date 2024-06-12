import razorpay
from django.shortcuts import render, redirect
from shop.models import Product, Size
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from cart.models import Cart, Coupon
from django.contrib import messages
from django.contrib.auth.models import User
from django.conf import settings
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
# Create your views here.
@login_required()
def view_cart(request):
    u = request.user
    c = Cart.objects.filter(user=u)
    total = 0
    disc = 0
    subtotal = 0
    for i in c:
        total += i.quantity * i.product.product_price
    shp_chg = int((total * 5) / 100)
    if request.method == "POST":
        cpo = request.POST.get('coupon')
        try:
            cp = Coupon.objects.get(coupon_name=cpo)
            disc_prct = cp.discount
            print(disc_prct)
            bf_disc = total + shp_chg
            disc = int((bf_disc * disc_prct) / 100)
            subtotal = bf_disc - disc
        except:
            pass
    else:
        subtotal = total + shp_chg + disc
    return render(request, 'cart.html',
                  {'c': c, 'total': total, 'shp_chg': shp_chg, 'subtotal': subtotal, 'disc': disc})


def add_to_cart(request, p):
    sz = request.POST.get('size')
    print (sz)
    if not sz:
        messages.error(request, 'Select Your Size')
        return redirect(reverse('shop:prdtdetail', args=[p]))
    else:
        sze = Size.objects.get(id=sz)
        s = Product.objects.get(id=p)
        u = request.user
        try:
            c = Cart.objects.get(user=u, product=s, size=sze)
            if (sze.stock > 1):
                c.quantity += 1
                sze.stock -= 1
                s.save()
                sze.save()
                c.save()
                return view_cart(request)
        except:
            if (sze.stock > 1):
                c = Cart.objects.create(user=u, product=s, size=sze, quantity=1)
                sze.stock -= 1
                c.save()
                s.save()
                sze.save()
                return view_cart(request)

    return render(request, 'cart.html')


def quantity_add(request, p, s):
    u = request.user
    pr = Product.objects.get(id=p)
    sz = Size.objects.get(id=s)
    try:
        c = Cart.objects.get(user=u, product=pr, size=sz)
        if (sz.stock > 1):
            print('product received')
            c.quantity += 1
            sz.stock -= 1
            c.save()
            sz.save()
            pr.save()
    except:
        if (sz.stock > 1):
            c = Cart.objects.create(user=u, product=pr, size=sz)
            sz.stock -= 1
            sz.save()
            pr.save()
            c.save()
    return view_cart(request)


def quantity_remove(request, p, s):
    u = request.user
    pr = Product.objects.get(id=p)
    sz = Size.objects.get(id=s)
    try:
        c = Cart.objects.get(user=u, product=pr, size=sz)
        if (c.quantity > 1):
            c.quantity -= 1
            sz.stock += 1
            c.save()
            sz.save()
            pr.save()
        else:
            sz.stock += 1
            c.delete()

    except:
        pass

    return view_cart(request)


def remove_item(request, p, s):
    u = request.user
    pr = Product.objects.get(id=p)
    sz = Size.objects.get(id=s)
    c = Cart.objects.get(user=u, product=pr, size=sz)
    c.delete()
    return view_cart(request)



def checkout(request):
    if request.method == 'POST':
        ttl_amnt = request.POST.get('total_amount')
        ttl=request.POST.get('total')
        dis = request.POST.get('discount')
        dlv=request.POST.get('delivery')
        request.session['total']=ttl_amnt
        return render(request,'checkout.html',{'ttl_amnt':ttl_amnt,'ttl':ttl,'dlv':dlv,'dis':dis})

def initiate_payment(request):
    if request.method=='POST':
        name =request.POST['name']
        email = request.POST['email']
        phoneno =request.POST['phoneno']
        amnt=request.session.get('total')
        amount = int(amnt)*100# Razorpay works with paise
        payment = client.order.create({'amount': amount, 'currency': 'INR', 'payment_capture': '1'})
        context={
            'name':name,
            'payment':payment,
            'amount':amount,
            'key_id': settings.RAZORPAY_KEY_ID,
            'email':email,
            'phone':phoneno

        }
        return render(request,'confirm_payment.html',context)
def payment_complete(request):
    if request.method == 'POST':
        payment_id = request.POST.get('razorpay_payment_id')
        order_id = request.POST.get('razorpay_order_id')
        signature = request.POST.get('razorpay_signature')
        params_dict = {
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
        status=client.utility.verify_payment_signature(params_dict)
        if status:
            u=request.user
            c = Cart.objects.filter(user=u)
            c.delete()
            return render(request, 'paymnt_cmplt.html',{'status':True,'payment_id':payment_id})
        else:
            return render(request, 'paymnt_cmplt.html',{'status':False})










