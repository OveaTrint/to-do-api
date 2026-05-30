from rest_framework import status, viewsets
from rest_framework.response import Response

from todo.permissions import is_owner_of_todo

from .models import ToDo
from .serializer import ToDoSerializer


class ToDoViewSet(viewsets.ModelViewSet):
    """
    Groups all the views using a Viewset since they all the HTTP methods use the same path.
    The GET method to retrieve all Todos is implemented automatically by the viewset's list() method
    """

    serializer_class = ToDoSerializer
    queryset = ToDo.objects.all()
    http_method_names = ["get", "post", "put", "delete"]

    def create(self, request):
        serializer = ToDoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk: int):
        try:
            todo = ToDo.objects.get(pk=pk)
            is_owner_of_todo(request, todo)

            serializer = ToDoSerializer(todo, request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status.HTTP_200_OK)
            else:
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
