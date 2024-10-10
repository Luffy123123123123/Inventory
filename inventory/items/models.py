from django.db import models

# Create your models here.


class Items(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'items'