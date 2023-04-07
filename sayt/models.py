from django.db import models
from django.utils.text import slugify


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=128)
    key = models.SlugField(max_length=128, blank=True)
    is_menu = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = slugify(self.name)
        return super(Category, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class new(models.Model):
    titel = models.CharField(max_length=128)
    short_desc = models.CharField(max_length=512)
    desc = models.TextField()
    img = models.ImageField(upload_to="images")
    date = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)
    views = models.IntegerField(default=0)
    ctg = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.titel


class Comment(models.Model):
    new = models.ForeignKey(new, on_delete=models.CASCADE)
    author = models.CharField(max_length=128)
    izoh = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.author


class Contact(models.Model):
    name = models.CharField(max_length=25)
    phone = models.CharField(max_length=18)
    msg = models.TextField()

    def __str__(self):
        return self.name

