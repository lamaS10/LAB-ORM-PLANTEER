from django.shortcuts import render , redirect
from plants.models import Plant
from django.db.models import Count
from .forms import ContactForm
from .models import Contact
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages



# Create your views here.

def home_view(request):

    plants = Plant.objects.order_by('-id').annotate(review_count=Count("review"))[:3]

    return render(request,'main/home.html',{'plants':plants})
def contact_page_view(request):

    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            contact = form.save()   

            full_name = f"{contact.first_name} {contact.last_name}"

            content_html = render_to_string(
                "main/mail/confirmation.html",
                {"name": full_name}
            )

            email_message = EmailMessage(
                subject="Thank you for contacting us! 🌿",
                body=content_html,
                from_email=settings.EMAIL_HOST_USER,
                to=[contact.email]
            )
            email_message.content_subtype = "html"
            email_message.send()

            messages.success(request, "Your message has been received. Thank you!", "alert-success")
            return redirect("main:contact_page_view")

    else:
        form = ContactForm()

    return render(request, "main/contact.html", {"form": form})



def messages_page_view(request):
    messages = Contact.objects.all().order_by('-created_at')
    count = messages.count()   
    return render(request, 'main/messages.html', {
        'messages': messages,
        'count': count
    })

