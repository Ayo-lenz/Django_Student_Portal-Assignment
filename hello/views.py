from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Student, Student_Profile, Program, CohortGroup


# we want to learn about django template instead of using httpresponse we can return our html
def home(request):
  student_list = Student.objects.all()
  context = {
    "students": student_list
  }
  return render(request, 'html/index.html', context)


def school(request):
  return HttpResponse('we are going for studies')

# we learnt about dynamic routing in django here

# def dynamic(request, unique):
# #    return HttpResponse(f"<h1>This is {unique}'s profile page</h1>")
#    return render(request, 'html/profile.html', {'profile': unique})

def profile_view(request, id):
  # profile = username  # or fetch profile from the database
  # if len(profile) < 6:
  #     profile_exists = False
  # else:
  #     profile_exists = True

  # context = {
  #     'profile': profile,
  #     'profile_exists': profile_exists,
  # }

 
    # Use prefetch_related for the reverse relationship, assuming `related_name='cohort_groups'`
  student = get_object_or_404(
    Student.objects.prefetch_related('cohort_groups'),  # Adjust based on the actual related_name
    id=id
  )

  # Retrieve the first cohort group if it exists
  cohort_group = student.cohort_groups.first()

  if cohort_group:
      # Filter students that are in the same cohort group
    cohort_members = Student.objects.filter(
        cohort_groups=cohort_group
    ).prefetch_related('cohort_groups')  # Adjust for reverse relationship if necessary
  else:
      cohort_members = Student.objects.none()

  # Pass the data to the template
  context = {
    "student": student,
    "cohort_members": cohort_members,
  }
  return render(request, 'html/profile.html', context)


# Create your views here.
