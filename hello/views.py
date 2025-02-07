from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Student, Student_Profile, Program, CohortGroup
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages  # For user feedback
from django.contrib.auth.mixins import LoginRequiredMixin
# from .forms import StudentForm, StudentProfileForm, ProgramForm
# from django.forms import inlineformset_factory

class Home(LoginRequiredMixin, View):
  login_url = "login"
  def get(self, request):
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
      cohort_names = CohortGroup._meta.get_field('name').choices  # Dynamic cohort names
    
    context = {
      #"students": student_list, # Now, each student has an attribute 'cohort_groups_list'
      "students_page": students_page,
      "cohort_names": cohort_names
    }
    
    return render(request, 'html/index.html', context)



def school(request):
  return HttpResponse('we are going for studies')

# we learnt about dynamic routing in django here

# def dynamic(request, unique):
# #    return HttpResponse(f"<h1>This is {unique}'s profile page</h1>")
#    return render(request, 'html/profile.html', {'profile': unique})

def profile_view(request, slug):
  
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
    #date_join = request.POST['dateJoined']
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
      #date_join=date_join,
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


def update(request, id):
  student = get_object_or_404(Student, pk=id)
  program = student.program_set.all
  cohort_names = CohortGroup._meta.get_field('name').choices

  context = {
    'student': student,
    'program' : program,
    "cohort_names": cohort_names
    # 'cohort' : cohort
  }
  
  return render(request, 'html/edit.html', context)


def edit_student(request, id):
    # Fetch the Student instance to be updated
    student = get_object_or_404(Student, pk=id)
    
    if request.method == 'POST':
        # Extract form data
        profile_picture = request.FILES.get('profileImage')  # Use `get` to handle missing files gracefully
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        address = request.POST.get('address')
        cohort_name = request.POST.get('cohort', '').strip()
        program_name = request.POST.get('program')  # Assume program_name corresponds to a course name or identifier
        status = request.POST.get('status') == 'true'
        rating = request.POST.get('rating')
        date_of_birth = request.POST.get('dob')
        bio = request.POST.get('bio')

        # Update the Student instance
        student.first_name = first_name
        student.last_name = last_name
        student.email = email
        student.status = status
        student.save()

        # Update or create the associated Student_Profile
        student_profile, created = Student_Profile.objects.update_or_create(
            student=student,  # Link to the existing Student
            defaults={
                'profile_picture': profile_picture,
                'rating': rating,
                'address': address,
                'date_of_birth': date_of_birth,
                'bio': bio
            }
        )

        # Update or create the Program associated with the Student
        program, created = Program.objects.update_or_create(
            student=student,
            defaults={'courses': program_name}  # Assuming courses is a single field; adjust if needed
        )

        # Update or create the CohortGroup and associate it with the Student
        cohort, created = CohortGroup.objects.get_or_create(name=cohort_name)
        cohort.students.add(student)  # Ensure the student is added to the cohort

        return redirect('home')

    # Render the form for editing if the method is not POST
    return render(request, 'html/index.html', {'student': student})




def send_message(request):
    
    if request.method == "POST":
        # Get form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # Validate required fields
        if not name or not email or not message:
            messages.error(request, "All fields are required.")
            return redirect('profile')

        try:
            # Send email
            send_mail(
                subject=f"New Contact Message for {name}",
                message=message,
                from_email=settings.EMAIL_HOST_USER,  # Sender email
                recipient_list=[email],  # Receiver email
                fail_silently=False,
            )
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")

        student = student = Student.objects.get(email=email)

    return redirect('profile', slug=student.slug)


