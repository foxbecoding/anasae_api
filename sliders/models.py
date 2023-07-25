from django.db import models

class Slider(models.Model):
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)

class SliderImage(models.Model):
    slider = models.ForeignKey(Slider, on_delete=models.CASCADE)
    image = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now_add=True, null=True)
