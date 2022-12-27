from django.shortcuts import render
from .models import ProductGroup, Products, ProductStatus, DamageProduct
from django.shortcuts import render, HttpResponseRedirect, reverse, redirect
from datetime import datetime
import pytz
from django.db.models import Sum, Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required

today_date = 0
first_day = 0

def date_time_maker():
    global today_date
    global first_day
    country_time_zone = pytz.timezone('Asia/Dhaka')
    country_time = datetime.now(country_time_zone)
    today_date = str(country_time).split(' ')[0]
    first_day = country_time.replace(day=1)
    first_day = str(first_day).split(' ')[0]

def home(request):
    return render(request, 'options.html')
@login_required
def company_groups(request):
    date_time_maker()
    product_groups = ProductGroup.objects.all()
    return render(request,'groups.html',{"product_groups":product_groups})
@login_required
def morning_evening_choice(request):
    date_time_maker()
    product_groups = ProductGroup.objects.all()
    return render(request,'morning_eve_input.html',{"product_groups":product_groups})
@login_required
def company_morning_groups(request):
    date_time_maker()
    product_groups = ProductGroup.objects.all()
    return render(request,'morning_group.html',{"product_groups":product_groups})
@login_required
def product_daily_input(request,pk = None):
    date_time_maker()
    total_products = 0
    product_groups = None
    names_outstatus = None
    if pk:
        product_groups = ProductGroup.objects.filter(id=pk)
        total_products = Products.objects.filter(product_group_id=pk).order_by('-id').annotate(count=Count('name'))
        product_names = Products.objects.filter(product_group_id=pk).order_by('-id')
        product_out = ProductStatus.objects.filter(product_group_id=pk, date = today_date).order_by('-product_id').values_list('product_out',flat=True)
        names_outstatus = zip(product_names,product_out)
    data = {"product_groups": product_groups,
            "names_outstatus": names_outstatus,
            "today_date": today_date,
            "total_products": len(total_products),
            }
    return render(request, 'groups_product_input.html', context=data)
@login_required
def daily_input_confirm(request, pk = None):
    date_time_maker()
    products = Products.objects.filter(product_group_id = pk).values_list('id',flat=True).order_by('-id')
    productReturn = request.POST.getlist('productReturn[]')
    price = request.POST.getlist('Price[]')
    damage_price = request.POST.get('DamagePrice')
    for ind, id in enumerate(products):
        product_status_model = ProductStatus.objects.get(product_id=int(id), product_group_id=pk ,date=today_date)
        product_status_model.product_return = productReturn[ind]
        product_status_model.final_price = price[ind]
        product_status_model.save()
    damage_model = DamageProduct(product_group_id=pk,  date = today_date ,  price=damage_price)
    damage_model.save()
    messages.info(request, 'Selling Information Submitted')
    return redirect('products:productInfoInput', pk = pk)
@login_required
def product_morning_input(request, pk = None):
    date_time_maker()
    total_products = 0
    product_groups = None
    product_names = None
    if pk:
        product_groups = ProductGroup.objects.filter(id=pk)
        total_products = Products.objects.filter(product_group_id=pk).order_by('-id').annotate(count=Count('name'))
        product_names = Products.objects.filter(product_group_id=pk).order_by('-id')
    data = {"product_groups": product_groups,
            "product_names": product_names,
            "today_date": today_date,
            "total_products": len(total_products)
            }
    return render(request, 'group_product_morning_input.html', context=data)
@login_required
def morning_input_confirm(request, pk = None):
    date_time_maker()
    products = Products.objects.filter(product_group_id = pk).values_list('id',flat=True).order_by('-id')
    productOut = request.POST.getlist('productOut[]')
    for ind, id in enumerate(products):
        product_model = ProductStatus(product_id=int(id), product_group_id=pk, date=today_date,product_out=productOut[ind], product_return='0',final_price='0')
        product_model.save()
    messages.info(request, 'First Input Done')
    return redirect('products:productMorningInput', pk = pk)
@login_required
def daily_input_view(request ):
    date_time_maker()
    search_date = request.POST.get('SearchDate')
    pk = request.POST.get('groupSelector')
    try:
        product_groups_name = ProductGroup.objects.filter(id=pk).only('name')[0]
        product_model = Products.objects.filter(product_group_id=pk).order_by('-id').reverse()
        product_status_model = ProductStatus.objects.filter(date = search_date, product_group_id=pk).order_by('-id')
        product_price = ProductStatus.objects.filter(date = search_date, product_group_id=pk).order_by('-id').aggregate(Sum('final_price'))
        damage_price = DamageProduct.objects.filter(date = search_date, product_group_id=pk).order_by('-id').values('price')[0]
        product_and_status = zip(product_model,product_status_model)
        damage_price= int(damage_price['price'])
        product_price = int(product_price['final_price__sum'])
        subtotal = product_price-damage_price
    except:
        messages.info(request, 'no data found')
        return render(request, 'daily_view.html')
    data ={
        "product_and_status":product_and_status,
        "damage_price":damage_price,
        "subtotal": subtotal,
        "today_date":search_date,
        'group_name':product_groups_name
    }
    return render(request, 'daily_view.html', context=data)

@login_required
def today_sell(request):
    date_time_maker()
    try:
        product_price = ProductStatus.objects.filter(date = today_date,).aggregate(Sum('final_price'))
        damage_price = DamageProduct.objects.filter(date = today_date,).aggregate(Sum('price'))
        damage_price= int(damage_price['price__sum'])
        product_price = int(product_price['final_price__sum'])
        subtotal = product_price-damage_price
    except:
        messages.info(request, 'no data found')
        return render(request, 'today_sell.html')
    data ={
        "product_price" : product_price,
        "damage_price":damage_price,
        "subtotal": subtotal,
        "today_date":today_date,

    }
    return render(request, 'today_sell.html', context=data)

@login_required
def monthly_sell(request):
    date_time_maker()
    try:
        product_price = ProductStatus.objects.filter(date__range=[first_day,today_date]).aggregate(Sum('final_price'))
        damage_price = DamageProduct.objects.filter(date__range=[first_day,today_date]).aggregate(Sum('price'))
        damage_price= int(damage_price['price__sum'])
        product_price = int(product_price['final_price__sum'])
        subtotal = product_price-damage_price
    except:
        messages.info(request, 'no data found')
        return render(request, 'monthly_sell.html')
    data ={
        "product_price" : product_price,
        "damage_price":damage_price,
        "subtotal": subtotal,
        "first_date":first_day,
        "today_date":today_date,

    }
    return render(request, 'monthly_sell.html', context=data)


@login_required
def accounts_section(request):
    date_time_maker()
    product_groups = ProductGroup.objects.all()
    return render(request, 'accounts_section.html', {"product_groups": product_groups})