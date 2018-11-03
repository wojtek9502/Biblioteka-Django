from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse_lazy
from django.views.generic import CreateView, TemplateView

from library_app import models
from accounts import forms

# Create your views here.
def register(request):

    registered = False

    if request.method == "POST":
        user_form = forms.UserCreateForm(data=request.POST)
        profile_form = forms.ProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.is_active = False #na poczatku user jest nieaktywny
            user.save()
            profile = profile_form.save(commit=False)
            
            # w modelu profile jest pole user z relacja 1do1 wiec uzupelniamy je
            profile.user = user
            profile.save()

            registered = True
            return redirect('accounts:after_signup')
        else:
            print(user_form.errors, profile_form.errors)

    else:  # jesli nie przeslemy nic w formularzu
        user_form = forms.UserCreateForm()
        profile_form = forms.ProfileForm()

    return render(request, 'accounts/signup.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})


class AfterRegisterPage(TemplateView):
    template_name = "accounts/after_signup.html"
