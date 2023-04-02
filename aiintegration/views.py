from adrf.views import APIView
from asgiref.sync import sync_to_async, async_to_sync
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets, views, permissions, status
from rest_framework.generics import *
from rest_framework.viewsets import *
from rest_framework.response import Response
from .serializers import *
from .models import *
from rest_framework.exceptions import PermissionDenied
from aiintegration.Generator import Generator
from aiintegration.models import Image
from aiintegration.permissions import CanDeleteImagePermission, CanViewAIparams
from aiintegration.serializers import PromptSerializer, ImageSerializer

import aiohttp
import asyncio


# async def download_images(image_urls):
#     images = []
#     async with aiohttp.ClientSession() as session:
#         for url in image_urls:
#             async with session.get(url) as response:
#                 image = await response.read()
#                 images.append(image)
#     return images

async def download_images(url):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as response:
            filename = os.path.basename(url)
            filepath = os.path.join('static', 'images', filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            with open(filepath, 'wb') as f:
                f.write(await response.content.read())
            return filepath

class PromptExecutor(APIView):
    def __init__(self):
        self.generator = Generator()

    """
    post request template
                    "prompt": text,
                    "width": prompt.width,
                    "height": prompt.height,
                    "negative_prompt": prompt.negative_prompt,
                    "num_outputs": prompt.num_outputs,
                    "num_interface_steps": prompt.num_steps,
                    "guidance_scale": prompt.guidance_scale,
                    "scheduler": prompt.scheduler,
                    "seed": prompt.seed
    """

    async def post(self, request):
        data = request.data
        newd = data
        prompt = PromptSerializer(data=newd)
        await sync_to_async(prompt.is_valid)(raise_exception=True)
        res = await sync_to_async(prompt.save)()
        ans = await self.generator.generate(res, request.user)
        loop = asyncio.get_event_loop()
        download_tasks = [loop.create_task(download_images(url)) for url in ans]
        images = await asyncio.gather(*download_tasks)
        data = [{"image": open(i), "prompt": prompt.data} for i in images]
        print(data)
        serializer = ImageSerializer(data=data, many=True)
        await sync_to_async(serializer.is_valid)(raise_exception=True)
        ser = await sync_to_async(serializer.save)()
        return Response({'images': ser.data, 'prompt': prompt.data})


class PromptAPIView(views.APIView):
    def get(self, request, pk):
        image = get_object_or_404(Image, prompt_id=pk)
        return Response(ImageSerializer(image).data)

    def delete(self, request, pk):
        if request.user.has_perm(CanDeleteImagePermission):
            cat = get_object_or_404(Image, pk=pk)
            cat.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class PromptListView(generics.ListAPIView):
    serializer_class = PromptSerializer
    queryset = Prompt.objects.all()

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)


class ModelSchedulerApiView(ModelViewSet):
    serializer_class = ModelScedulerSerializer
    queryset = ModelSceduler.objects.all()
    permission_classes = [CanViewAIparams]


class AiModelListCreateAPIView(generics.ListCreateAPIView):
    queryset = AiModel.objects.all()
    serializer_class = AiModelSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AiModelRetrieveUpdateDeleteAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = AiModel.objects.all()
    serializer_class = AiModelSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_update(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied()
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user.is_staff:
            raise PermissionDenied()
        instance.delete()
