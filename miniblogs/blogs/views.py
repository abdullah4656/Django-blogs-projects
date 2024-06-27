
from django.contrib import messages
from django.shortcuts import redirect, render
from blogs.forms import signup,userlogin,Postform
from django.contrib.auth import login,authenticate,logout
from blogs.models import Post
from django.contrib.auth.models import Group
# Create your views here.
#Home
def home(request):
    post=Post.objects.all()
    return render(request,'blogstemp/home.html',{'post':post})
#about
def about(request):
      return render(request,'blogstemp/about.html')
#contact
def contact(request):
      return render(request,'blogstemp/contactpage.html')
#Dashboard
def Dashboard(request):
      if request.user.is_authenticated:
       posts=Post.objects.all()
       user=request.user
       fullname=user.get_full_name()
       gps=user.groups.all()
       return render(request,'blogstemp/Dashboard.html',{'posts':posts,'fullname':fullname,'gps':gps})
      else:
          return redirect('user_login')
#login
def user_login(request):
     if not request.user.is_authenticated:
      if request.method=='POST':
           form=userlogin(request=request,data=request.POST)
           if form.is_valid():
                uname=form.cleaned_data.get('username')
                upass=form.cleaned_data.get('password')
                user=authenticate(username=uname,password=upass)
                if user is not None:
                 login(request,user)
                messages.success(request,'logged in successfully')
                return redirect('dashboard')
      else:
           form=userlogin()
      return render(request,'blogstemp/login.html',{'form':form})
     else:
         return redirect('dashboard')
#signup
def user_signup(request):
      if request.method=='POST':
       form=signup(request.POST)
       if form.is_valid():
            user= form.save()
            group=Group.objects.get(name='Author')
            user.groups.add(group)
            messages.success(request,"signed up Successfully")
            return redirect('user_login')
      else:
           form=signup()
      return render(request,'blogstemp/signup.html',{'form':form})
#logout
def user_logout(request):

       logout(request)
       return redirect('home')
#AddPost
def add_post(request):
  if request.user.is_authenticated:
      if request.method=='POST':
          form=Postform(request.POST)
          if form.is_valid():
              title=form.cleaned_data.get('title')
              desc=form.cleaned_data.get('desc')
              pst=Post(title=title,desc=desc)
              pst.save()
      else:
          form=Postform()         
      return render(request,'blogstemp/addpost.html',{'form':form})
  else:
      return redirect('login')
  #updatePost
def update_post(request,id):
  if request.user.is_authenticated:
      if request.method=='POST':
          pi=Post.objects.get(pk=id)
          form=Postform(request.POST,instance=pi)
          if form.is_valid():
              form.save()
      else:
          pi=Post.objects.get(pk=id)
          form=Postform(instance=pi)
      return render(request,'blogstemp/updatepost.html',{'form':form})
  else:
      return redirect('login')
#deletePost
def delete_post(request,id):
  if request.user.is_authenticated:
       if request.method=='POST':
          pi=Post.objects.get(pk=id)
          pi.delete()
          return redirect('dashboard')
  else:
      return redirect('login')