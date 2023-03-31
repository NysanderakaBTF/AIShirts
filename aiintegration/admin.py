from django.contrib import admin
from .models import Image, ModelSceduler, AiModel, Prompt


class ImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_at', 'is_final', 'image')
    search_fields = ('uploaded_at',)
    list_filter = ('is_final',)
    list_editable = ('is_final',)


class ModelScedulerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    list_editable = ('name',)


class AiModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'access_url', 'description')
    search_fields = ('access_url', 'description')
    list_editable = ('access_url', 'description')


class PromptAdmin(admin.ModelAdmin):
    list_display = ('id', 'prompt', 'negative_prompt', 'width', 'height', 'prompt_strenght', 'num_outputs', 'num_steps',
                    'guidance_scale', 'scheduler', 'ai_model', 'seed', 'owner', 'is_template', 'is_final')
    search_fields = ('prompt', 'ai_model', 'owner')
    list_filter = ('is_template', 'is_final')
    list_editable = ('is_template', 'is_final')


admin.site.register(Image, ImageAdmin)
admin.site.register(ModelSceduler, ModelScedulerAdmin)
admin.site.register(AiModel, AiModelAdmin)
admin.site.register(Prompt, PromptAdmin)
