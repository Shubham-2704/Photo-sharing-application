from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class UserPhoto(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='user_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_photos', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_photos', blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.photo.name}"
    
    def like_count(self):
        return self.likes.count()

    def dislike_count(self):
        return self.dislikes.count()
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    profile_photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)

    def __str__(self):
        return self.user.username
    
class ContactForm(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField(default="abc@gmail.com")
    subject = models.CharField(max_length=300, default="Subject")
    message = models.TextField(default="Message")
    

    def __str__ (self):
        return self.name
