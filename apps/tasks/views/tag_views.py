from rest_framework.generics import get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from apps.tasks.models import Tag
from apps.tasks.serializers.tag_serializers import TagSerializer


class TagListAPIView(APIView):

    def get_objects(self):
        tags = Tag.objects.all()
        return tags

    def get(self, request: Request) -> Response:
        tags = self.get_objects()

        if not tags.exists():
            return Response(
                data=[],
                status=status.HTTP_204_NO_CONTENT
            )

        serializer = TagSerializer(tags, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request: Request) -> Response:
        serializer = TagSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                data=serializer.validated_data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TagDetailApiView(APIView):

    def get_object(self, tag_id: int) -> Tag:
        return get_object_or_404(Tag, pk=tag_id)

    def get(self, request: Request, tag_id: int) -> Response:
        tag = self.get_object(tag_id)
        serializer = TagSerializer(tag)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, tag_id: int):
        tag = self.get_object(tag_id)

        serializer = TagSerializer(tag, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request: Request, tag_id: int):
        tag = self.get_object(tag_id)

        tag.delete()
        response_msg = {
            "message": "Successfully deleted"
        }
        return Response(data=response_msg, status=status.HTTP_200_OK)
