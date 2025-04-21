from django.db import models

class Student(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    department = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name} ({self.user_id})"


class Faculty(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    department = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name} ({self.user_id})"


class Administrator(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    department = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128)

    def __str__(self):
        return f"{self.name} ({self.user_id})"

