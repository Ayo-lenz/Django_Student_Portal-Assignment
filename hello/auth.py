from django.views.generic import View
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout

class Signup(View):
  def get(self, request):
    return render(request, 'auth/signup.html')
  
  def post(self,request):
    username = request.POST['username']
    last_name = request.POST['last_name']
    first_name = request.POST['first_name']
    email = request.POST['email']
    password = request.POST['password']
    comfirm_password = request.POST['password1']

    if password != comfirm_password:
      messages.error(request, 'password not match')
      return render(request,'auth/signup.html')


    if User.objects.filter(username=username).exists():
      messages.error(request, 'username already taken')
      return render(request,'auth/signup.html')
        # return HttpResponse('username already taken')

    user = User.objects.create_user(username=username, last_name=last_name,
            first_name=first_name, email=email, password=password )

    if user:
      messages.success(request, 'account created ')
      return redirect('home')

    
    return render(request,'auth/signup.html')
  
class Login(View):
  def get(self,request):
    return render(request,'auth/login.html')
  
    
  def post(self,request):
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request,user )
        messages.success(request, f"Login successful! welcome back {username}")
        return redirect('home')
    else:
        messages.error(request, "Invalid credentials")
        return render(request,'auth/login.html')
  




class Logout(View):
    def get(self,request):
        logout(request)
        messages.success(request, "You have been logged out successfully.")
        return redirect('login') 
    