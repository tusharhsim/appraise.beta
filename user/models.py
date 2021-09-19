from django.contrib.auth.models import User
from django.db import models

GENDER_CHOICES = (
   ('Male', 'Male'),
   ('Female', 'Female'),
   ('Other', 'Other')
)
SECTORS = (
    ('Domestic','Domestic'),
    ('Education','Education'),
    ('Teaching','Teaching'),
    ('Telecommunication','Telecommunication'),
    ('Hospitality','Hospitality'),
    ('Tourism','Tourism'),
    ('Mass-Media','Mass-Media'),
    ('Healthcare/Hospitals','Healthcare/Hospitals'),
    ('Pharmacy','Pharmacy'),
    ('Information-Technology','Information-Technology'),
    ('Waste Disposal','Waste Disposal'),
    ('Consulting','Consulting'),
    ('Retail Sales','Retail Sales'),
    ('FMCG','FMCG'),
    ('Franchising','Franchising'),
    ('Real-Estate','Real-Estate'),
    ('Financial Services','Financial Services'),
    ('Banking','Banking'),
    ('Insurance','Insurance'),
    ('Investment Management','Investment Management'),
    ('Professional Services','Professional Services'),
    ('Legal Services','Legal Services'),
    ('Management Consulting','Management Consulting'),
    ('Transportation','Transportation'),
    ('Others','Others'),
)

class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    pin_code = models.CharField('PIN CODE', max_length=6, blank=False)
    name = models.CharField("Full name", max_length=18, null=True, blank=True)
    contact = models.CharField("Contact info", max_length=10, null=True, blank=True)
    dob = models.DateField("Date of birth", auto_now=False, null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=6, null=True, blank=True)
    visibility = models.BooleanField("Profile visibility", default=True)
    employability = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    employer_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)

    def __str__(self):
        return self.user.username

class RequestService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pin_code = models.CharField(max_length=6)
    title = models.CharField('Job title', max_length=180)
    tag = models.CharField(choices=SECTORS, max_length=64, null=True)
    contact = models.CharField("Contact info", max_length=10)
    deadline = models.DateField('Job deadline', auto_now=False, null=True, blank=True)
    location = models.CharField(max_length=180, null=True, blank=True)
    pay_scale = models.PositiveIntegerField('Wage cost', null=True, blank=True)

    def __str__(self):
        return self.title

class ProvideService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pin_code = models.CharField(max_length=6)
    title = models.CharField(max_length=180)
    tag = models.CharField(choices=SECTORS, max_length=64, null=True)
    contact = models.CharField("Contact info", max_length=10)
    location = models.CharField(max_length=180, null=True, blank=True)
    pay_scale = models.PositiveIntegerField('Expected paycheck', null=True, blank=True)

    def __str__(self):
        return self.title

class JobAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True)
    job = models.ForeignKey(RequestService, on_delete=models.CASCADE, related_name='job', null=True)
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requester', null=True)
    pin_code = models.CharField('PIN CODE', max_length=6, null=True)
    contact = models.CharField("Contact info", max_length=10, null=True)
    ask_amount = models.PositiveIntegerField('Expected paycheck', null=True)

    def __str__(self):
        return self.user.username

class HiringAlert(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='freelancer', null=True)
    task = models.ForeignKey(ProvideService, on_delete=models.CASCADE, related_name='task', null=True)
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='employer', null=True)
    pin_code = models.CharField('PIN CODE', max_length=6, null=True)
    contact = models.CharField("Contact info", max_length=10, null=True)
    bid_amount = models.PositiveIntegerField('Expected budget', null=True)

    def __str__(self):
        return self.user.username

#class status_job(models.Model):
 #   user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user', null=True)
 #   job = models.ForeignKey(RequestService, on_delete=models.CASCADE, related_name='job', null=True)
 #   requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requester', null=True)
 #   pin_code = models.CharField('PIN CODE', max_length=6, null=True)
 #   contact = models.CharField("Contact info", max_length=10, null=True)
 #   ask_amount = models.PositiveIntegerField('Expected paycheck', null=True)

  #  def __str__(self):
  #      return self.user.username
