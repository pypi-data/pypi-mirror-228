﻿"""Clases que contienen respuestas del webservice."""

import pprint
import pandas as pd


class WSResponse:
    """Clase base para manejar las respuetsas del WebService.

    Cada respuesta contiene los siguientes atributos:

    Attributes
    ----------
    Codigo : int
        Código de la respuesta.
    Descripcion : str
        Descripción del código de la respuesta.
    Series : dict
        Diccionario que contiene la serie consultada desde el método
        :meth:`~bcchapi.webservice.Session.get`. En caso de usar otro método,
        el diccionario va a contener el texto ``'null'`` para todos sus campos.
        Se compone de 4 instancias: ``'descripEsp'`` con el nombre de la serie
        en español, ``'descripIng'`` con el nombre en inglés, ``'seriesId'``
        con el código de la serie y ``'Obs'``, una lista de diccionarios que
        contienen las observaciones. Cada uno de estos diccionarios se compone
        de 3 instancias: ``'indexDateString'`` con la fecha, ``'value'`` con el
        valor en formato texto (o ``'NaN'`` si no hay datos) y ``'statusCode'``
        que toma el valor de ``'OK'`` cuando existen observaciones en la fecha
        y ``'ND'`` cuando no.
    SeriesInfos : list
        Lista de diccionarios que contiene metadata de las series buscadas por
        el método :meth:`~bcchapi.webservice.Session.search`. En caso de usar
        otro método devuelve una lista vacía. Los diccionarios se componen de 8
        campos: ``'seriesId'`` con el código de la serie, ``'frequencyCode'``
        con la frecuencia de la serie, ``'spanishTitle'` con el nombre en
        español, ``'englishTitle'` con el nombre en inglés,
        ``'firstObservation'` con la fecha de la primera observación
        disponible, ``'lastObservation'`` con la fecha de la última observación
        disponible, ``'updatedAt'`` con la  con la fecha de la última
        actualización y  ``'createdAt'`` con la fecha de creación de la serie.
    """

    def __init__(
        self, Codigo: int, Descripcion: str, Series: dict, SeriesInfos: list
    ) -> None:
        self.Codigo = Codigo
        self.Descripcion = Descripcion
        self.Series = Series
        self.SeriesInfos = SeriesInfos

    def __repr__(self):
        return f"""{self.__class__.__name__}(
    Codigo = {self.Codigo},
    Descripcion = {self.Descripcion},
    Series = {pprint.pformat(self.Series)},
    SeriesInfos = {pprint.pformat(self.SeriesInfos)}
    )"""

    def _to_gsr(self):
        return GSResponse(self.Codigo, self.Descripcion, self.Series, self.SeriesInfos)

    def _to_ssr(self):
        return SSResponse(self.Codigo, self.Descripcion, self.Series, self.SeriesInfos)


class GSResponse(WSResponse):
    """Clase que contiene respuetsas del método GetSeries."""

    def to_series(self) -> pd.Series:
        """Entrega la serie en formato pandas.Series."""
        date_range = pd.to_datetime(
            [i["indexDateString"] for i in self.Series["Obs"]], dayfirst=True
        )
        obs = [float(i["value"]) for i in self.Series["Obs"]]
        serie = self.Series["seriesId"]
        return pd.Series(obs, date_range, name=serie)

    def to_df(self) -> pd.DataFrame:
        """Entrega la serie en formato pandas.DataFrame."""
        return self.to_series().to_frame()

    @property
    def nombre(self):
        return self.Series["descripEsp"]

    @property
    def name(self):
        return self.Series["descripIng"]

    @property
    def id(self):
        return self.Series["seriesId"]


class SSResponse(WSResponse):
    """Clase que contiene respuetsas del método SearchSeries."""

    def to_df(self) -> pd.DataFrame:
        """Entrega los datos en formato pandas.DataFrame."""

        df = pd.DataFrame(self.SeriesInfos)
        for key in ["firstObservation", "lastObservation", "updatedAt", "createdAt"]:
            df[key] = pd.to_datetime(df[key], errors="coerce", format="%d-%m-%Y")

        return df
