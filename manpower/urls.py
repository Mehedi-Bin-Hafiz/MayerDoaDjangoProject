from django.urls import path
from manpower.views import emp_attendance,emp_profile

app_name = 'manpower'

urlpatterns = [
    path('', emp_attendance, name='empAttendance'),
    path('profile/(?P<pk>\d+)', emp_profile, name= "empProfile"),
]
