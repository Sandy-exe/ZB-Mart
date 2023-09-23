from django.shortcuts import render

from django.views.generic import TemplateView,ListView,DetailView, View
# Create your views here.

class Homeview(TemplateView):
    template_name = 'index.html'
    # def put(self,request):
    #     return render(request,'index.html')