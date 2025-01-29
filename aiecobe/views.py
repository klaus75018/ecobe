from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
# Create your views here.
import openai
from django.contrib.auth.models import User
from aiecobe.models import *
from aiecobe.functions.tool1_functions import *
from aiecobe.functions.start_functions import *
from aiecobe.functions.Conversation_functions import *
from aiecobe.forms import NewProjectForm


client = openai.OpenAI()

assistant_id = "asst_sKKdVZkeKneOYbCtcb8tnL3J"
thread = client.beta.threads.create()
thread_id = thread.id
vs_id = "vs_YUuSw6fikktYVFeoDjTcIVOc"

def remarks(request):
    if not request.user.is_authenticated:
        messages.success(request,("You need to be loged-in to access... Register if you don't have an account yet !"))
        return redirect('login')
    else:
        if request.method == 'POST':
           print("POST")
           return redirect('dashboard')
        else:
            return render(request, 'remarks.html', {})

def dashboard(request):
    if not request.user.is_authenticated:
        messages.success(request,("You need to be loged-in to access... Register if you don't have an account yet !"))
        return redirect('login')
    else:
        if request.method == 'POST':
            print("ET CA POST________________________________________________POST")
            project_name = request.POST["project_name"]
            print(f"ET CA POST2________________________________________________{project_name}")
            if "Incendie" in request.POST:
                print(f"ET CA POST3________________________________________________{project_name}")
                return redirect('incendie', project_name=project_name)
        else:
            projects = User.objects.get(username=request.user.username).project_set.all()
            incendie_studies = []
            for project in projects:
                if len(project.etude_set.filter(name="Incendie")) != 0:
                    incendie_studies.append(project.etude_set.get(name="Incendie"))

            return render(request, 'dashboard.html', {"projects":projects, "incendie_studies":incendie_studies})


def incendie(request, project_name):
    if not request.user.is_authenticated:
        messages.success(request,("You need to be loged-in to access... Register if you don't have an account yet !"))
        return redirect('login')
    else:
        print(f".............................{request.user.project_set.get(name=project_name).etude_set.get(name='Incendie').thread_id}")
        thread_id=request.user.project_set.get(name=project_name).etude_set.get(name="Incendie").thread_id
        assistant_id=request.user.project_set.get(name=project_name).etude_set.get(name="Incendie").assistant_id
        
        
        if request.method == 'POST':
            user_message = request.POST["user_message"]

 #           message = client.beta.threads.messages.create(
  #               thread_id=thread_id,
   #              role="user",
    #             content=user_message,
    #        )
#            run = client.beta.threads.runs.create_and_poll(
 #               thread_id=thread_id, assistant_id=assistant_id
#
#            )
#            ai_messages = list(client.beta.threads.messages.list(thread_id=thread_id, run_id=run.id))
#            message_content = ai_messages[0].content[0].text

#
            run_id = newMessage(user_message, client=client, thread_id=thread_id, assistant_id=assistant_id)
            
            response = wait_for_run_completion(client=client, thread_id=thread_id, run_id=run_id, username = request.user.username, project_name=project_name)
                
            messages.success(request,(f"REPONSE : \n\n {response}\n\n{thread_id}"))
            return redirect('incendie',project_name=project_name) 
        else:

            
            return render(request, 'conversations/incendie.html', {"project_name":project_name})

def initiate_new_project(request):
    if not request.user.is_authenticated:
        messages.success(request,("You need to be loged-in to access... Register if you don't have an account yet !"))
        return redirect('login')
    
    else:
        if request.method == 'POST':
            project_name = request.POST["project_name"]
            study_type = request.POST["study_type"]
            print(f"............etLAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA.................{study_type}")
            if len(User.objects.get(username=request.user.username).project_set.filter(name = project_name)) != 0:
                print(f".............................{study_type}")
                if len(User.objects.get(username=request.user.username).project_set.get(name = project_name).etude_set.filter(name = study_type)) != 0:
                    print(f".............................{study_type}")
                    messages.success(request,("Cette étude existe déjà pour ce projet"))
                    return redirect('initiate_new_project')
                else:
                    if study_type != "Incendie":
                        messages.success(request,("Study type MUST be 'Incendie'"))
                        return redirect('initiate_new_project')
                    else:
                        thread_id = initialize(request.user.username, study_type, project_name)
                        e = Project.objects.get(name=project_name).etude_set.get(name=study_type)
                        e.thread_id = thread_id
                        e.save()
                        print(f".............................{project_name}")
                        return redirect('incendie', project_name=project_name)
            else:
                if study_type != "Incendie":
                    messages.success(request,("Study type MUST be 'Incendie'"))
                    return redirect('initiate_new_project')
                else:
                    thread_id = initialize(request.user.username, study_type, project_name)
                    e = Project.objects.get(name=project_name).etude_set.get(name=study_type)
                    e.thread_id = thread_id
                    e.save()
                    print(f".............................{project_name}")
                    return redirect('incendie', project_name=project_name)
        else:

            return render(request, 'initiate_new_project.html', {"form" : NewProjectForm})