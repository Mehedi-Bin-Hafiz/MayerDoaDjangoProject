from django.urls import path
from products.views import monthly_sell, company_groups, product_daily_input, daily_input_confirm, daily_input_view, today_sell

app_name = 'products'

urlpatterns = [
    path('', company_groups, name='companyGroups'),
    path('info_input/(?P<pk>\d+)',product_daily_input , name='productInfoInput'),
    path('input_confirm/(?P<pk>\d+)',daily_input_confirm , name='dailyInputConf'),
    path('daily_view/(?P<pk>\d+)',daily_input_view , name='dailyInputView'),
    path('today_view/',today_sell , name='todayView'),
    path('monthly_view/',monthly_sell , name='monthlyView'),

]
