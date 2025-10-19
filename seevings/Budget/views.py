from django.shortcuts import render

# Create your views here.
def add_budget(request):
    return render(request, 'addBudget.html')

def update_budget(request):
    return render(request, 'updateBudget.html')

def remove_budget(request):
    return render(request, 'removeBudget.html')

def budget_list(request):
    return render(request, 'budgetList.html')