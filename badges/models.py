from django.db import models

class Badge(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='badges/')
    purchasable = models.BooleanField(default=False)
    price = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return f"{self.name} Badge"
