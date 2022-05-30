from apps.core import generics
from apps.user.serializers import normal_user_serializers
from apps.user.usecases import normal_user_usecases


class ListNormalUserView(generics.ListAPIView):
    """
    Use this end-point to list normal user
    """
    serializer_class = normal_user_serializers.ListNormalUserForNormalUserSerializer

    def get_queryset(self):
        return normal_user_usecases.ListNormalUserUseCase().execute()
