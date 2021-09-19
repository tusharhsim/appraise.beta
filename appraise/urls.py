from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth

from django.views.static import serve
from django.conf.urls import url
from django.conf import settings

from user import views as user_view

urlpatterns = [
        
        url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
        url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 

	path('admin/', admin.site.urls),
	path('', include('user.urls')),
        path('register', user_view.register, name ='register'),
	path('login', user_view.Login, name ='login'),
	path('logout', auth.LogoutView.as_view(template_name ='index.html'), name ='logout'),

        path('dashboard', user_view.dashboard, name ='dashboard'),
        path('user/update', user_view.update, name ='update'),
        path('user/instances/', user_view.open_requests, name ='open_requests'),
        path('user/notification', user_view.notification, name ='notification'),

        path('user/requests/', user_view.requested_services, name ='requested_services'),
        path('user/requested_jobs/delete/<int:job_id>', user_view.delete_requested_jobs, name ='delete_requested_jobs'),
        path('user/requested_freelancers/delete/<int:task_id>', user_view.delete_requested_freelancers, name ='delete_requested_freelancers'),

        path('services/', user_view.services, name ='services'),
        path('services/ask', user_view.ask_for_service, name ='ask_for_service'),
        path('services/offer', user_view.offer_a_service, name ='offer_a_service'),

        path('browse/apply/<slug:user>/<int:job_id>/<slug:job_title>', user_view.apply_for_job, name ='apply_for_job'),
        path('browse/hire/<slug:user>/<int:task_id>/<slug:task_title>', user_view.hire_a_freelancer, name ='hire_a_freelancer'),
 
        path('browse/local/jobs', user_view.browse_local_jobs, name ='browse_local_jobs'),
        path('browse/local/freelancers', user_view.browse_local_freelancers, name ='browse_local_freelancers'),
        path('browse/global/jobs', user_view.browse_global_jobs, name ='browse_global_jobs'),
        path('browse/global/freelancers', user_view.browse_global_freelancers, name ='browse_global_freelancers'),


        path('user/instances/update/ask/<int:i_id>', user_view.update_asked_services, name ='update_asked_services'),
        path('user/instances/delete/ask/<int:i_id>', user_view.delete_asked_services, name ='delete_asked_services'),
        path('user/instances/update/bid/<int:i_id>', user_view.update_offered_services, name ='update_offered_services'),
        path('user/instances/delete/bid/<int:i_id>', user_view.delete_offered_services, name ='delete_offered_services'),
]