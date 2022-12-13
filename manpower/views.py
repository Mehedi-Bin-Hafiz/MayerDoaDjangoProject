from django.shortcuts import render, HttpResponse
from .models import Employee,Attendance,Salary
from datetime import datetime
import pytz
from django.db.models import Sum, Count


time_zones = pytz.all_timezones
country_time_zone = pytz.timezone('Asia/Dhaka')
country_time = datetime.now(country_time_zone)
today_date = str(country_time).split(' ')[0]
first_day = country_time.replace(day=1)
first_day = str(first_day).split(' ')[0]



def emp_attendance(request):
    emp_model = Employee.objects.all()
    attend_model = Attendance.objects.all()
    return render(request,'attendance.html',{"emp_model":emp_model,"today_date":today_date, "attend_model":attend_model})

def emp_profile(request,pk=None):
    total_present = 0
    total_absent = 0
    salary_remain = 0
    money_value = 0
    fixed_salary = 0

    if pk:
        emp_model = Employee.objects.filter(pk=pk).order_by('-id')
        attend_model = Attendance.objects.filter(employee_id=pk).filter(date__range=[first_day,today_date]).order_by('-date').only('date','present_status').reverse()
        salary_model = Salary.objects.filter(employee_id=pk).filter(date__range=[first_day,today_date]).order_by('-date').only('money_taken').reverse()
        money_taken = Salary.objects.filter(employee_id=pk).filter(date__range=[first_day,today_date]).order_by('-date').aggregate(Sum('money_taken'))
        fixed_salary = Employee.objects.filter(pk=pk).values('fixed_salary')[0]['fixed_salary']
        two_model = zip(attend_model, salary_model)

        if money_taken['money_taken__sum'] is None:
            money_value = 0
        else:
            money_value = money_taken['money_taken__sum']

        for i in attend_model:
            if i.present_status == 'present':
                total_present +=1
            elif i.present_status == 'absent':
                total_absent +=1

        daily_salary = int(fixed_salary)/26
        salary_remain =  round(daily_salary*int(total_present) - int(money_value),2)

    else:
        emp_model = Employee.objects.filter(pk=1) #need to work
        attend_model = Attendance.objects.filter(pk=1)
        salary_model = Salary.objects.filter(pk=1)
        two_model = zip( attend_model, salary_model)
    data = {"emp_model": emp_model,
            "attend_model": attend_model,
            "salary_model": salary_model,
            "today_date": today_date,
            "total_absent": total_absent,
            "total_present": total_present,
            "salary_remain": salary_remain,
            "total_money_taken": money_value,
            "two_model": two_model,
            "fixed_salary": fixed_salary
            }
    return render(request, 'employee_profile.html', context=data)
