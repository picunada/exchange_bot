from abc import ABC

from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.exceptions import ValidationError
from tortoise.validators import Validator

from core.logger import log
from utils.check_card_bin import check_bank


def validate_card_number(value):
    """
    A Validator to validate card number for length and bin
    """
    if len(value) not in range(16, 23):
        raise ValidationError(f"Card number is not correct!")
    try:
        check_bank(value)
    except Exception as e:
        log.error(e)


class Users(models.Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(max_length=50)
    chat_id = fields.IntField()
    is_admin = fields.BooleanField(default=False)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)


class Orders(models.Model):
    id = fields.IntField(pk=True)
    amount_before = fields.IntField()
    amount_after = fields.IntField()
    rate: fields.ForeignKeyRelation["Rates"] = fields.ForeignKeyField(
        "models.Rates", related_name="orders"
    )
    withdraw_card = fields.CharField(max_length=19, null=True, validators=[validate_card_number])
    is_paid = fields.BooleanField(default=False)
    user: fields.ForeignKeyRelation["Users"] = fields.ForeignKeyField(
        "models.Users", related_name="orders"
    )
    manager: fields.ForeignKeyNullableRelation["Manager"] = fields.ForeignKeyField(
        "models.Manager", related_name="orders", null=True
    )
    bank: fields.ForeignKeyRelation["Banks"] = fields.ForeignKeyField(
        "models.Banks", related_name="orders"
    )
    status: fields.ForeignKeyRelation["Status"] = fields.ForeignKeyField(
        "models.Status", related_name="orders"
    )


class Status(models.Model):
    id = fields.IntField(pk=True)
    status = fields.CharField(max_length=50)


class Banks(models.Model):
    id = fields.IntField(pk=True)
    bank_name = fields.CharField(max_length=50)


class Rates(models.Model):
    id = fields.IntField(pk=True)
    rate = fields.FloatField()
    created_at = fields.DatetimeField(auto_now_add=True)


class Manager(models.Model):
    id = fields.IntField(pk=True)
    user: fields.ForeignKeyRelation["Users"] = fields.ForeignKeyField(
        "models.Users", related_name="manager"
    )
    created_at = fields.DatetimeField(auto_now_add=True)


Users_Pydantic = pydantic_model_creator(Users, name="User")
UsersIn_Pydantic = pydantic_model_creator(Users, name="UserIn", exclude_readonly=True)

Orders_Pydantic = pydantic_model_creator(Orders, name="Order")
OrdersIn_Pydantic = pydantic_model_creator(Orders, name="OrderIn", exclude_readonly=True)

Status_Pydantic = pydantic_model_creator(Status, name="Status")
StatusIn_Pydantic = pydantic_model_creator(Status, name="StatusIn", exclude_readonly=True)

Banks_Pydantic = pydantic_model_creator(Banks, name="Banks")
BanksIn_Pydantic = pydantic_model_creator(Banks, name="BanksIn", exclude_readonly=True)
