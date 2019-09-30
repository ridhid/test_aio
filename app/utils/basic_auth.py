import sys

from aiohttp_basicauth import BasicAuthMiddleware


class CustomBasicAuth(BasicAuthMiddleware):
    async def authenticate(self, request):
        if hasattr(sys, "_called_from_test"):
            return True
        return await super().authenticate(request)

    async def check_credentials(self, username, password):
        return username == 'user' and password == 'password'


auth = CustomBasicAuth()
