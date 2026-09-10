from rest_framework.generics import CreateAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.users.serializers import RegisterSerializer, UserSerializer
from apps.users.models import User

import logging

logger = logging.getLogger(__name__)

# Generic view: handles the whole "POST -> validate -> save -> 201" flow.
# We only plug in which serializer to use.
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

class UserDetailView(APIView):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        # Shortcut for:
        # try:
        #     user = User.objects.get(pk=pk)
        # except User.DoesNotExist:
        #     raise Http404

        logger.error("user fetched: %s", vars(user))

        serializer = UserSerializer(user)
        return Response(serializer.data)

# NOTE: generic equivalent of the view above — same behavior, 2 lines:
# class UserDetailView(RetrieveAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
