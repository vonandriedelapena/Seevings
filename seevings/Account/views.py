from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')

def view_account(request):
    return render(request, 'viewAccount.html')

def add_account(request):
    return render(request, 'addAccount.html')

def update_account(request):
    return render(request, 'updateAccount.html')

def close_account(request):
    return render(request, 'closeAccount.html')

