from django.shortcuts import render

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Student, Student_Profile, Program, CohortGroup


# we want to learn about django template instead of using httpresponse we can return our html
# def home(request):
#   student_list = Student.objects.all()  # Retrieve all students
  
#   # Create a dictionary to store each student's cohort group(s)
#   student_cohort_groups = {student.cohort_groups.all() for student in student_list}
  
#   context = {
#       "students": student_list,
#       "student_cohort_groups": student_cohort_groups  # Pass the student-cohort mapping
#   }
#   print(student_cohort_groups)
#   return render(request, 'html/index.html', context)

def home(request):
  student_list = Student.objects.all()  # Retrieve all students

  paginator = Paginator(student_list, 5)  # 10 students per page

  page_number = request.GET.get('page') # is used to retrieve the value of the page parameter from the URL query string
  try:
    students_page = paginator.page(page_number)
  except PageNotAnInteger:
    students_page = paginator.page(1)
  except EmptyPage:
    students_page = paginator.page(paginator.num_pages)
  
  # Attach cohort groups to each student object as a custom attribute which can also be done on the template
  for student in students_page:
    student.cohort_groups_list = student.cohort_groups.all()
  
  context = {
    #"students": student_list, # Now, each student has an attribute 'cohort_groups_list'
    "students_page": students_page
  }
  
  return render(request, 'html/index.html', context)



def school(request):
  return HttpResponse('we are going for studies')

# we learnt about dynamic routing in django here

# def dynamic(request, unique):
# #    return HttpResponse(f"<h1>This is {unique}'s profile page</h1>")
#    return render(request, 'html/profile.html', {'profile': unique})

def profile_view(request, slug):
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
    slug=slug
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
    'cohort_group': cohort_group,
    "cohort_members": cohort_members,
  }
  return render(request, 'html/profile.html', context)


# Create your views here.


def update_student(request):
  if request.method == 'POST':
    profile_picture = request.FILES['profileImage']
    first_name = request.POST['firstName']
    email = request.POST.get('email')
    last_name = request.POST['lastName']
    address = request.POST['address']
    name = request.POST['cohort']
    courses = request.POST['program']
    status = request.POST.get('status') == 'true'
    date_join = request.POST['dateJoined']
    rating = request.POST['rating']
    date_of_birth = request.POST['dob']
    bio = request.POST['bio']


    # Create the Student instance and save it first
    student = Student(first_name=first_name, last_name=last_name, email=email, status=status)
    student.save()

    # Associate the Student_Profile with the Student
    student_profile = Student_Profile(
      student=student,  # Link the Student_Profile to Student
      profile_picture=profile_picture,
      date_join=date_join,
      rating=rating,
      address=address,
      date_of_birth=date_of_birth,
      bio = bio
    )
    student_profile.save()

    # Associate the Program with the Student
    program = Program(
        student=student,  # Link the Program to Student
        courses=courses
    )
    program.save()

    # Create the CohortGroup and associate it with the Student
    cohort, created = CohortGroup.objects.get_or_create(name=name)
    cohort.students.add(student)  # Add the student to the cohort

    return redirect('home')

  return render(request, 'html/index.html')


def delete(request, id):
  student = get_object_or_404(Student, pk=id)
  student.delete()

  return redirect('home')

  return render(request, 'html/index.html')

