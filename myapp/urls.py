
from django.urls import path
from myapp import views
urlpatterns = [
    
    path('',views.Home,name='home'),
    path('signup',views.Signup,name='signup'),
    path('login',views.Signin,name='login'),
    path('dashboard',views.Dashboard,name='dashboard'),
    path('download',views.Download_Video,name='download'),
    path('download-per-res',views.download_vid,name='download_vid'),
    path('success',views.success,name='success'),
    path('logout',views.logout,name='logout'),
    path('history',views.History,name='history'),
]