from django.urls import path
from manpower.views import emp_attendance,emp_profile, confirm_attendance

app_name = 'manpower'

urlpatterns = [
    path('', emp_attendance, name='empAttendance'),
    path('profile/(?P<pk>\d+)', emp_profile, name= "empProfile"),
    path('confirmattend/', confirm_attendance, name="confirmAttend"),
]
