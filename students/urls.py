from django.urls import path
from .views import student_list
from . import views
urlpatterns =[
    path('', student_list, name='student_list'),
    path('classroom/add/', views.add_classroom, name='add_classroom'),
    path('add/', views.add_student, name='add_student'),
    path('update/<int:pk>/', views.update_student, name='update_student'),
    path('delete/<int:pk>/', views.delete_student, name='delete_student'),
    path('add-class/', views.add_class, name='add_class'), 
    path(
    'attendance/<int:student_id>/',
    views.monthly_attendance,
    name='monthly_attendance'
    ),
    path('attendance/mark/', views.mark_attendance, name='mark_attendance'),
    path('attendance/class/', views.class_wise_attendance, name='class_attendance'),
    path('attendance/dashboard/', views.attendance_dashboard, name='attendance_dashboard'),
    path('marks/add/<int:student_id>/', views.add_marks, name='add_marks'),
    path('result/<int:student_id>/', views.student_result, name='student_result'),
    path('subject/add/', views.add_subject, name='add_subject'),
    path('teacher/login/', views.teacher_login, name='teacher_login'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    # Notices
    path('notice/add/', views.add_notice, name='add_notice'),
    path('notices/', views.view_notices, name='view_notices'),
]


