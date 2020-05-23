from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from mdeditor.fields import MDTextField
from django.contrib import admin
from ckeditor_uploader.fields import RichTextUploadingField
from PIL import Image

# Each class is table in database
class Category(models.Model):
    name = models.CharField(max_length=100)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=300, blank=True, null=True)
    image = models.ImageField(default='default.jpg', upload_to='category_pics')
    date_created = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        super(Category, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def __str__(self):
        return self.name

class UserCategory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        r  = str(self.user)+":"+str(self.category)
        return r

class Post(models.Model):
    title = models.CharField(max_length=100)
    code = RichTextUploadingField(blank=True, null=True, config_name='special')
    date_posted = models.DateTimeField(default=timezone.now) # actual timezone function is passed
    author = models.ForeignKey(User, on_delete=models.CASCADE) # if a user is deleted, also delete their posts
    votes = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    ranking = models.IntegerField(default=0)

    def __str__(self):
        return self.title

class Response(models.Model):
    content = models.TextField(max_length=500, blank=True, null=True)
    code = RichTextUploadingField(blank=True, null=True, config_name='special')
    post = models.ForeignKey(Post, on_delete=models.CASCADE) # if a post is deleted, also delete its comments
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=timezone.now) # actual timezone function is passed
    votes = models.IntegerField(default=0)
    best = models.BooleanField(default=False)

    def __str__(self):
        return self.code

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)

class ResponseVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    response = models.ForeignKey(Response, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)
