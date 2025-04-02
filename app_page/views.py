from django.shortcuts import render
from django.views.generic import TemplateView


class InfoTemplateView(TemplateView):
    template_name = 'index.html'