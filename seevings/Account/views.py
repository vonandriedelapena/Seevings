from django.shortcuts import redirect, render
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('../account/')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'register.html', context)

def login(request):
    return render(request, 'login.html')

@login_required
def view_account(request):
    return render(request, 'viewAccount.html')

def view_detailed(request):
    return render(request, 'viewDetailed.html')

def add_account(request):
    return render(request, 'addAccount.html')

def update_account(request):
    return render(request, 'updateAccount.html')

def close_account(request):
    return render(request, 'closeAccount.html')

def view_user(request):
    return render(request, 'viewUser.html')