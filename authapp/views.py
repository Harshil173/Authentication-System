from django.shortcuts import redirect, render 
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def index(request):
    return render(request,'authapp/index.html')

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('index')
    else :
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username,password=password)

            if user is not None:
                login(request,user)
                return redirect('index')
            else:
                messages.info(request,"USERNAME OR PASSWORD IS INCORRECT")
                return render(request,'authapp/login.html')

        context = {}
        return render(request,'authapp/login.html',context)


def logoutUser(request):
    logout(request)
    return redirect('login')

def registration(request):
    if request.user.is_authenticated:
        return redirect('index')
    else :
        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request,"Account was successfully created for " + user)
                return redirect('login')
        context = {'form':form}
        return render(request,'authapp/register.html',context)
