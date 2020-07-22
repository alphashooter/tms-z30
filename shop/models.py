from django.db.models import *
from root import settings

# Create your models here.


class Item(Model):
    title = CharField(max_length=32, null=False, blank=False)
    description = TextField(null=True, default=None)
    price = DecimalField(max_digits=10, decimal_places=2)
    image = ImageField(upload_to=settings.MEDIA_ROOT, null=True)

    def __str__(self):
        return self.title

    @property
    def formatted_price(self):
        return f'${self.price}'


class Order(Model):
    name = CharField(max_length=64, null=False, blank=False)
    address = CharField(max_length=64, null=False, blank=False)
    tel = CharField(max_length=32, null=False, blank=False)


class OrderItem(Model):
    order = ForeignKey(Order, null=False, on_delete=CASCADE)
    item = ForeignKey(Item, null=False, on_delete=PROTECT)
    amount = IntegerField(null=False)
