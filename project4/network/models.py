from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    writer = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return f"{self.writer} wrote {self.content}"

    def serialize(self):
        return {
            "id": self.id,
            "writerid":self.writer.id,
            "writer": self.writer.username,
            "content": self.content,
            "timestamp": self.timestamp.strftime("%b %d %Y, %I:%M %p")
        }

class Like(models.Model):
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    liked_by = models.ForeignKey("User", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.post} is liked by {self.liked_by}"
    

class Follower(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey("User", on_delete=models.CASCADE, related_name="user")

    def __str__(self):
            return f"{self.user} is following {self.following}"

    