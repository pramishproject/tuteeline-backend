from urllib.parse import parse_qs

from asgiref.sync import sync_to_async
from channels.middleware import BaseMiddleware
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.db import close_old_connections
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken, AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings


class TokenAuthMiddleware(BaseMiddleware):
    """
    Custom token auth middleware
    """

    async def __call__(self, scope, receive, send):
        close_old_connections()

        # Get the token
        raw_token = parse_qs(scope["query_string"].decode("utf8"))["token"][0]

        validated_token = self.get_validated_token(raw_token)
        user = await self.get_user(validated_token)

        # Return the inner application directly and let it run everything else
        scope = dict(scope, user=user)
        return await self.inner(scope, receive, send)

    def get_validated_token(self, raw_token):
        """
        Validates an encoded JSON web token and returns a validated token
        wrapper object.
        """
        messages = []
        for AuthToken in api_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except TokenError as e:
                messages.append({'token_class': AuthToken.__name__,
                                 'token_type': AuthToken.token_type,
                                 'message': e.args[0]})

        raise InvalidToken({
            'detail': _('Given token not valid for any token type'),
            'messages': messages,
        })

    @sync_to_async
    def get_user(self, validated_token):
        """
        Attempts to find and return a user using the given validated token.
        """
        try:
            user_id = validated_token[api_settings.USER_ID_CLAIM]
        except KeyError:
            raise InvalidToken(_('Token contained no recognizable user identification'))

        try:
            user = get_user_model().objects.get(**{api_settings.USER_ID_FIELD: user_id})
        except get_user_model().DoesNotExist:
            raise AuthenticationFailed(_('User not found'), code='user_not_found')

        if not user.is_active or user.is_archived:
            raise AuthenticationFailed(_('User is inactive'), code='user_inactive')

        return user
