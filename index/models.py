# from django.db import models

# class Item(models.Model):
#     item_id = models.AutoField(primary_key=True)
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     condition = models.CharField(max_length=255)
#     # photos = models.CharField(max_length=255)
#     photos = models.ImageField()
#     seller_id = models.ForeignKey('accounts.User', on_delete=models.CASCADE)
from django.db import models
from django.contrib.auth.models import User

class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=255, default='Uncategorized')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    condition = models.CharField(max_length=255)
    photos = models.ImageField(upload_to='items/photos')  # Specify the upload directory
    image_encoded = models.TextField(blank=True)
    seller_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class sendmessage(models.Model):
    sender_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name="sender")
    reciver_id = models.ForeignKey(User, on_delete=models.CASCADE,related_name='reciver')
    Item_id = models.CharField(max_length=255,default="")
    message = models.TextField()
    time = models.DateTimeField(auto_now=True)
    read=models.BooleanField(default=False)

    
    def __str__(self):
        return f"Message from {self.sender_id} to {self.reciver_id} at {self.time.strftime('%Y-%m-%d')}"

    class Meta:
        verbose_name_plural = 'Chat Messages'
    def get_sender_name(self):
        return self.sender.get_full_name() or self.sender.username  # Return full name if available, otherwise username


class wishlistModel(models.Model):
    orderId = models.CharField(max_length=20)
    itemId = models.CharField(max_length=20)
    userId = models.CharField(max_length=20)
    qty = models.CharField(max_length=20)
    price = models.CharField(max_length=20)
    totalPrice = models.CharField(max_length=20)
    
    def __str__(self) -> str:
        return self.orderId


class Ordermodel(models.Model):
    userid=models.CharField(max_length=200)
    username=models.CharField(max_length=200)
    useremail=models.EmailField()
    productid=models.CharField(max_length=200)
    qty=models.CharField(max_length=200,default="")
    # address=models.TextField()
    # city=models.CharField(max_length=200)
    # state=models.CharField(max_length=200)
    # pincode=models.CharField(max_length=200)
    orderamount=models.CharField(max_length=200)
    paymentvia=models.CharField(max_length=200)
    paymentmethod=models.CharField(max_length=200)
    transactionid=models.TextField()
    orderdatetime=models.DateTimeField(auto_created=True,auto_now=True)

    def __str__(self) -> str:
        orderid=self.pk
        return str(orderid)