from django.db import models
from django.utils.crypto import get_random_string

class Student(models.Model):
    registration_number = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=50)
    middle_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    course = models.CharField(max_length=10)

    def __str__(self):
        return self.registration_number

        return self.name
    
class Equipment(models.Model):
    name = models.CharField(max_length=100)
    tag = models.CharField(max_length=100, unique=True)
    model_number = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Check if the tag value already exists
        if Equipment.objects.filter(tag=self.tag).exists():
            # Generate a new unique tag value
            while True:
                new_tag = get_random_string(length=10)
                if not Equipment.objects.filter(tag=new_tag).exists():
                    self.tag = new_tag
                    break

        super().save(*args, **kwargs)


class Borrowing(models.Model):
    equipment = models.ManyToManyField(Equipment)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    borrowed_date = models.DateTimeField(auto_now_add=True)
    returned_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Borrowing by {self.student}'

class RFID(models.Model):
    tag = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag
    
class Arduino_COM(models.Model):
    COM = models.CharField(max_length=100)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.COM
