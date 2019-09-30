import ujson
from aiohttp import web
from pydantic import ValidationError


def json_error(status_code: int, exception: Exception) -> web.Response:
    """
    Возвращаем ошибку
    :param status_code:
    :param exception:
    :return:
    """
    return web.Response(
        status=status_code,
        body=ujson.dumps({
            'error': exception.__class__.__name__,
            'detail': str(exception)
        }).encode('utf-8'),
        content_type='application/json')


async def error_middleware(app: web.Application, handler):
    """
    Мидлвара для обработки
    :param app:
    :param handler:
    :return:
    """

    async def func(request):
        try:
            response = await handler(request)
            if response.status == 404:
                return json_error(response.status, Exception(response.text))
            return response
        except ValidationError as e:
            return json_error(400, e)
        except web.HTTPException as ex:
            if ex.status == 404:
                return json_error(ex.status, ex)
            raise
        except Exception as e:
            return json_error(500, e)

    return func
