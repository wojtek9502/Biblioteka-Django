from django.views.generic import TemplateView

class ThanksPage(TemplateView):
    template_name = 'thanks.html'    

class HomePage(TemplateView):
    template_name = "index.html"

class ContactPage(TemplateView):
    template_name = "contact.html"