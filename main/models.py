from django.db import models
from django.contrib.auth.models import User



# Create your models here.
'''
null=True : Allow this field to have Null/ Empty value
blank=True : Allow this field to have an empty string ""
default="SAMPLE" : If no value is being set, use this default value while creating a new data entry


- user1 - first_name - usernaame- asdasdas
- user2
'''

class UserData(models.Model):
    # In choices the left one is actual value, right one is display value. The display value is what we see
    # IN the admin page.
    Gender=models.CharField(max_length=32,choices=[('M','Male'),('F','Female'),('NA','NA')])
    Age=models.IntegerField(null = True, blank=True)
    About=models.TextField()
    user_account = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return (self.user_account.first_name + " | "+self.user_account.email)


class PostData(models.Model):
    Title = models.CharField(max_length=200)
    Author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    Category = models.CharField(max_length=100,choices=[('Cooking','Cooking'),('Entertainment','Entertainment'),('Tech','Tech'),('News','News')])
    Body = models.TextField()
    Time = models.DateTimeField(null = True,auto_now = True)

    def __str__(self):
        try:
            return (self.Title + " by "+self.Author.username + " | "+ str(self.Time) + " | PK="+str(self.pk))
        except:
            return("Blog Post")

class CommentData(models.Model):
    Author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    Post = models.ForeignKey(PostData, on_delete=models.CASCADE)
    Name = models.CharField(max_length=100, default="Anonymous")
    Email = models.EmailField(null=True, blank=True)
    Comment = models.TextField()
    Time = models.DateTimeField(null = True,auto_now = True)

    def __str__(self):
        try:
            return ("Comment on " + self.Post.Title +" by "+ self.Name)
        except:
            return("Post Comment")    