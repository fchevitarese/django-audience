from django.db import models
from dateutil.relativedelta import relativedelta


class Theme(models.Model):
    name = models.CharField('Theme name', max_length=150)

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=150)
    date_uploaded = models.DateField()
    views = models.PositiveIntegerField('Number of views')
    theme = models.ManyToManyField('Theme')

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     now = datetime.now()

    #    super(Video, self).save(*args, **kwargs) # Call the real save() method


class Comment(models.Model):
    is_positive = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)
    video = models.ForeignKey('Video', related_name='comments')
    comment = models.TextField('Comment')


class Thumb(models.Model):
    is_positive = models.BooleanField(default=False)
    time = models.DateTimeField(auto_now_add=True)
    video = models.ForeignKey('Video', related_name='thumbs')


