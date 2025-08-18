from django.db import models

class BaseItem(models.Model):
  name = models.CharField(max_length=255, unique=True)

class UniqueItem(models.Model):
  name = models.models.CharField(max_length=50, unique=True)
  base = models.ForeignKey(BaseItem, on_delete=models.CASCADE)
  requirements = models.JSONField(default=dict, blank=True)
  stats = models.JSONField(default=dict, blank=True)
  icon_url = models.URLField(blank=True, null=True)
  flavour_text = models.TextField(blank=True, null=True)

  def __str__(self):
    return f"{self.name} ({self.base.name})"
  
