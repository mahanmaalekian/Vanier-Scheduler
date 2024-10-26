import json
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q


 # Create your views here.


def index(request):
     print("in index")
     if "exams" not in request.session:
          request.session["exams"] = []

     return render(request, "scheduler/index.html")

def search(request):
     queried = False
     query = request.POST.get('q')
     exams = []
     if query:
          queried=True
          query = query.upper()
          exams = Exam.objects.filter(Q(course_id__icontains=query) | Q(description__icontains=query))
          exam_list = list(exams.values())
          print(exam_list)
     print(exams)
     return render(request, "scheduler/search.html", {
          "exams": exams,
          "queried": queried
     })

def calendar(request):
     return render(request, "scheduler/calendar.html", {
          "exams": request.session["exams"],
     })

def contact(request):
     return render(request, "scheduler/contact.html")

def add_to_calendar(request):
     print("hi")

     if request.method != "PUT":
          return JsonResponse({"error:": "PUT request required"})
     data = json.loads(request.body)
     course_id = data.get("courseId", "")
     sections = data.get("sections", "")
     
     try:
          exam = Exam.objects.get(course_id = course_id, section_id = sections)
     except Exam.DoesNotExist:
          return JsonResponse({"error": "Exam not found."}, status=404)
     #print(request.session["exams"])
     

     exam_dict = exam.to_dict()
     if any(existing_exam['course_id'] == exam_dict['course_id'] and 
           existing_exam['section_id'] == exam_dict['section_id'] for existing_exam in request.session["exams"]):
        return JsonResponse({"error": "Exam already added to calendar."}, status=409)
     if "exams" in request.session:
          print("empty list")
         # print(request.session["exams"])

     request.session["exams"] += [exam_dict]
     print("list", request.session["exams"])
     return JsonResponse({"message": "Calendar updated succesfully"}, status=200)



def remove_from_calendar(request):
     print("in remove")
     if request.method != "DELETE":
          return JsonResponse({"error:": "DELETE request required"}, status=400)
     data = json.loads(request.body)
     course_id = data.get("courseId", "")
     sections = data.get("sections", "")
     if "exams" not in request.session:
        return JsonResponse({"error": "No exams found in session."}, status=400) 
     exams = request.session["exams"]

     # Find the exam and remove it
     updated_exams = [exam for exam in exams if not (exam['course_id'] == course_id and exam['section_id'] == sections)]
     if len(updated_exams) == len(exams):
        # If no exam was removed, return an error
        return JsonResponse({"error": "Exam not found."}, status=404)
     
     request.session["exams"] = updated_exams
     request.session.modified = True  # Mark the session as modified to ensure Django saves it

     return JsonResponse({"message": "Exam removed successfully."}, status=200)

#https://dylanbeattie.net/2021/01/12/adding-events-to-google-calendar-via-a-link.html