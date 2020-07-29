from django.db.models import *
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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
    user = OneToOneField(User, null=False, on_delete=CASCADE)
    name = CharField(max_length=64, null=False, blank=False)
    address = CharField(max_length=64, null=False, blank=False)
    tel = CharField(max_length=32, null=False, blank=False)


class OrderItem(Model):
    order = ForeignKey(Order, null=False, on_delete=CASCADE)
    item = ForeignKey(Item, null=False, on_delete=PROTECT)
    amount = IntegerField(null=False)


def validate_name(name: str) -> bool:
    import re
    if not re.fullmatch('[а-яА-Я ]+', name):
        raise ValidationError('Invalid name')\


class FeedbackModel(Model):
    name = CharField(max_length=100, null=False, blank=False, validators=[validate_name])
    email = EmailField(null=False, blank=False)
    text = TextField(max_length=100, null=False, blank=False)
