from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy

class ThanksPage(TemplateView):
    template_name = 'thanks.html'    

class HomePage(TemplateView):
    template_name = "index.html"

class ContactPage(TemplateView):
    template_name = "contact.html"

class RegulationsPage(TemplateView):
    template_name = "regulations.html"

class NoPermsPage(TemplateView):
    template_name = "no_perms.html"

