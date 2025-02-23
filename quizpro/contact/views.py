
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']

            # Send email (modify these settings as needed)
            send_mail(
                subject=f"New Contact Form Submission from {name}",
                message=message,
                from_email=email,
                recipient_list=['pragyakhadka765@gmail.com'], 
            )

            messages.success(request, "Your message has been sent successfully!")
            return redirect("contact")

    else:
        form = ContactForm()

    return render(request, "contact.html", {"form": form})
