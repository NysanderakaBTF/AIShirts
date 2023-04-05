import os
import time

from django.core.files import File
from django.urls import reverse
from psycopg2 import Date
from rest_framework import serializers

from cust_and_stuff.models import Customer
from cust_and_stuff.serializers import CustomerSerializer
from .models import Image, ModelSceduler, AiModel, Prompt


# TODO: make realted fields by myself (where i use foreign key, or delete them)


class AiModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AiModel
        fields = ['id', 'access_url', 'description', 'parameters', 'name']


class ModelScedulerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelSceduler
        fields = ['id', 'name']


class PromptSerializer(serializers.ModelSerializer):
    scheduler = serializers.PrimaryKeyRelatedField(queryset=ModelSceduler.objects.all())
    ai_model = serializers.PrimaryKeyRelatedField(queryset=AiModel.objects.all())
    owner = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())

    class Meta:
        model = Prompt
        fields = '__all__'

    def create(self, validated_data):
        prompt = Prompt.objects.create(**validated_data)
        return prompt


class PromptDetailSerializer(serializers.ModelSerializer):
    scheduler = ModelScedulerSerializer(ModelSceduler.objects.all())
    ai_model = AiModelSerializer(AiModel.objects.all())
    owner = CustomerSerializer(Customer.objects.all())
    images = serializers.SerializerMethodField()

    def get_images(self, obj):
        img = Image.objects.filter(prompt_id=obj.id)
        return [{'image': i.image_path, 'id': i.pk} for i in img]

    class Meta:
        model = Prompt
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    # image = serializers.FileField(write_only=True, required=True)
    image_path = serializers.CharField(required=True)
    prompt = PromptSerializer()

    class Meta:
        model = Image
        fields = '__all__'

    def create(self, validated_data):
        # print(validated_data)
        # print(self.initial_data)
        # image_path = validated_data.pop('image_path')
        # prompt_data = dict(self.initial_data[0].get('prompt'))
        # print(prompt_data)
        #
        # prompt = Prompt.objects.get(id=prompt_data['id'])
        # save_data = validated_data
        # del save_data['prompt']
        # print(save_data)
        # # image = Image(prompt=prompt, **save_data)
        # # image.image = image_path
        # # image.save()
        # # print(self.initial_data)
        # # prompt_id = self.initial_data.get('prompt')['id']
        # # print(prompt_id)
        # # image_path = validated_data.pop('image_path')
        # # prompt_data = validated_data.pop('prompt')
        # # prompt = Prompt.objects.get(id=prompt_data['id'])
        # # # Open the file at the specified path and assign it to the image field
        # with open(image_path, 'rb') as f:
        #     django_file = File(f)
        #     image = Image(prompt=prompt, image=django_file, **validated_data)
        # image.save()
        print(validated_data)
        image_path = validated_data.pop('image_path')
        # prompt_data = validated_data.pop('prompt')
        prompt_data = dict(self.initial_data[0].get('prompt'))
        prompt = Prompt.objects.get(id=prompt_data['id'])
        save_data = validated_data
        save_data.pop('prompt')
        image = Image(prompt=prompt, image_path='media/' + image_path, **save_data)
        image.save()
        return image
