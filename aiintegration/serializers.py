import os

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


class ImageSerializer(serializers.ModelSerializer):
    img_url = serializers.SerializerMethodField()
    prompt = PromptSerializer()

    class Meta:
        model = Image
        fields = '__all__'
        read_only = True
        editable = False

    def get_img_url(self, obj):
        return obj.image.url

    def create(self, validated_data):
        print(validated_data)
        image_url = validated_data.pop('image_url')
        prompt_data = validated_data.pop('prompt')
        prompt = Prompt.objects.create(**prompt_data)
        image = Image(prompt=prompt, **validated_data)
        image.image.save(os.path.basename(image_url), open(image_url, 'rb'))
        image.save()
        return image
