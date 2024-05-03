from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from ckeditor.fields import RichTextField
from PIL import Image
from django.core.files import File


# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('home')


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    bio = models.TextField()
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images/profile/")
    website_url = models.CharField(max_length=255, null=True, blank=True)
    facebook_url = models.CharField(max_length=255, null=True, blank=True)
    linkedin_url = models.CharField(max_length=255, null=True, blank=True)
    github_url = models.CharField(max_length=255, null=True, blank=True)
    instagram_url = models.CharField(max_length=255, null=True, blank=True)
    twitter_url = models.CharField(max_length=255, null=True, blank=True)
    tiktok_url = models.CharField(max_length=255, null=True, blank=True)
    snapchat_url = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return str(self.user)


    def save(self, *args, **kwargs): # pt. a face resize automat cand un user face upload
        super().save()

        img = Image.open(self.profile_pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)



    def get_absolute_url(self):
        return reverse('home')


class Post(models.Model):
    title = models.CharField(max_length=255)
    header_image = models.ImageField(null=True, blank=True, upload_to="images/")
    title_tag = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = RichTextField(blank=True, null=True)
    date_posted = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=255, default='coding')
    snippet = models.CharField(max_length=255)
    likes = models.ManyToManyField(User, related_name='blog_posts')

    def total_likes(self):
        return self.likes.count()

    def save(self, *args, **kwargs):
        # Verificați dacă header_image este gol și setați imaginea implicită în loc
        if not self.header_image:
            # Setați calea către imaginea implicită
            default_image_path = 'path_to_default_image/default_image.png'
            # Încercați să deschideți și să salvați imaginea implicită
            try:
                with open(default_image_path, 'rb') as f:
                    self.header_image.save('default_image.png', File(f))
            except FileNotFoundError:
                # În cazul în care imaginea implicită nu poate fi găsită, puteți înlocui acest lucru cu o altă logică, cum ar fi alegerea unei imagini predefinite din sistem
                pass

        # Redimensionați imaginea încărcată
        super().save(*args, **kwargs)
        if self.header_image:
            img = Image.open(self.header_image.path)
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size)
                img.save(self.header_image.path)

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        return reverse('home')




class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('article-detail', kwargs={'pk': self.post.pk})

    def edit_comment_url(self):
        return reverse('edit-comment', kwargs={'pk': self.pk})

    def delete_comment_url(self):
        return reverse('delete-comment', kwargs={'pk': self.pk})


    # def __str__(self):
    #     return '%s - %s' % (self.post.title, self.name)

