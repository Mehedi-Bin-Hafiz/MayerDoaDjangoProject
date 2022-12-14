from django.shortcuts import render
from .models import ProductGroup, Products, ProductStatus, DamageProduct
from django.shortcuts import render, HttpResponseRedirect, reverse
from datetime import datetime
import pytz
from django.db.models import Sum, Count
from django.contrib import messages

time_zones = pytz.all_timezones
country_time_zone = pytz.timezone('Asia/Dhaka')
country_time = datetime.now(country_time_zone)
today_date = str(country_time).split(' ')[0]
first_day = country_time.replace(day=1)
first_day = str(first_day).split(' ')[0]



def company_groups(request):
    product_groups = ProductGroup.objects.all()

    return render(request,'groups.html',{"product_groups":product_groups})

def product_daily_input(request,pk = None):
    total_products = 0
    if pk:
        product_groups = ProductGroup.objects.filter(id=pk)
        total_products = Products.objects.filter(product_group=pk).order_by('-id').values('name').annotate(count=Count('name'))
    data = {"emp_model": product_groups,
            "attend_model": product_groups,
            "salary_model": product_groups,
            "today_date": 0,
            "total_absent": 0,
            "total_present": 0,
            "salary_remain": 0,
            "total_money_taken": 0,
            "two_model": 0,
            "total_products": total_products
            }
    return render(request, 'groups_product_input.html', context=data)



