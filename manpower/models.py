from django.db import models



class Employee(models.Model):
    name = models.CharField(blank=True,null=True,max_length=50)
    department = models.CharField(blank=True,null=True,max_length=100)
    fixed_salary =  models.FloatField(blank=True,null=True,default=0.00)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(blank=True,null=True,)
    present_status = models.CharField(blank=True,null=True,max_length=50, default='absent')
    def __str__(self):
        return self.employee.name

class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(blank=True,null=True,)
    money_taken = models.FloatField(blank=True,null=True,default=0.00)
    def __str__(self):
        return self.employee.name