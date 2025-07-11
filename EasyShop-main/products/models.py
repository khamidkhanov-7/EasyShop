from tortoise import fields
from tortoise.models import Model


class Product(Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    description = fields.CharField(max_length=500)
    price = fields.IntField()
    owner_id = fields.IntField()

    def __str__(self):
        return self.name
