# CampusSMS - Student Management Module


from django.shortcuts import render,redirect,get_object_or_404
from .forms import StudentForm
from .models import Student

from .models import Notice

def student_list(request):
    students = Student.objects.all()
    notices = Notice.objects.all().order_by('-created_at')[:5]  # latest 5

    return render(request, 'students/student_list.html', {
        'students': students,
        'notices': notices
    })


def add_student(request):
    form = StudentForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'students/add_student.html', {'form': form})

# Update student
def update_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = StudentForm(request.POST or None, request.FILES or None, instance=student)
    if form.is_valid():
        form.save()
        return redirect('student_list')
    return render(request, 'students/add_student.html', {'form': form})

# Delete student
def delete_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    student.delete()
    return redirect('student_list')

from .forms import ClassRoomForm




# Add class
def add_class(request):
    form = ClassRoomForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('add_student')  # redirect back to Add Student page
    return render(request, 'students/add_class.html', {'form': form})


from django.utils.timezone import now
from django.shortcuts import render, redirect
from .models import Student, Attendance

def mark_attendance(request):
    today = now().date()
    students = Student.objects.all()

    if request.method == 'POST':
        for student in students:
            status = request.POST.get(str(student.id))
            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    date=today,
                    defaults={'status': status}
                )
        return redirect('student_list')

    return render(request, 'students/mark_attendance.html', {
        'students': students,
        'today': today
    })
def monthly_attendance(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    current_month = now().month
    attendance_records = Attendance.objects.filter(
        student=student,
        date__month=current_month
    ).order_by('date')

    return render(request, 'students/monthly_attendance.html', {
        'student': student,
        'attendance_records': attendance_records
    })
from django.utils.timezone import now
from django.shortcuts import render, redirect
from .models import Student, Attendance, ClassRoom

def class_wise_attendance(request):
    today = now().date()
    classes = ClassRoom.objects.all()
    students = None

    if request.method == 'POST':
        class_id = request.POST.get('classroom')
        students = Student.objects.filter(classroom_id=class_id)

        for student in students:
            status = request.POST.get(str(student.id))
            if status:
                Attendance.objects.update_or_create(
                    student=student,
                    date=today,
                    defaults={'status': status}
                )

        return redirect('student_list')

    class_id = request.GET.get('classroom')
    if class_id:
        students = Student.objects.filter(classroom_id=class_id)

    return render(request, 'students/class_attendance.html', {
        'classes': classes,
        'students': students,
        'today': today
    })

from django.db.models import Count, Q
from django.utils.timezone import now

def attendance_dashboard(request):
    today = now().date()

    total_students = Student.objects.count()

    today_present = Attendance.objects.filter(
        date=today, status='P'
    ).count()

    today_absent = Attendance.objects.filter(
        date=today, status='A'
    ).count()

    total_attendance = Attendance.objects.count()
    total_present = Attendance.objects.filter(status='P').count()

    overall_percentage = (
        (total_present / total_attendance) * 100
        if total_attendance > 0 else 0
    )

    class_stats = ClassRoom.objects.annotate(
        present=Count(
            'student__attendance_records',
            filter=Q(
                student__attendance_records__date=today,
                student__attendance_records__status='P'
            )
        ),
        total=Count('student')
    )

    return render(request, 'students/attendance_dashboard.html', {
        'total_students': total_students,
        'today_present': today_present,
        'today_absent': today_absent,
        'overall_percentage': round(overall_percentage, 2),
        'class_stats': class_stats,
        'today': today
    })


from .forms import MarksForm
from .models import Marks

def add_marks(request, student_id):  # <-- Add student_id here
    student = Student.objects.get(id=student_id)  # fetch student
    if request.method == 'POST':
        form = MarksForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        # pre-fill student in the form
        form = MarksForm(initial={'student': student})

    return render(request, 'students/add_marks.html', {'form': form, 'student': student})

def student_result(request, student_id):
    marks = Marks.objects.filter(student_id=student_id)
    total = sum(m.marks_obtained for m in marks)

    return render(request, 'students/result.html', {
        'marks': marks,
        'total': total
    })
def add_subject(request):
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = SubjectForm()
    return render(request, 'students/add_subject.html', {'form': form})
from .forms import SubjectForm

from .forms import ClassRoomForm

def add_classroom(request):
    if request.method == 'POST':
        form = ClassRoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('add_student')  # go back to Add Student page
    else:
        form = ClassRoomForm()
    return render(request, 'students/add_classroom.html', {'form': form})



from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

def teacher_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('teacher_dashboard')
        else:
            return render(request, 'students/teacher_login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'students/teacher_login.html')


from django.contrib.auth.decorators import login_required

@login_required
def teacher_dashboard(request):
    return render(request, 'students/teacher_dashboard.html')


@login_required
def add_notice(request):
    if request.method == 'POST':
        Notice.objects.create(
            title=request.POST['title'],
            message=request.POST['message'],
            teacher=request.user
        )
        return redirect('view_notices')

    return render(request, 'students/add_notice.html')


def view_notices(request):
    notices = Notice.objects.all().order_by('-created_at')
    return render(request, 'students/view_notices.html', {'notices': notices})
from .models import Notice