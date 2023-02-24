from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User

from django.dispatch import receiver
from django.db.models.signals import post_save


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    shared_user = models.ForeignKey(User,related_name="+",on_delete=models.CASCADE,null=True,blank=True)
    body = models.TextField()
    image = models.ManyToManyField('Image',blank=True,related_name="images")
    shared_on = models.DateTimeField(blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User,related_name="likes",blank=True)
    tags = models.ManyToManyField('Tag',blank=True)
    
    def create_tags(self):
        for word in self.body.split():
            if (word[0] == '#'):
                tag = Tag.objects.filter(name=word[1:]).first()
                if tag:
                    self.tags.add(tag.pk)
                else:
                    tag = Tag(name=word[1:])
                    tag.save()
                    self.tags.add(tag.pk)
                    self.save()
    
    class Meta:
        ordering = ['-created_on','-shared_on']
        
    def __str__(self):
        return self.body
        
    
    def num_of_likes(self):
        return self.likes.count()
    
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User,related_name="comment_likes", blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    tags = models.ManyToManyField('Tag',blank=True)

    def create_tags(self):
        for word in self.comment.split():
            if (word[0] == '#'):
                tag = Tag.objects.filter(name=word[1:]).first()
                if tag:
                    self.tags.add(tag.pk)
                else:
                    tag = Tag(name=word[1:])
                    tag.save()
                    self.tags.add(tag.pk)
                self.save()
    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created_on').all()

    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
    
    class Meta:
        ordering = ['-created_on']

    
    def num_of_likes(self):
        return self.likes.count()
    
    def __str__(self):
        return self.comment[:20]
    
    
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    birth_date=models.DateField(null=True, blank=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    picture = models.ImageField(upload_to='uploads/profile_pictures',default="avatar.jpg",blank=True)
    followers = models.ManyToManyField(User,related_name="followers")
    
    def followers_no(self):
        return self.followers.count()    
    
    def __str__(self):
        return self.user.username
    
@receiver(post_save,sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        

class Notification(models.Model):
    notification_type = models.IntegerField()
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name="receiver")
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="from_user")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    thread = models.ForeignKey('ThreadModel', on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    date = models.DateTimeField(default=timezone.now)
    
class ThreadModel(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')

class MessageModel(models.Model):
	thread = models.ForeignKey('ThreadModel', related_name='+', on_delete=models.CASCADE, blank=True, null=True)
	sender_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	receiver_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
	body = models.CharField(max_length=1000)
	image = models.ImageField(upload_to='uploads/message_photos', blank=True, null=True)
	date = models.DateTimeField(default=timezone.now)
	is_read = models.BooleanField(default=False)
 
class Image(models.Model):
    image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True)
    
class Tag(models.Model):
    name = models.CharField(max_length=30)
    
    def __str__(self):
        return self.name
    

    