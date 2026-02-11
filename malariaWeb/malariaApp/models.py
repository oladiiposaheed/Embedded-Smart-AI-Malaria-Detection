from django.db import models

# Create your models here.

class PredictionModel(models.Model):
    image = models.ImageField(upload_to='images/')
    result = models.CharField(max_length=100)
    confidence = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Prediction {self.id} - Result: {self.result} at {self.created_at}'