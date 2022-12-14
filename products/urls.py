from django.urls import path
from products.views import company_groups, product_daily_input

app_name = 'products'

urlpatterns = [
    path('', company_groups, name='companyGroups'),
    path('info_input/(?P<pk>\d+)',product_daily_input , name='productInfoInput'),

]
