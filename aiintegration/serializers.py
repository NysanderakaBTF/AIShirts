from rest_framework import serializers

from cust_and_stuff.serializers import CustomerSerializer
from .models import Image, ModelSceduler, AiModel, Prompt


# TODO: make realted fields by myself (where i use foreign key, or delete them)


class AiModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = AiModel
        fields = ['id', 'access_url', 'description', 'parameters']


class ModelScedulerSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelSceduler
        fields = ['id', 'name']


class PromptSerializer(serializers.ModelSerializer):
    scheduler = ModelScedulerSerializer()
    ai_model = AiModelSerializer()
    owner = CustomerSerializer()

    class Meta:
        model = Prompt
        fields = ['id', 'prompt', 'negative_prompt', 'width', 'height', 'prompt_strenght', 'num_outputs', 'num_steps',
                  'guidance_scale', 'seed', 'is_template', 'is_final']


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
