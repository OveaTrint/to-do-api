from rest_framework import routers

from todo.views import ToDoViewSet

app_name = "todo"

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"todos", ToDoViewSet)

urlpatterns = router.urls
