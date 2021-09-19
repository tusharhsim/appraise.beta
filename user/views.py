from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from .models import Person, RequestService, ProvideService, JobAlert, HiringAlert
from .forms import UserRegisterForm, PersonUpdateForm, RequestServiceForm, ProvideServiceForm, ApplyForJob, HireFreelancer

from datetime import datetime, timedelta

##basics##
def login_validator(request):
        try:
                if request.user.username != '':
                        return True
        except:
                pass
def index(request):
        days = 0
        for i in RequestService.objects.all():
                if i.deadline is None:
                      continue
                if i.deadline <= datetime.now().date()+timedelta(days=days):
                        print(f'expiring in {days} days {i}')
                        i.delete()
                else:
                        print(f'time remaining for expiry {i.deadline-datetime.now().date()}')

        try:
                data = Person.objects.get(user=request.user)
        except:
                data = None
        return render(request, 'index.html', {'title':'Home',
                                              'name':request.user, 'misc':data,
                                              'all_users' : get_user_model().objects.all()})

def register(request):
        if login_validator(request):
                messages.success(request, f'Already logged in!')
                return redirect('dashboard')
        if request.method == 'POST':
                form = UserRegisterForm(request.POST)
                if form.is_valid():
                        form.save()
                        messages.success(request, f'Account created successfully!')
                        return redirect('login')
                else:
                        messages.error(request, f'Improper / duplicate data')
        form = UserRegisterForm()
        return render(request, 'register.html', {'form': form, 'title':'Sign-up | Appraise'})

def Login(request):
        if login_validator(request):
                messages.success(request, f'Already logged in!')
                return redirect('dashboard')
        if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(request, username = username, password = password)
                if user is not None:
                        form = login(request, user)
                        messages.success(request, f' Howdy {username}!')
                        return redirect('dashboard')
                else:
                        messages.error(request, f'Incorrect/invalid credentials')
        form = AuthenticationForm()
        return render(request, 'login.html', {'form':form, 'title':'Login'})


##user##
def dashboard(request):
        return render(request, 'dashboard.html', {'name':request.user, 'title':'Dashboard', 'all_users' : get_user_model().objects.all()})

def update(request):
        try:
                misc = Person.objects.filter(user=request.user).annotate()
                misc = misc[0]
                data = {'pin_code' : misc.pin_code, 'name' : misc.name, 'contact' : misc.contact, 'dob' : misc.dob, 'gender' : misc.gender, 'visibility' : misc.visibility}
                form = PersonUpdateForm(initial=data)
        except:
                form = PersonUpdateForm()
                data = None

        if request.method == 'POST':
                form = PersonUpdateForm(request.POST)
                if form.is_valid():
                        if not data:
                                    try:
                                        profile = form.save(commit=False)
                                        profile.user = request.user
                                        profile.save()
                                        messages.success(request, f'Information feeeded!')
                                        return redirect('dashboard')
                                    except Exception as e:
                                            messages.error(request, e)
                        else:
                                Person.objects.filter(user=request.user).update(pin_code = form.cleaned_data['pin_code'], name = form.cleaned_data['name'], contact = form.cleaned_data['contact'], dob = form.cleaned_data['dob'], gender = form.cleaned_data['gender'], visibility = form.cleaned_data['visibility'])
                                messages.success(request, f'Information updated!')
                                return redirect('dashboard')
                else:
                        messages.error(request, f'Couldn\'t update data!')
        return render(request, 'update.html', {'form': form, 'title':'Update', 'name': request.user, 'misc': data})

##elementary tasks##
def open_requests(request):
        try:
                services_requested = RequestService.objects.filter(user=request.user).order_by('-id').annotate()
                services_offered = ProvideService.objects.filter(user=request.user).order_by('-id').annotate()
        except:
                services_requested, services_offered = None, None
        return render(request, 'open_requests.html', {'name':request.user, 'title':'Instances', 'services_requested':services_requested, 'services_offered':services_offered})

def notification(request):
        job_alerts = JobAlert.objects.filter(user=request.user).order_by('-id').annotate()
        hiring_alerts = HiringAlert.objects.filter(user=request.user).order_by('-id').annotate()
        return render(request, 'notification.html', {'name':request.user, 'title':'Notification', 'job_alerts':job_alerts, 'hiring_alerts':hiring_alerts})

