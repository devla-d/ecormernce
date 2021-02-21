from django.db import models
from accounts.models import Account
from django.urls import reverse
# Create your models here.








CATEGORY_CHOICES = (
    ('S', 'Shoes'),
    ('SW', 'Sport wear'),
    ('HM', 'Home'),
    ('CR', 'Cars'),
    ('EL', 'Electronic'),
    ('BK', 'Books'),
    ('MP', 'mobile Phone'),
    ('mk', 'Makeup'),
)




class Item(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products')
    description = models.TextField()
    price = models.FloatField()
    discount_price = models.FloatField(blank=True , null=True)
    date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    slug = models.SlugField(unique=True, blank=True,null=True)
    
   

    def __str__(self):
        return self.name

    def get_abolute_url(self):
        return reverse("store-detail", kwargs={
            'slug': self.slug
        })

    def get_add_to_cart_url(self):
        return reverse("cart", kwargs={
            'slug': self.slug
        })

    def get_delete_to_cart_url(self):
        return reverse("remove_item", kwargs={
            'slug': self.slug
        })

    def get_delete_single_to_cart_url(self):
        return reverse("remove_single_item", kwargs={
            'slug': self.slug
        })

    '''def save(self, *args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            super(Item,self).save(*args, **kwargs)'''



class OrderItem(models.Model):
    item = models.ForeignKey(Item,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    quantity = models.IntegerField(default=1)
    order = models.ForeignKey("Order", on_delete=models.SET_NULL, null=True)
    customer = models.ForeignKey( Account, on_delete=models.CASCADE)


    def get_total_price(self):
        return self.item.price * self.quantity

    def get_total_discount_price(self):
        return self.item.discount_price * self.quantity


    def __str__(self):
        return f"{self.item.name} and {self.quantity}"


class Order(models.Model):
    customer = models.ForeignKey( Account, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(OrderItem, related_name='item_order')

   
    
    def __str__(self):
        return  f"{self.customer.username} order"
    @property
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_total_price()
        return total


    def shipping(self):
        shipping = True
        return shipping





class Shipping(models.Model):
    customer = models.ForeignKey(Account, on_delete=models.CASCADE,blank=True)
    Address = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100,null=True)


    
    def __str__(self):
        return  self.Address



  




