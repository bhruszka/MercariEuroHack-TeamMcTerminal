import json

from django.contrib.auth import get_user_model, login, authenticate


class AuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        setattr(request, '_dont_enforce_csrf_checks', True)

        if request.body and request.content_type == 'application/json':
            data = json.loads(request.body.decode("utf-8") )

            facebook_id = data.get('userId')

            try:
                user = get_user_model().objects.get(facebook_id=facebook_id)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
            except get_user_model().DoesNotExist:
                pass
        elif request.GET and request.GET.get('userId'):
            facebook_id = request.GET.get('userId')

            try:
                user = get_user_model().objects.get(facebook_id=facebook_id)
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
            except get_user_model().DoesNotExist:
                pass


        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response