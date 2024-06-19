from django.db import models

# Create your models here.
class ProductTransaction(models.Model):
    id=models.IntegerField(primary_key=True)
    title=models.CharField(max_length=500)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    description=models.TextField()
    category=models.CharField(max_length=255)
    # image=models.CharField()
    sold=models.BooleanField()
    date_of_sale=models.DateField()

    def __str__(self):
        return self.title