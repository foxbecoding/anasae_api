from django.db import models

class Slider(models.Model):
    name = models.CharField(max_length=30, blank=False, default='')
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class SliderImage(models.Model):
    slider = models.ForeignKey(Slider, on_delete=models.CASCADE, related_name="images")
    image = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
