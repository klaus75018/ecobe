from django.shortcuts import render, redirect
from django.conf import settings
from django.core.mail import send_mail
from django.contrib import messages


def form1(request):
    if request.method == 'POST':
        if request.POST["useremail"] == "":
            messages.success(request,("Entrer à minima un email valide"))
        
            return redirect("form1")
        else:
            username = request.POST["username"]
            email = request.POST["useremail"] 
            tel = request.POST["telephone"]
            message = request.POST["message"]
            full_message = f"""
                Received message below from {username}, 
                ________________________


                {message}

                {email}

                {tel}
            """

            send_mail(
                subject="Received contact form submission",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.NOTIFY_EMAIL],
                fail_silently=False,
            )
            
            return redirect("success1")
    else:
        return render(request,"form1.html", {})

# Create your views here.

def success1(request):
    return render(request,"success1.html", {})

