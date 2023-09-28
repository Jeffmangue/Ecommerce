from django.shortcuts import render
from django.contrib.auth.models import User, Group
from .models import ProductsModel, ProductImagesModel, CartModel
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required

def Homepage(request):
    products = ProductsModel.objects.all()
    try:
        username = request.user.username

        myinfo = User.objects.get(username=username)
        

        my_cart = CartModel.objects.filter(user=myinfo).count()


        user = User.objects.get(id=request.user.id)
        info = CartModel.objects.filter(user=user).all()
        ids = []
        for i in info:
            ids.append(i.product_id)


        dict = {}
        dict_list = []

        for i in ids:
            p = ProductsModel.objects.filter(id=i).first()
            q = CartModel.objects.filter(product_id=i).first()

            price = float(p.price)
            total = int(price) * int(q.quantity)

            img = p.product_images.first()
            dict["id"] = q.id
            dict["image"] = img.image.url
            dict["name"] = p.name
            dict["price"] = p.price
            dict["qty"] = q.quantity
            dict["total"] = total
            dict_list.append(dict)
            dict = {}

        classes = dict_list

        user = User.objects.get(id=request.user.id)
        cart_count = CartModel.objects.filter(user=user).count()
        user_status="True"
    except:
        cart_count=0
        classes =[]
        user_status="False"
    context = {
        'products':products,
        'cart_count': cart_count,
        'classes':classes,
        'user_status':user_status
    }
    return render(request, 'Homepage/home.html', context)


def create(request):
    id = request.POST['id']
    qty = request.POST['qty']
    
    user = User.objects.get(id=request.user.id)
    c = CartModel.objects.filter(product_id=id).count()
    if c > 0:
        b = CartModel.objects.filter(product_id=id).first()
        bb = int(b.quantity) + int(qty)
        CartModel.objects.filter(user=user,product_id=id).update(quantity=bb)
        cart_count = CartModel.objects.filter(user=user).count()
    else:
         a = CartModel(user=user,product_id=id,quantity=qty)
         a.save()
         cart_count = CartModel.objects.filter(user=user).count()
      
    
    response = {
         'cart_count': cart_count
    }
    return JsonResponse(response)


def read(request):
    id = request.GET['id']
    user = User.objects.get(id=id)
    info = CartModel.objects.filter(user=user).all()
    my_cart = CartModel.objects.filter(user=user).count()
    ids = []
    for i in info:
        ids.append(i.product_id)

    products = ProductsModel.objects.filter(id__in=ids).values("name")
    products = json.dumps(list(products))

    dict = {}
    dict_list = []

    for i in ids:
        p = ProductsModel.objects.filter(id=i).first()
        q = CartModel.objects.filter(product_id=i).first()
        price = float(p.price)
        total = int(price) * int(q.quantity)
        img = p.product_images.first()
        dict["id"] = q.id
        dict["image"] = img.image.url
        dict["name"] = p.name
        dict["price"] = p.price
        dict["qty"] = q.quantity
        dict["total"] = total
        dict_list.append(dict)
        dict = {}

    classes = dict_list
    classes = json.dumps(list(classes))

    test = ""

    response = {
    'test':test,
    'products':products,
    'classes':classes,
    'my_cart':my_cart
    }
    return JsonResponse(response)


def delete(request):
    id = request.GET['id']
    username = request.GET['username']
  
    try:
        c = CartModel.objects.filter(id=id).first()
        u = User.objects.get(username=username)
        CartModel.objects.filter(id=id).delete()
        my_cart = CartModel.objects.filter(user=u).count()
        msg = 'success'
    except:
        msg = 'error'
    
    response = {
        'msg':msg,
        'my_cart':my_cart
    }
    return JsonResponse(response)

def login(request):
    context = {
       
    }
    return render(request, 'homepage/login.html', context)

@login_required(login_url='login')
def checkout(request):
    username = request.user.username
    myinfo = User.objects.get(username=username)
    products = ProductsModel.objects.all()

    my_cart = CartModel.objects.filter(user=myinfo).count()

    user = User.objects.get(id=request.user.id)
    info = CartModel.objects.filter(user=user).all()
    ids = []
    for i in info:
        ids.append(i.product_id)

    dict = {}
    dict_list = []
    total_ = 0

    for i in ids:
        p = ProductsModel.objects.filter(id=i).first()
        q = CartModel.objects.filter(product_id=i).first()
        price = float(p.price)
        total = int(price) * int(q.quantity)
        if q.checked == True:
            img = p.product_images.first()
            dict["id"] = q.id
            dict["image"] = img.image.url
            dict["name"] = p.name
            dict["price"] = p.price
            dict["qty"] = q.quantity
            dict["total"] = total
            dict_list.append(dict)
            dict = {}
            total_ += total

    classes = dict_list
    
  
    context = {
        'myinfo': myinfo,
        'products':products,
        'my_cart':my_cart,
        'classes':classes,
        'total_':total_
    }
    return render(request, 'homepage/checkout.html', context)