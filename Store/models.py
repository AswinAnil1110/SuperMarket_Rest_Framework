from django.db import models

# Create your models here.
class ProductDb(models.Model):
    product_name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    price = models.FloatField()
    production_date = models.DateField()
    expiry_date = models.DateField()
    stock = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

class OrderDb(models.Model):
    customer_name = models.CharField(max_length=100)
    product_id = models.ForeignKey(ProductDb,on_delete=models.PROTECT)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    total_amount = models.FloatField(default=0)
    payment_choices = [('cash','Cash'),('upi','UPI'),('card','Card')]
    payment_type = models.CharField(max_length=20,choices=payment_choices)
    status_choices = [('pending','Pending'),('paied','Paied'),('cancelled','Cancelled')]
    status = models.CharField(max_length=20,choices=status_choices,default='pending')
    order_date = models.DateTimeField(auto_now_add=True)