from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from .models import User


# Create your views here.
def index(request):
    return render(request, "WakeUpApp/index.html")

def login_view(request):
    if request.method == "POST":

        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "WakeUpApp/login.html", {
                "loginError": "Username Or Password Is Incorrect"
            })
    else: 
        return render(request, "WakeUpApp/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]

        # ensure password matches confirmation
        password = request.POST["password"]

        try: 
            user = User.objects.create_user(username, password)
            user.save()
        except:
            return render(request, "WakeUpApp/register.html", {
                "registerError": "Username Already Exists"
            })
        
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "WakeUpApp/register.html")
    
def completedTasks(request):
    return render(request, "WakeUpApp/completedTasks.html")

def notifications(request):
    return render(request, "WakeUpApp/notifications.html")

def favourites(request):
    return render(request, "WakeUpApp/favourites.html")

def settings(request):
    return render(request, "WakeUpApp/settings.html")
