from rest_framework import status, viewsets
from rest_framework.response import Response

from todo.permissions import is_owner_of_todo

from .models import ToDo
from .serializer import ToDoSerializer


class ToDoViewSet(viewsets.ModelViewSet):
    serializer_class = ToDoSerializer
    queryset = ToDo.objects.all()
    http_method_names = ["get", "post", "put", "delete"]

    def list(self, request):
        queryset = ToDo.objects.filter(owner=request.user)
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = ToDoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status.HTTP_201_CREATED)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk: int):
        try:
            todo = ToDo.objects.get(pk=pk)
            is_owner_of_todo(request, todo)

            serializer = ToDoSerializer(todo, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except ToDo.DoesNotExist:
            return Response(
                {"detail": "The requested resource does not exist"},
                status.HTTP_404_NOT_FOUND,
            )

    def destroy(self, request, pk: int):
        try:
            todo = ToDo.objects.get(pk=pk)
            is_owner_of_todo(request, todo)

            todo.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ToDo.DoesNotExist:
            return Response(
                {"detail": "The requested resource does not exist"},
                status.HTTP_404_NOT_FOUND,
            )
