from django.shortcuts import render

def goal_list_view(request):
    return render(request, 'goal_list.html')

def set_goal_view(request):
    return render(request, 'set_goal.html')

def edit_goal_view(request):
    return render(request, 'edit_goal.html')
