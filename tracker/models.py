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


class LostItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_lost = models.DateField()
    location = models.CharField(max_length=255)
    posted_by_id = models.CharField(max_length=20)
    posted_by_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} (Lost by {self.posted_by_name})"


class FoundItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_found = models.DateField()
    location = models.CharField(max_length=255)
    posted_by_id = models.CharField(max_length=20)
    posted_by_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} (Found by {self.posted_by_name})"


class LostItemImage(models.Model):
    lost_item = models.ForeignKey(LostItem, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='lost_items/')

    def __str__(self):
        return f"Image for {self.lost_item.name}"
