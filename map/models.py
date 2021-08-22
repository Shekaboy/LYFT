from django.db import models
from django.contrib.auth import get_user_model
from login.models import Beaver
# Create your models here.



class Nodes(models.Model):
    node = models.CharField(max_length=10)

    def __str__(self):
        return self.node

class Edges(models.Model):
    node1 = models.ForeignKey(Nodes, on_delete=models.CASCADE, related_name='topic_nodes')
    node2 = models.ForeignKey(Nodes, on_delete=models.CASCADE)
    edge = models.CharField(max_length=10)
    distance = models.IntegerField()

    def __str__(self):
        return self.edge

class Event(models.Model):
    name = models.TextField(blank=True)
    desc = models.TextField(max_length = 300)
    picture = models.ImageField(null=True, upload_to="images/events/", help_text="Event Photo", blank=True, default="images/events/default.jpg")
    people = models.IntegerField(null=True)
    info = models.TextField(blank=True, max_length=300)
    date = models.DateField(auto_now=False)

    def __str__(self):
        return str(self.pk)

class Trip(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.OneToOneField(Beaver, related_name = "beavers", on_delete=models.CASCADE)