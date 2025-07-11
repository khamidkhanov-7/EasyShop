from tortoise import fields
from tortoise.models import Model


class Product(Model):
    id = fields.IntField(pk=True)
    product_name = fields.CharField(max_length=100)
    product_description = fields.CharField(max_length=500)
    product_price = fields.IntField(max_length=50)
    product_owner_id = fields.CharField(max_length=50)

    def __str__(self):
        return self.product_name