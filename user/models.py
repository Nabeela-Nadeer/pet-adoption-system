from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom User model
class User(AbstractUser):
    is_admin = models.BooleanField(default=False)  # distinguishes admin vs normal user

class Pet(models.Model):
    PET_TYPES = [('Dog','Dog'), ('Cat','Cat'), ('Bird','Bird'), ('Other','Other')]
    
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    pet_type = models.CharField(max_length=10, choices=PET_TYPES)
    breed = models.CharField(max_length=50)
    description = models.TextField()
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='pets/', null=True, blank=True)

    def __str__(self):
        return self.name

class AdoptionRequest(models.Model):
    STATUS_CHOICES = [('Pending','Pending'), ('Approved','Approved'), ('Rejected','Rejected')]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.pet.name}"
