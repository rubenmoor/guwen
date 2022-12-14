from django.conf.urls import patterns, url
from django.contrib.auth.views import password_reset, password_reset_done,\
                                      password_reset_confirm, password_reset_complete

urlpatterns = patterns('auth_frontend.views',
	url(r'^login/$', 'login', name='login'),
	url(r'^logout/$', 'logout', name='logout'),
	url(r'^user_new/$', 'user_new', name='user_new'),
	url(r'^user_change_password/$', 'user_change_password', name='user_change_password'),
	url(r'^user_change_email/$', 'user_change_email', name='user_change_email'),

	url(r'^password_reset/$', password_reset, {
		'template_name': 'password_reset_form.html',
		'email_template_name': 'password_reset_email.html',
		'subject_template_name': 'password_reset_subject.txt',
	}, name='password_reset'),
	url(r'^password_reset_done/$', password_reset_done, {
		'template_name': 'password_reset_done.html'
	}, name='password_reset_done'),
	url(r'^password_reset_confirm/(?P<uidb64>\w+)/(?P<token>[\w-]+)/$', password_reset_confirm, {
		'template_name': 'password_reset_confirm.html'
	}, name='password_reset_confirm'),
	url(r'^password_reset_complete/$', password_reset_complete, {
		'template_name': 'password_reset_complete.html'
	}, name='password_reset_complete')
)
