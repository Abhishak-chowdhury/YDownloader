from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
import random,string
from pytube import YouTube
from myapp.models import DownloadedVideos
from django.contrib.auth import authenticate,login as login_details,logout as logout_details
from django.contrib.auth.decorators import login_required
# Create your views here.
def Home(request):
    return render(request,'index.html')

def Signup(request):
    if request.method == 'POST':
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        Email = request.POST.get('email')
        Password = request.POST.get('password')
        Confirm_Password = request.POST.get('re-password')
        try:
            if User.objects.filter(email = Email).first():
                messages.warning(request, "Email is already exists,please go to signin")
                return redirect('login')
            
            if Password != Confirm_Password:
                messages.warning(request, "please check your confirm password")
                return redirect('signup')
            str_characters = string.ascii_lowercase + string.digits
            username = ''.join(random.choices(str_characters, k=5))  
            user_obj=User(username=firstname+'_'+username,first_name=firstname,last_name=lastname,email=Email)
            user_obj.set_password(Password)
            print(user_obj)
            user_obj.save()
            messages.success(request, "sucessfully registered and continue to sign in process")
            return redirect('login')
            
        except Exception as e:
            print(e)

    return render(request,'register.html')

def Signin(request):
    if request.method == 'POST':
        Email = request.POST.get('email')
        Password = request.POST.get('password')
        try:
            obj = User.objects.get(email=Email)
        
            username=obj.username
            print(username)
            user = authenticate(request,email = Email ,password = Password,username=username)
            print(user)
            if user is not None:
                login_details(request, user)
                messages.success(request,f"sucessfully registered {Email}")
                return redirect('dashboard')
            else:
                messages.warning(request,"password is incorrect")
                return redirect('login')
        except Exception as e:
            print(e)
            messages.warning(request,"login details are incorrect")
            return redirect('login')
    
    return render(request,'user-login.html')

@login_required(login_url='login')
def Dashboard(request):
    return render(request,'dashboard.html')
@login_required(login_url='login')
def Download_Video(request):
    contex={}
    if request.method == 'POST':
        try:
            url=str(request.POST.get('url'))
            embeded_link=url.replace("watch?v=","embed/")
            print(embeded_link)
            print(url)
            yt = YouTube(url)
            embeded_title=yt.title
            video_resolutions=[]
            video_resolutions= yt.streams.filter(progressive=True).all()
            
            print(video_resolutions)
            contex={
                'embeded_link':embeded_link,
                'embeded_title':embeded_title,
                'video_resolutions':video_resolutions,
                'url':url,
                'is_valid_url':True
            }
        except Exception as e:
            print(e)
            contex['is_valid_url']=False
    return render(request,'download.html',contex)
@login_required(login_url='login')
def download_vid(request):
    if request.method == 'POST':
        res=request.POST.get('res')
        url=request.POST.get('url')
        yt = YouTube(url)
        video_title=yt.title
        video_thumbnali=yt.thumbnail_url
        video_download= yt.streams.filter(progressive=True,res=res).first()
        video_download.download("C:\Downloads")
        DownloadedVideos.objects.create(user=request.user,video_title=video_title,video_url=url,video_thumbnali=video_thumbnali)
        return redirect('success')
@login_required(login_url='login')    
def success(request):
    return render(request,'success.html')
@login_required(login_url='login')
def logout(request):
    logout_details(request)
    messages.success(request,'thank you for spending some moments')
    return redirect('login')
@login_required(login_url='login')
def History(request):
    download_objects=DownloadedVideos.objects.all()
    return render(request,'history.html',{'download_objects':download_objects})