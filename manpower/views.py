from django.shortcuts import render, HttpResponseRedirect, reverse
from .models import Employee,Attendance,Salary
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

@login_required
def emp_attendance(request):
    date_time_maker()
    emp_model = Employee.objects.all().order_by("-id")
    attend_model = Attendance.objects.all().order_by("-id")
    return render(request,'attendance.html',{"emp_model":emp_model,"today_date":today_date, "attend_model":attend_model})
@login_required
def emp_profile(request,pk=None):
    date_time_maker()
    total_present = 0
    total_absent = 0
    salary_remain = 0
    money_value = 0
    fixed_salary = 0

    if pk:
        emp_model = Employee.objects.filter(id=pk).order_by('-id')
        attend_model = Attendance.objects.filter(employee_id=pk).filter(date__range=[first_day,today_date]).order_by('-date').only('date','present_status').reverse()
        salary_model = Salary.objects.filter(employee_id=pk).filter(date__range=[first_day,today_date]).order_by('-date').only('money_taken').reverse()
        money_taken = Salary.objects.filter(employee_id=pk).filter(date__range=[first_day,today_date]).order_by('-date').aggregate(Sum('money_taken'))
        fixed_salary = Employee.objects.filter(id=pk).values('fixed_salary')[0]['fixed_salary']
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

@login_required
def confirm_attendance(request):
    date_time_maker()

    present_id = request.POST.getlist('present[]')
    absent_id = request.POST.getlist('absent[]')
    money_Taken = request.POST.getlist('moneyTaken[]')
    emp_id = present_id + absent_id
    emp_id = sorted(emp_id, reverse=True)
    for id in present_id:
        attend_model = Attendance(date=today_date,employee_id=int(id),present_status="present")
        attend_model.save()
    for id in absent_id:
        absent_model = Attendance(date=today_date,employee_id=int(id),present_status="absent")
        absent_model.save()
    for id, money in zip(emp_id,money_Taken):
        try:
            money = float(money.strip())
        except:
            money = 0.0
        salary_model = Salary(date=today_date,employee_id=int(id),money_taken=money)
        salary_model.save()
    messages.info(request, 'Attendance is taken')
    return HttpResponseRedirect(reverse('empProfile:empAttendance'))
