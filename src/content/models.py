from django.db import models
from django.db.models.deletion import CASCADE

from user.models import User
from django.core.files.storage import FileSystemStorage

from django.utils.text import slugify
from datetime import datetime
import random
import string
fs = FileSystemStorage(location='./media/photos')

class PostManager(models.Manager):
    """Perform Queries for Post"""
    def createDraft(self, title, user, album, draft, slug):
        post_draft = self.model(
            user = User.objects.get(email=user),
            title = title,
            album = album,
            created = datetime.now(),
            slug = slug if slug else slugify(title)+''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
        )
        if draft:
            post_draft.set_published(datetime.now())
        post_draft.save(using = self._db)   
        return post_draft

    def publish_post(self,id):
            self.get(pk=id).update(published = datetime.now())
    def list_every_published_posts(self):
        return self.filter()
    def list_user_all_posts(self, useremail):
        return self.filter(user_email=useremail)
    def list_user_published_posts(self, user):
        return self

class Post(models.Model):
    """Post by User"""
    title = models.CharField(max_length=500)
    user = models.ForeignKey(User, on_delete=CASCADE)
    draft =  models.BooleanField(default = False)
    created = models.DateTimeField(auto_now_add = True, editable=False)
    published = models.DateTimeField(auto_now = True, null=True)

    objects = PostManager()

    class Meta: 
       ordering = [('-published')]
    def __str__(self):
       return self.title 

    def thumbnails(self):
            return self.images.filter(width__lt=100, length_lt=100)
    def default(self):
        return self.images.filter(default=True).first()

    def get_absolute_url(self):
        return f'/posts/{self.slug}/'
    def get_update_url(self):
        return f'/posts/{self.slug}/update/'
    def get_delete_url(self):
        return f'/posts/{self.slug}/delete/'

class Image(models.Model):
    """Upload Image Item"""
    image = models.ImageField(storage=fs)
    album = models.ForeignKey(Post, related_name='images', on_delete=models.CASCADE)
    
    def thumbnails(self):
            return self.images.filter(width__lt=100, length_lt=100)
