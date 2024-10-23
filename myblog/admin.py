from django.contrib import admin
from django.db.models.functions import Now
# Register your models here.
class Post(models.Model):
    title = models.CharField(max_length = 250)
    slug = models.SlugField(max_length = 250)
    body = models.TextField()
    publish = model.DateTimeField(default = timezone.now)
    created = models.DateTimeField(auto_now_add=true);
    def __str__(self):
        return self.title;