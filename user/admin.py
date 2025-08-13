from django.contrib import admin
from .models import User, Pet, AdoptionRequest

admin.site.register(User)
admin.site.register(Pet)
admin.site.register(AdoptionRequest)
