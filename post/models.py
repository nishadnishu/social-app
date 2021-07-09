import uuid

from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import ugettext_lazy as _

from decimal import Decimal
from versatileimagefield.fields import VersatileImageField
    

class Images(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey('post.Post', on_delete=models.CASCADE)
    post_image = VersatileImageField('Image', upload_to="posts/images")

    class Meta:
        db_table = 'posts_images'
        verbose_name = _('post image')
        verbose_name_plural = _('post images')

    def __str__(self):
        return str(self.post)
    

class Tag(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tag = models.CharField(max_length=128, unique=True)

    class Meta:
        db_table = 'post_tag'
        verbose_name = _('tag')
        verbose_name_plural = _('tags')

    def __str__(self):
        return self.tag

    def save(self, *args, **kwargs):
        super(Tag, self).save(*args, **kwargs)
        self.tag = self.tag.lower()


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    date_added = models.DateTimeField(db_index=True, auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField('post.Tag',)

    is_deleted = models.BooleanField(default=False)
    is_liked = models.BooleanField(default=False)
    is_disliked = models.BooleanField(default=False)

    class Meta:
        db_table = 'posts_post'
        verbose_name = _('post')
        verbose_name_plural = _('posts')
        ordering = ('id',)

    def __str__(self):
        return str(self.id)
