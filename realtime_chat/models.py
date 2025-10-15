from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    @property
    def is_online(self):
        if self.last_seen:
            from datetime import timedelta
            return timezone.now() - self.last_seen <= timedelta(seconds=10)  # active last 10 sec
        return False

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:20]}"

# # Optional: User last_seen
# class UserStatus(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     last_seen = models.DateTimeField(default=timezone.now)

#     def is_online(self):
#         # User ko online maante hain agar 10 sec me request ayi ho
#         return (timezone.now() - self.last_seen).total_seconds() < 10