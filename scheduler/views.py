import json
from django.shortcuts import render
from django.http import HttpResponse
from .models import *

 # Create your views here.

searched_courses = []

def index(request):
     return render(request, "scheduler/index.html")

def search(request):
     query = request.POST.get('q')
     exams = []
     courses = Exam.objects.values_list('course_id', flat=True)
     if query:
          query = query.upper()
          if query in courses:
               exam = Exam.objects.filter(course_id = query)
               exams.append(exam)
          else:
               exams = Exam.objects.filter(course_id__icontains=query)
     print(exams)
     return render(request, "scheduler/search.html", {
          "exams": exams
     })

