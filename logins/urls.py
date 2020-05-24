from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
	url(r'^$', views.base, name='base'),
	url(r'resetpassword/$', views.resetpassword, name='resetpassword'),
	url(r'simple_upload/$', views.simple_upload, name='simple_upload'),
	url(r'updateprofile/$', views.updateprofile, name='updateprofile'),
	url(r'^signin/$', views.signin, name='signin'),
	url(r'^signup/$', views.signup, name='signup'),
	url(r'postsignin/$', views.postsignin, name='postsignin'),
	url(r'postsignup/$', views.postsignup, name='postsignup'),
	url(r'logout/$', views.logout, name='logout'),
	url(r'^profile/', views.profile, name='profile'),
	url(r'resetpassword/$', views.resetpassword, name='resetpassword'),
	url(r'simple_upload/$', views.simple_upload, name='simple_upload'),
	url(r'document_upload/$', views.document_upload, name='document_upload'),
	url(r'updateprofile/$', views.updateprofile, name='updateprofile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
