from django.db import models
from django.core.validators import MaxLengthValidator
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User

import datetime

OPTIONS = ((0, "Inactive"), (1, "Active"))


class Category(models.Model):
    created = models.DateTimeField(verbose_name="Created date", null=True, blank=True, auto_now_add=True)
    name = models.CharField(max_length=200)
    status = models.IntegerField(max_length=1, choices=OPTIONS, default=0)

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.name


class Article(models.Model):
    id = models.AutoField(primary_key=True)
    created = models.DateTimeField(verbose_name="Created date", null=True, blank=True, auto_now_add=True)
    last_updated = models.DateTimeField(editable=False, verbose_name="Last Updated Date", null=True, blank=True)
    name = models.CharField(max_length=200)
    status = models.IntegerField(max_length=1, choices=OPTIONS, default=0)
    file = models.FileField(upload_to='uploads/%Y/%m/%d/%H/%M/%S/')
    content = models.TextField(validators=[MaxLengthValidator(3000)])
    category = models.ForeignKey(Category, blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)

    @property
    def filename(self):
        return self.file.name.rsplit('/', 1)[-1]

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __unicode__(self):
        return self.name

@receiver(pre_save, sender=Article)
def update_edit_date(sender, instance, *args, **kwargs):
    instance.last_updated = datetime.datetime.now()