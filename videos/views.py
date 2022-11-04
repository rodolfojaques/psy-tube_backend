from django.shortcuts import render
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework import generics
from pytube import YouTube

from psytube.pagination import CustomPageNumberPagination
from .models import Video
from .serializers import ListVideoDetailSerializer, VideoSerializer
import requests
from traitlets import Bool
from videos.serializers import VideoSerializer, ListTopVideoSerializer
import ipdb


class CreateVideoView(APIView):
    queryset = Video
    serializer_class = VideoSerializer

    def post(self, request):
        try:
            yt = YouTube(request.data["link"])
            video = yt.streams.filter(progressive=True).last()
            video.download(output_path="./media", filename="video")
        except KeyError:
            return Response({"message": "invalid link"}, status.HTTP_400_BAD_REQUEST)
        my_file = open("./media/video", "rb")
        response = requests.post("https://file.io", files={"file": my_file})
        my_file.close()
        resposta = {
            "title": yt.title,
            "thumbnail": yt.thumbnail_url,
        }
        serializer = VideoSerializer(data=resposta)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save(link=request.data["link"])
        if Bool(request.user and request.user.is_authenticated):
            # ipdb.set_trace()
            instance.users.set(
                [*[user["id"] for user in serializer.data["users"]], request.user.id]
            )
        return Response(
            {
                **resposta,
                "link": request.data["link"],
                "download_url": response.json()["link"],
            },
            status.HTTP_200_OK,
        )


class ListTopVideosView(generics.ListAPIView):
    queryset = Video.objects.all()
    serializer_class = ListTopVideoSerializer

    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        return self.queryset.order_by("-downloads")[0:10]


class ListDetailVideosView(generics.RetrieveAPIView):
    queryset = Video.objects.all()
    serializer_class = ListVideoDetailSerializer

    pagination_class = CustomPageNumberPagination
