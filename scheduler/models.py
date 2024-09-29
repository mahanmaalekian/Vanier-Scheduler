from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator

# Create your models here.

class Exam(models.Model):
    date = models.DateField()
    course_id = models.CharField(
        max_length=8,
        validators=[MinLengthValidator(10), MaxLengthValidator(10)]
    )
    section_id = models.CharField(max_length=10)
    description = models.CharField(max_length=64)
    teacher = models.CharField(max_length=64)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room_number = models.CharField(max_length=10)
    row=models.CharField(max_length=10, null=True)

    def __str__(self):
        return f"{self.description}: sections {self.section_id}"
        
