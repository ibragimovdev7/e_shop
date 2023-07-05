from django.db import models


class Order(models.Model):
    STATUES = [
        ('PENDING', 'pending'),
        ('INPROGRESS', 'inprogress'),
        ('COMPLATED', 'complated'),
        ('CANCELED', 'canceled')
    ]
    custumor = models.ForeignKey('account.CustomUser', on_delete=models.SET_NULL, null=True, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    required_date = models.DateTimeField(null=True)
    shipped_date = models.DateTimeField(null=True)
    canceled_date = models.DateTimeField(null=True)
    status = models.CharField(max_length=10, choices=STATUES)

    def str(self):
        return f'{self.custumor.str()} -- order_id : {self.id}'

    def item_count(self):
        return self.details.count()

    def total_price(self):
        return sum([i.total_price() for i in self.details.all()])


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='details')
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, related_name='orders')
    quantity = models.IntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity

    def str(self):
        return f'order :{self.order} -- {self.product} -- quantity :{self.quantity}'