﻿class ResponseException(Exception):
    """Si la consulta no es exitosa."""

    pass


class InvalidFrequency(ResponseException):
    """Si la frecuencia de busqueda no es válida."""

    pass


class InvalidCredentials(ResponseException):
    """Si el usuario o contraseña no son válidos."""

    pass


class InvalidSeries(ResponseException):
    """Si el código de serie de tiempo es inválido."""

    pass
