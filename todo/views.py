from rest_framework import status, viewsets
from rest_framework.response import Response

from todo.permissions import is_owner_of_todo

from .models import ToDo
from .serializer import ToDoSerializer

# Create your views here.


# @api_view(["POST"])
# def create_todo(request):
#     serializer = ToDoSerializer(data=request.data)

#     if serializer.is_valid():
#         serializer.save(owner=request.user)
#         return Response(data=serializer.data, status=status.HTTP_201_CREATED)

#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(["GET", "PUT", "DELETE"])
# def todo_get_update_delete(request, pk: int):
#     try:
#         todo = ToDoItem.objects.get(pk=pk)

#         # checks if requesting user is the owner of todo object
#         is_owner_of_todo(request, todo)

#         if request.method == "GET":
#             pass
#         elif request.method == "PUT":
#             serializer = ToDoSerializer(instance=todo, data=request.data)

#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data, status=status.HTTP_200_OK)

#         elif request.method == "DELETE":
#             todo.delete()
#             return Response(status=status.HTTP_204_NO_CONTENT)
#     except ToDoItem.DoesNotExist:
#         return Response(
#             {"detail": "Requested resource does not exist"},
#             status=status.HTTP_404_NOT_FOUND,
#         )


class ToDoViewSet(viewsets.ModelViewSet):
    serializer_class = ToDoSerializer
    queryset = ToDo.objects.all()

    # TODO - Reformat views to make it more modular
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
                status.HTTP_400_BAD_REQUEST,
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
                status.HTTP_400_BAD_REQUEST,
            )
