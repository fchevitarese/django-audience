from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime
from dateutil.relativedelta import relativedelta


class Theme(models.Model):
    name = models.CharField('Theme name', max_length=150)

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=150)
    date_uploaded = models.DateField()
    views = models.PositiveIntegerField('Number of views', default=0)
    theme = models.ManyToManyField('Theme', blank=True)

    def __str__(self):
        return self.title

    def get_thumbs_up(self):
        return self.thumbs.filter(is_positive=True).count()
    get_thumbs_up.short_description = 'Thumbs Up'

    def get_thumbs_down(self):
        return self.thumbs.filter(is_positive=False).count()
    get_thumbs_down.short_description = 'Thumbs Down'

    def get_comments(self):
        return self.comments.count()
    get_comments.short_description = 'Comments'

    def clean(self, *args, **kwargs):
        if not self.pk:
            if relativedelta(datetime.now(), self.date_uploaded).years > 0:
                raise ValidationError("Videos can't have more than 1 year old.")

    def save(self, *args, **kwargs):
        if not self.pk:
            if relativedelta(datetime.now(), self.date_uploaded).years > 0:
                raise ValidationError("Videos can't have more than 1 year old.")
        super(Video, self).save(*args, **kwargs)


class Comment(models.Model):
    is_positive = models.BooleanField(default=False)
    time = models.TimeField(auto_now_add=True)
    video = models.ForeignKey('Video', related_name='comments')
    comment = models.TextField('Comment')


class Thumb(models.Model):
    is_positive = models.BooleanField(default=False)
    time = models.TimeField(auto_now_add=True)
    video = models.ForeignKey('Video', related_name='thumbs')


