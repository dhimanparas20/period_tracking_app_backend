from django.db import models
from django.contrib.auth.models import User

class Period(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField(blank=True,)
    end_date = models.DateField(blank=True)
    symptoms = models.CharField(max_length=100,blank=True)
    
    def __str__(self):
        return self.user.username + " : " + self.symptoms
    
    @property
    def duration(self):
        if self.start_date and self.end_date:
            return (self.end_date - self.start_date).days
        else:
            return None