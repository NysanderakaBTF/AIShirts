import os

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

from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


async def download_images(url):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(url) as response:
            # filename = os.path.basename(url)
            filename = os.path.basename(url)
            print(filename)
            filepath = os.path.join('images/' + filename[:-4] + str(time.time() * 1000000) + filename[-4:])
            data = await response.content.read()
            default_storage.save(filepath, ContentFile(data))
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
        images_data = [{"image_path": i, "prompt": prompt.data} for i in images]
        serializer = ImageSerializer(data=images_data, many=True)
        await sync_to_async(serializer.is_valid)(raise_exception=True)
        saved_images = await sync_to_async(serializer.save)()
        return Response(
            {'images': await sync_to_async(list)([{'id': i.id, 'image_path': i.image_path} for i in saved_images]),
             'prompt': prompt.data})


class PromptImageAPIView(views.APIView):
    def get(self, request, pk):
        image = Image.objects.filter(pk=pk)
        return Response(ImageSerializer(instance=image, many=True).data)

    def delete(self, request, pk):
        if request.user.has_perm(CanDeleteImagePermission):
            cat = get_object_or_404(Image, pk=pk)
            cat.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def put(self, request, pk):
        if request.user.has_perm(CanDeleteImagePermission):
            img = get_object_or_404(Image, pk=pk)
            serializer = ImageSerializer(instance=img, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_403_FORBIDDEN)


class PromptDetailAPIView(viewsets.ModelViewSet):
    queryset = Prompt.objects.all()
    serializer_class = PromptDetailSerializer

    def update(self, request, pk):
        prompt = get_object_or_404(Prompt, pk=pk)
        serializer = PromptDetailSerializer(instance=prompt, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


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
