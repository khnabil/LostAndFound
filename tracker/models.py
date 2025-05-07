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



from django.db import models

class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    date_reported = models.DateField()
    location = models.CharField(max_length=255)
    posted_by_id = models.CharField(max_length=20)
    posted_by_name = models.CharField(max_length=255)
    is_found = models.BooleanField(default=False)  # False = lost, True = found

    def __str__(self):
        status = "Found" if self.is_found else "Lost"
        return f"{self.name} ({status} by {self.posted_by_name})"


class ItemImage(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='items/')

    def __str__(self):
        return f"Image for {self.item.name}"

