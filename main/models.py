from django.db import models
from django.contrib.auth.models import User



# Create your models here.
'''
null=True
blank=True
default="SAMPLE"


- user1 - first_name - usernaame- asdasdas
- user2
'''

class UserData(models.Model):
    Name=models.CharField(max_length=100)
    # In choices the left one is actual value, right one is display value. The display value is what we see
    # IN the admin page.
    Gender=models.CharField(max_length=32,choices=[('M','Male'),('F','Female'),('NA','NA')])
    Age=models.IntegerField(null = True, blank=True)
    Email=models.EmailField()
    About=models.TextField()
    user_account = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return (self.Name + " | "+self.Email)
