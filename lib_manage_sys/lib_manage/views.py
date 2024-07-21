from django.shortcuts import redirect, render

from .forms import NewUserRegForm
from django.contrib.auth import login
# Create your views here.

def loginView(request):
    return render(request,'lib_manage/index.html')

def registerView(request):
    form = NewUserRegForm()
    if request.method == "POST":
        form = NewUserRegForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("/")
    context={'form':form}
    return render(request, 'registration/register.html', context)

