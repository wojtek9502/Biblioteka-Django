from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from library_app import models
from datetime import datetime

class ThanksPage(TemplateView):
    template_name = 'thanks.html'    

class HomePage(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        borrowHistoryObj = models.BorrowHistory.objects.all()

        context["borrows_per_month_chart_data"] = self.get_borrows_per_months_data(borrowHistoryObj)
        return context

    def get_borrows_per_months_data(self, borrow_history_obj):
        months_counter = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for borrow in borrow_history_obj:
            if(str(borrow.receive_date).split('-')[0] == str(datetime.now().year)): #tylko z biezacego roku
                months_counter_index = int(str(borrow.receive_date).split('-')[1].strip('0'))-1
                months_counter[months_counter_index] +=1
        
        return months_counter


class ContactPage(TemplateView):
    template_name = "contact.html"

class RegulationsPage(TemplateView):
    template_name = "regulations.html"

class NoPermsPage(TemplateView):
    template_name = "no_perms.html"

