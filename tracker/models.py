from django.db import models

class User(models.Model):
    USER_TYPE_CHOICES = (
        (1, 'Administrator'),
        (2, 'Faculty'),
        (3, 'Student'),
    )

    user_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=128)
    department = models.CharField(max_length=100)
    user_type = models.IntegerField(choices=USER_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} ({self.get_user_type_display()})"



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

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey('LostItem', on_delete=models.CASCADE)  # or a generic Item model if unified
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Upvote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey('LostItem', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'item')  # Prevent duplicate upvotes
