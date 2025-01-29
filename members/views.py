from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm
from django.contrib.auth import get_user_model
from django_email_verification import send_email, send_password
from django.views.generic.edit import FormView
from django_email_verification import send_email
from django.views import generic
from django.contrib.auth.models import User
from aiecobe.models import *

class CreateAccountClassView(FormView):

    def form_valid(self, form):
        user = form.save()
        return_val = super(CreateAccountClassView, self).form_valid(form)
        send_email(user)
        return return_val
    

def homeai(request):
    if not request.user.is_authenticated:
        messages.success(request,("You need to be loged-in to access... Register if you don't have an account yet !"))
        return redirect('login')
    else:
        return render(request, 'authenticate/homeai.html', {})

def logout_view(request):
    logout(request)
    messages.success(request,("Vous êtes bien déconnecté !"))
    return redirect('index')
  

def login_user(request):
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if len(User.objects.get(username=request.user.username).project_set.all()) == 0:
                messages.success(request,("Bienvenue ! Vous n'avez pas encore de projet..."))
                
                return redirect('homeai')
            else:
#                projects = User.objects.get(username=request.user.username).project_set.all()
#                projects_studies = []
#                for project in projects:
#                    studies = project.etude_set.all()
#                    if len(studies.filter(name="Incendie")) == 0:
#                        Incendie = False
#                        ThreadIncendie = ""
#                        AssIncendie = ""
##                    else:
#                        Incendie = True
#                        ThreadIncendie = studies.filter(name="Incendie")[-1].thread_id
#                        AssIncendie = studies.filter(name="Incendie")[-1].assistant_id
#                    if len(studies.filter(name="ICPE")) == 0:
#                        ICPE = False
#                        ThreadICPE = ""
#                        AssICPE = ""
#                    else:
#                        ICPE = True
#                        ThreadICPE = studies.filter(name="ICPE")[-1].thread_id
#                        AssICPE = studies.filter(name="ICPE")[-1].assistant_id
#                    projects_studies.append({"project" : project, "Incendie" : Incendie, "ThreadIncendie":ThreadIncendie, "ICPE" : ICPE, "ThreadICPE":ThreadICPE, "AssIncendie" : AssIncendie, "AssICPE" : AssICPE})
#                return render(request, 'console.html', {"projects_studies" : projects_studies})
            # Redirect to a success page.
             return redirect('homeai') 
        else:
            messages.success(request,("Error during login. Try again..."))
            return redirect('login') 
    else:
        # Return an 'invalid login' error message.
        return render(request, 'authenticate/login.html', {})


def register_user(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            #form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            email = form.cleaned_data['email']
            user = get_user_model().objects.filter(email=email)
            if len(user) != 0:
                form = RegisterUserForm()
                messages.success(request, (f"Cette adresse mail est déjà prise...{user}"))
                return render(request, 'authenticate/register_user.html',{
                        'form':form
                        })
            else:
                user = get_user_model().objects.create(username=username, password=password, email=email)
                user.is_active = False  # Example
                #send_email(user)
                messages.success(request, ("Veuillez acceder à votre boite mail pour valider le compte"))
                form = RegisterUserForm()
                return render(request, 'authenticate/register_user.html',{
                        'form':form
                        })
        else:
            #form = RegisterUserForm()
            messages.success(request, (form.errors))
            return render(request, 'authenticate/register_user.html',{
                    'form':form
                })
    else:
        form = RegisterUserForm()

        return render(request, 'authenticate/register_user.html',{
                'form':form
            })
            

def password(request):
    if request.method == 'POST':
            email = request.POST["email"]
            user = get_user_model().objects.filter(email=email)
            if len(user) != 0:
                send_password(user)
                messages.success(request, ("Veuillez acceder à votre boite mail pour créer un nouveau mot de passe"))
                return render(request, 'authenticate/password.html', {})
            else:
                messages.success(request, ("Il n'y a pas de compte avec cette adresse mail"))
                return render(request, 'authenticate/password.html', {})
    else:
        return render(request, 'authenticate/password.html', {})
  