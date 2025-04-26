from django.shortcuts import render
from django.views.generic import TemplateView

from main.models import HomeSlider

class HomePageView(TemplateView):
    template_name = 'pages/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sliders"] = HomeSlider.objects.filter(is_active=True)
        return context
