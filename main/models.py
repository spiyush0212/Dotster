from django.db import models
from django.forms import ModelForm

# Create your models here.

class Application(models.Model):
    _id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    docker_image_url = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        "auth.User", related_name="applications", on_delete=models.CASCADE
    )
    num_replicas_min = models.IntegerField()
    num_replicas_max = models.IntegerField()
    current_instances = models.IntegerField()
    port = models.TextField()
    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]


class AppForm(ModelForm):
    class Meta:
        model = Application
        fields = ["name", "description", "docker_image_url", "num_replicas_min", "num_replicas_max", "port"]
