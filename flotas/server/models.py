from django.db import models


class Location(models.Model):
    vehicle = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
        ordering = ['timestamp']

    def __str__(self):
        return f"Location of {self.vehicle} at {self.timestamp}. Coords: ({self.latitude,self.longitude}) "