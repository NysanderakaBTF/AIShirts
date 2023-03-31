from rest_framework import serializers

from cust_and_stuff.models import Customer


# TODO: make celery scheduler to daily set current gen n to 0
def dailyLimitCheck(user: Customer):
    if user.generation_count < user.daily_limit:
        raise serializers.ValidationError("You have reached your daily limit")
    return True
