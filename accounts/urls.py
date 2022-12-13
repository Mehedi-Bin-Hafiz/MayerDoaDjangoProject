from django.urls import path
from accounts.views import owner_login,owner_logout

app_name = 'accounts'

urlpatterns = [
    path('', owner_login, name='ownerLogin'),
    path('logout/', owner_logout, name='ownerLogOut'),
]
