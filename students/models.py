from django.db import models

# Create your models here.


class ClassRoom(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Student(models.Model):
    name = models.CharField(max_length=100)
    roll = models.IntegerField(unique=True)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    joined_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.roll})"



from django.utils import timezone

class Attendance(models.Model):
    STATUS_CHOICES = (
        ('P', 'Present'),
        ('A', 'Absent'),
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)

    class Meta:
        unique_together = ('student', 'date')  # one record per day

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"


class Subject(models.Model):
    name = models.CharField(max_length=100)
    max_marks = models.IntegerField(default=100)

    def __str__(self):
        return self.name
class Marks(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks_obtained = models.IntegerField()

    def grade(self):
        if self.marks_obtained >= 90:
            return "A+"
        elif self.marks_obtained >= 75:
            return "A"
        elif self.marks_obtained >= 60:
            return "B"
        elif self.marks_obtained >= 40:
            return "C"
        else:
            return "F"

    def __str__(self):
        return f"{self.student.name} - {self.subject.name}"


class Marks(models.Model):

    EXAM_TYPE_CHOICES = [
        ('Internal', 'Internal'),
        ('Semester', 'Semester'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    exam_type = models.CharField(max_length=10, choices=EXAM_TYPE_CHOICES)
    marks_obtained = models.IntegerField()
    max_marks = models.IntegerField(default=100)

    def percentage(self):
        return round((self.marks_obtained / self.max_marks) * 100, 2)

    def grade(self):
        p = self.percentage()
        if p >= 90:
            return "A+"
        elif p >= 75:
            return "A"
        elif p >= 60:
            return "B"
        elif p >= 40:
            return "C"
        else:
            return "F"

    def __str__(self):
        return f"{self.student.name} - {self.subject.name} ({self.exam_type})"


from django.contrib.auth.models import User

class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username


class Notice(models.Model):
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