##browse##
def browse_local_jobs(request):
        try:
                pin = Person.objects.get(user=request.user).pin_code
                services_requested = RequestService.objects.filter(pin_code=pin).exclude(user=request.user).order_by('-id').annotate()
                message = 'Find and apply for the jobs that interests/suits you (in your locality):'
        except:
                pin, services_requested = None, None
                message = 'Sorry! No localised work is available at the moment; you can still look out for global job listings'
        aply_to = JobAlert.objects.filter(requester=request.user).annotate()
        try:
                aply = [i.job.id for i in aply_to]
        except:
                aply = []
        return render(request, 'browse_jobs.html', 
        {'title':'Browse | Local Jobs', 'name':request.user, 'message':message, 'extent':'global', 'url':'browse_global_jobs', 'open_services':services_requested, 'my_requests':aply})

def browse_local_freelancers(request):
        try:
                pin = Person.objects.get(user=request.user).pin_code
                services_offered = ProvideService.objects.filter(pin_code=pin).exclude(user=request.user).order_by('-id').annotate()
                message = 'Find and hire freelancers who meets your requirements (in your locality):'
        except:
                pin, services_offered = None, None
                message = 'Sorry! No localised freelancer is available at the moment; you can still look out for global freelancer listings'
        ask_for = HiringAlert.objects.filter(employer=request.user).annotate()
        try:
                ask = [i.task.id for i in ask_for]
        except:
                ask = []
        return render(request, 'browse_freelancers.html', 
        {'title':'Browse | Local Freelancers', 'name':request.user, 'message':message, 'extent':'global', 'url':'browse_global_freelancers', 'open_services':services_offered, 'my_requests':ask})

def browse_global_jobs(request):
        try:
                services_requested = RequestService.objects.all().exclude(user=request.user).order_by('-id').annotate()
                message = 'Find and apply for the jobs that interests/suits you (globally):'
        except:
                services_requested = None
                message = 'Sorry! No work is available at the moment; you can still post your request'
        aply_to = JobAlert.objects.filter(requester=request.user).annotate()
        try:
                aply = [i.job.id for i in aply_to]
        except:
                aply = []
        return render(request, 'browse_jobs.html', 
        {'title':'Browse | Global Jobs', 'name':request.user, 'message':message, 'extent':'local', 'url':'browse_local_jobs', 'open_services':services_requested, 'my_requests':aply})

def browse_global_freelancers(request):
        try:
                services_offered = ProvideService.objects.all().exclude(user=request.user).order_by('-id').annotate()
                message = 'Find and hire freelancers who meets your requirements (globally):'
        except:
                services_offered = None
                message = 'Sorry! No freelancer is available at the moment; you can still post your request'
        ask_for = HiringAlert.objects.filter(employer=request.user).annotate()
        try:
                ask = [i.task.id for i in ask_for]
        except:
                ask = []
        return render(request, 'browse_freelancers.html', 
        {'title':'Browse | Global Freelancers', 'name':request.user, 'message':message, 'extent':'local', 'url':'browse_local_freelancers', 'open_services':services_offered, 'my_requests':ask})

##real work##
def apply_for_job(request, user, job_id, job_title):
        requester_data = Person.objects.get(user=request.user)
        data_items = {'pin_code' : requester_data.pin_code, 'contact' : requester_data.contact}
        form = ApplyForJob(initial=data_items)
        if request.method == 'POST':
                form = ApplyForJob(request.POST)
                if form.is_valid():
                        try:
                                job = form.save(commit=False)
                                job.user = User.objects.get(username=user)
                                job.job_id = job_id
                                job.job_title = job_title
                                job.requester = request.user
                                job.requester_rating = requester_data.employability
                                job.save()
                                messages.success(request, f'Applied for job successfully, we will keep you updated!')
                                return redirect('browse_local_jobs')
                        except Exception as e:
                                messages.error(request, e)
                else:
                        messages.error(request, f'Invalid form!')
        return render(request, 'apply.html', {'form': form, 'title':'Apply for job'})

def hire_a_freelancer(request, user, task_id, task_title):
        requester_data = Person.objects.get(user=request.user)
        data_items = {'pin_code' : requester_data.pin_code, 'contact' : requester_data.contact}
        form = HireFreelancer(initial=data_items)
        if request.method == 'POST':
                form = HireFreelancer(request.POST)
                if form.is_valid():
                        try:
                                job = form.save(commit=False)
                                job.user = User.objects.get(username=user)
                                job.task_id = task_id
                                job.task_title = task_title
                                job.employer = request.user
                                job.employer_rating = requester_data.employer_rating
                                job.save()
                                messages.success(request, f'Request sent to freelancer, we will keep you updated!')
                                return redirect('browse_local_freelancers')
                        except Exception as e:
                                messages.error(request, e)
                else:
                        messages.error(request, f'Invalid form!')
        return render(request, 'hire.html', {'form': form, 'title':'Hire a freelancer'})

