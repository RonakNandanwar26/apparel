from django.shortcuts import render, redirect
from .forms import ContactForm
from apparel import settings
from django.core.mail import send_mail
from django.contrib import messages
from .forms import UserForm,ProfileForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def Home(request):
    try:
        template = 'Home/index.html'
        return render(request, template, {})
    except:
        return render(request, 'Home/404.html', {})


def about(request):
    template = 'Home/about.html'
    return render(request, template, {})

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST or None)
        if form.is_valid():
            contact_name = form.cleaned_data['name']
            contact_email = form.cleaned_data['email']
            sub = form.cleaned_data['subject']
            content = form.cleaned_data['message']
            # print(contact_name)
            form.save()
            subject = 'Hello ' + contact_name + ' from apparel!'
            message = 'Stay Connected. We would love to hear you!'
            email_from = settings.EMAIL_HOST_1USER
            email_to = [contact_email, ]
            send_mail(subject, message, email_from, email_to)
            messages.success(request, 'Form submitted successfully.')
            return redirect('Home:Home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = ContactForm()
    template = 'Home/contact.html'
    return render(request, template, {'form': form})



# def profile(request):
#     template = 'Home/profile.html'
#     return render(request, template, {})

def profile(request):
    template = 'Home/profile.html'
    if request.method == 'POST':
        user_form = UserForm(request.POST or None, request.FILES or None, instance=request.user)
        profile_form = ProfileForm(request.POST or None, request.FILES or None, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your Profile is Updated Successfully..")
            return redirect('Home:Home')
        else:
            messages.error(request, 'Please Correct the error below')
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    return render(request, template, {'user_form': user_form,
                                      'profile_form': profile_form})