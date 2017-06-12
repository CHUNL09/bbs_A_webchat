from django.db import models
from superbbs.models import UserProfile
# Create your models here.

class WebGroup(models.Model):
    name=models.CharField(max_length=64)
    brief=models.CharField(max_length=255,null=True,blank=True)
    owner=models.ForeignKey(UserProfile)
    admins=models.ManyToManyField(UserProfile,related_name="group_admins")
    members=models.ManyToManyField(UserProfile,related_name="group_members")
    max_members=models.IntegerField(default=200)

    def __str__(self):
        return self.name

