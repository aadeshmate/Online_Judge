from django import views
from django.conf import settings
from django.contrib import admin
from django.urls import  path,include
from onlinejudge import views
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name='index'),
    path('addproblem',views.addproblem,name='addproblem'),
    path('showproblem',views.showproblem,name='showproblem'),
    path('problem/<int:question_id>',views.viewproblem,name='viewproblem'),
    path('problem/<int:question_id>/submitproblem',views.submitproblem,name='submitproblem'),
    path('signup',views.handleSignup,name='handlesignup'),
    path('login',views.handlelogin,name='handlelogin'),
    path('logout',views.handlelogout,name='handlelogout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)