def requested_services(request):
        try:
                applied_jobs = JobAlert.objects.filter(requester=request.user).order_by('-id').annotate()
        except:
                applied_jobs = None
        try:
                requested_freelancers = HiringAlert.objects.filter(employer=request.user).order_by('-id').annotate()
        except:
                requested_freelancers = None        
        return render(request, 'requested_services.html', {'name':request.user, 'title':'Requested services', 'applied_jobs':applied_jobs, 'requested_freelancers':requested_freelancers})

def delete_requested_jobs(request, job_id):
        JobAlert.objects.filter(requester=request.user).filter(job_id=job_id).delete()
        return redirect('requested_services')

def delete_requested_freelancers(request, task_id):
        HiringAlert.objects.filter(employer=request.user).filter(task_id=task_id).delete()
        return redirect('requested_services')

##services##
def services(request):
        return render(request, 'services.html', {'name':request.user, 'title':'Services | Home'})

def ask_for_service(request):
        try:
                pin = Person.objects.get(user=request.user).pin_code
        except:
                messages.error(request, 'Please update your PIN first')
                return redirect('update')
        if request.method == 'POST':
                form = RequestServiceForm(request.POST)
                if form.is_valid():
                            try:
                                job = form.save(commit=False)
                                job.user = request.user
                                job.pin_code = pin
                                job.save()
                                messages.success(request, f'Job posted successfully!')
                                return redirect('open_requests')
                            except Exception as e:
                                    messages.error(request, e)
                else:
                        messages.error(request, f'Couldn\'t update data!')
        form = RequestServiceForm()
        return render(request, 'ask_for_service.html', {'form': form, 'name':request.user, 'title':'Service | Request'})

def update_asked_services(request, i_id):
        misc = RequestService.objects.filter(user=request.user).filter(id=i_id).annotate()
        misc = misc[0]
        data = {'title' : misc.title, 'tag' : misc.tag, 'contact' : misc.contact, 'deadline' : misc.deadline, 'location' : misc.location, 'pay_scale' : misc.pay_scale}
        form = RequestServiceForm(initial=data)
        if request.method == 'POST':
                form = RequestServiceForm(request.POST)
                if form.is_valid():
                        RequestService.objects.filter(user=request.user).filter(id=i_id).update(title = form.cleaned_data['title'], tag = form.cleaned_data['tag'], contact = form.cleaned_data['contact'], deadline = form.cleaned_data['deadline'], location = form.cleaned_data['location'], pay_scale = form.cleaned_data['pay_scale'])
                        messages.success(request, f'Information for asked service updated!')
                        return redirect('open_requests')
                else:
                        messages.error(request, f'Couldn\'t update data!')
        return render(request, 'update_services.html', {'form': form, 'title':'Update | Ask_Service', 'misc': data})

def delete_asked_services(request, i_id):
        RequestService.objects.filter(user=request.user).filter(id=i_id).delete()
        return redirect('open_requests')

def offer_a_service(request):
        try:
                pin = Person.objects.get(user=request.user).pin_code
        except:
                messages.error(request, 'Please update your PIN first')
                return redirect('update')
        if request.method == 'POST':
                form = ProvideServiceForm(request.POST)
                if form.is_valid():
                            try:
                                job = form.save(commit=False)
                                job.user = request.user
                                job.pin_code = pin
                                job.save()
                                messages.success(request, f'Request for job generated!')
                                return redirect('open_requests')
                            except Exception as e:
                                    messages.error(request, e)
                else:
                        messages.error(request, f'Couldn\'t update data!')

        form = ProvideServiceForm()
        return render(request, 'offer_a_service.html', {'form': form, 'name':request.user, 'title':'Service | Offer'})

def update_offered_services(request, i_id):
        misc = ProvideService.objects.filter(user=request.user).filter(id=i_id).annotate()
        misc = misc[0]
        data = {'title' : misc.title, 'tag' : misc.tag, 'contact' : misc.contact, 'location' : misc.location, 'pay_scale' : misc.pay_scale}
        form = ProvideServiceForm(initial=data)
        if request.method == 'POST':
                form = ProvideServiceForm(request.POST)
                if form.is_valid():
                        ProvideService.objects.filter(user=request.user).filter(id=i_id).update(title = form.cleaned_data['title'], tag = form.cleaned_data['tag'], contact = form.cleaned_data['contact'], location = form.cleaned_data['location'], pay_scale = form.cleaned_data['pay_scale'])
                        messages.success(request, f'Information for offered service updated!')
                        return redirect('open_requests')
                else:
                        messages.error(request, f'Couldn\'t update data!')
        return render(request, 'update_services.html', {'form': form, 'title':'Update | Offer_Service', 'misc': data})

def delete_offered_services(request, i_id):
        ProvideService.objects.filter(user=request.user).filter(id=i_id).delete()
        return redirect('open_requests')
