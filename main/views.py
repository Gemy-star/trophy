from django.shortcuts import render
from django.views.generic import TemplateView

from main.models import Category , User

class HomePageView(TemplateView):
    template_name = 'pages/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.filter(is_active=True)
        context["vendors"] = User.objects.filter(is_active=True, scope_level=User.Scope.CUSTOMER)
        return context


class PolicyPageView(TemplateView):
    template_name = 'pages/policy.html'


class RefundPageView(TemplateView):
    template_name = 'pages/refund.html'
