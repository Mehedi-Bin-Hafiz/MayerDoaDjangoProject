from django.urls import path
from products.views import morning_input_confirm,company_morning_groups
from products.views import morning_evening_choice, product_morning_input
from products.views import monthly_sell, company_groups, product_daily_input
from products.views import daily_input_confirm, daily_input_view, today_sell, accounts_section, home

app_name = 'products'

urlpatterns = [
    path('', company_groups, name='companyGroups'),
    path('home/',home, name = 'home'),
    path('morning_group/', company_morning_groups, name='companyMorningGroups'),
    path('morning_eve/', morning_evening_choice, name='morningEvening'),
    path('info_input/(?P<pk>\d+)', product_daily_input , name='productInfoInput'),
    path('input_confirm/(?P<pk>\d+)', daily_input_confirm, name='dailyInputConf'),
    path('morning_input/(?P<pk>\d+)', product_morning_input, name='productMorningInput'),
    path('morning_input_confirm/(?P<pk>\d+)',morning_input_confirm , name='morningInputConf'),
    path('daily_view/',daily_input_view , name='dailyInputView'),
    path('today_view/',today_sell , name='todayView'),
    path('monthly_view/',monthly_sell , name='monthlyView'),
    path('accounts/', accounts_section, name='accountsSection'),

]
