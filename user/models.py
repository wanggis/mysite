from django.db import  models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)   #一对一关系，一个用户名对一个昵称
    nick_name = models.CharField(max_length=20,verbose_name="昵称")

    def __str__(self):
        return '<Profile: %s for %s>'  %(self.nick_name,self.user.username)


def get_nickname(self):
    if Profile.objects.filter(user =self).exists():
        profile = Profile.objects.get(user = self)
        return profile.nick_name
    else:
        return ''

def get_nickname_or_username(self):
    if Profile.objects.filter(user =self).exists():
        profile = Profile.objects.get(user = self)
        return profile.nick_name
    else:
        return self.username


def has_nickname(self):
    return Profile.objects.filter(user = self).exists()



User.get_nickname = get_nickname
User.get_nickname_or_username = get_nickname_or_username
User.has_nickname = has_nickname
