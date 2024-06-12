from cart.models import Cart
def cart_num(request):
    cnt=0
    if request.user.is_authenticated: #because if the user is authenticated then only it has to execute the function
        u=request.user
        try:
            c=Cart.objects.filter(user=u)
            for i in c:
                cnt+=i.quantity
        except:
            cnt=0
    return {'cnt':cnt}
