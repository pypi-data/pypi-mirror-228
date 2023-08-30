"""API para conectarse al webservice del Banco Central de Chile."""

import requests
import pandas as pd

from .wsresponse import WSResponse, GSResponse, SSResponse
from .exception import InvalidFrequency, InvalidCredentials, InvalidSeries
from .credentials import read_credentials

URL = "https://si3.bcentral.cl/SieteRestWS/SieteRestWS.ashx"


class Session:
    """Conexión para Base de Datos Estadísticos del Banco CEntral de Chile.

    El Banco Central de Chile provee dos métodos en este servicio, uno que
    permite obtener los datos de las series estadísticas, y otro que entrega el
    catálogo de las series disponibles para ser consultadas.

    Parameters
    ----------
    usr : str, opcional
        Nombre de usuario.
    pwd : str, opcional
        Contraseña.
    file : str u objeto de ruta, opcional
        Importa las credenciales desde un archivo de texto donde la primera
        línea es el nombre de usuario y la segunda es la contraseña.

    """

    def __init__(self, usr: str = None, pwd: str = None, *, file: str = None):

        self._usr = usr
        self._pwd = pwd

        if usr is None and pwd is None:
            if file is None:
                m = "Debe introducir usuario y contraseña o ruta de archivo con credenciales."
                raise ValueError(m)
            self._usr, self._pwd = read_credentials(file)

    def get(
        self, time_series: str, first_date: str = "", last_date: str = ""
    ) -> GSResponse:
        """Permite obtener los datos de la serie.


        Parameters
        ----------
        time_series : str
            Incorporar código de la serie de tiempo a consultar.
        first_date : str u objeto de fecha, opcional
            Ingresar fecha en formato ``'YYYY-MM-DD'`` desde la que se requiere
            recoger datos. Si el parámetro no está presente, se recoge por
            defecto desde el primer dato disponible.
        last_date : str u objeto de fecha,, opcional
            Ingresar fecha en formato ``'YYYY-MM-DD'`` hasta la que se requiere
            recoger datos. Si el parámetro no está presente, se recoge por
            defecto hasta el último dato disponible.

        Returns
        -------
        GSResponse
            Un objeto GSResponse que contiene la respuesta.

        Raises
        ------
        InvalidSeries
            Si la serie consultada no existe.
        InvalidCredentials
            Si las credenciales no son válidas.

        """

        if hasattr(first_date, "strftime"):
            first_date = first_date.strftime("%Y%m%d")

        if hasattr(last_date, "strftime"):
            last_date = last_date.strftime("%Y%m%d")

        params = {
            "user": self._usr,
            "pass": self._pwd,
            "firstdate": first_date,
            "lastdate": last_date,
            "timeseries": time_series,
            "function": "GetSeries",
        }
        response = self._make_request(params)

        if response.Codigo == -50:
            raise InvalidSeries(f"Serie {time_series!r} no encontrada.")

        return response._to_gsr()

    def search(self, frequency: str) -> SSResponse:
        """Permite ver la lista de series disponibles por frecuencia y su metadata.

        Parameters
        ----------
        frequency : ``{'DAILY', 'MONTHLY', 'QUARTERLY', 'ANNUAL'}``
            Completar con la frecuencia para la cual se quiere consultar el
            catálogo de series disponibles. Puede tomar los valores DAILY,
            MONTHLY, QUARTERLY o ANNUAL.

        Returns
        -------
        SSResponse
            Un objeto ``SSResponse`` que contiene la respuesta.

        Raises
        ------
        InvalidFrequency
            Si la serie consultada no existe.
        InvalidCredentials
            Si las credenciales no son válidas.

        """
        params = {
            "user": self._usr,
            "pass": self._pwd,
            "frequency": frequency,
            "function": "SearchSeries",
        }
        response = self._make_request(params)

        if response.Codigo == -1:
            m = f"El parámetro 'frequency' debe ser DAILY, MONTHLY, QUARTERLY o ANNUAL. No {frequency!r}."
            raise InvalidFrequency(m)

        return response._to_ssr()

    def _make_request(self, params: dict) -> WSResponse:
        r = requests.get(URL, params=params)
        self.last_response = r.json()
        response = WSResponse(**self.last_response)

        if response.Codigo == -5:
            raise InvalidCredentials("Usuario o contraseña incorrecta.")

        return response


class Siete(Session):
    """Interfaz para crear cuadros y buscar series del Banco Central de Chile.

    Parameters
    ----------
    usr : str, opcional
        Nombre de usuario.
    pwd : str, opcional
        Contraseña.
    file : str u objeto de ruta, opcional
        Importa las credenciales desde un archivo de texto donde la primera
        línea es el nombre de usuario y la segunda es la contraseña.

    """

    def cuadro(
        self,
        series: list,
        desde: str = "",
        hasta: str = "",
        *,
        nombres: list = None,
        frecuencia=None,
        observado=None,
        variacion: int = None,
        resample_kw: dict = dict(),
        aggregate_kw: dict = dict(),
        detener_invalidas: bool = True,
    ) -> pd.DataFrame:
        """Construye un cuadro en formato DataFrame de acuerdo a series solicitadas.

        Parameters
        ----------
        series : str, list o dict
            Incorporar códigos de la serie de tiempo a consultar. En caso
            introducir un diccionario se toma el valor como el código de la
            serie y la llave como el nombre de la columna del cuadro resultado.
        desde : str, opcional
            Ingresar fecha en formato ``'YYYY-MM-DD'`` desde la que se requiere
            recoger datos. Si el parámetro no está presente, se recoge por
            defecto desde el primer dato disponible.
        hasta : str, opcional
            Ingresar fecha en formato ``'YYYY-MM-DD'`` hasta la cual se requiere
            recoger datos. Si el parámetro no está presente, se recoge por
            defecto hasta el último dato disponible.
        nombres : list, opcional
            Nombres de la columnas del cuadro. Debe tener el mismo largo que el
            objeto del parámetro ``series``.
        frecuencia : str, opcional
            Permite reagrupar la series en una frecuencia distinta a la
            original. Valores aceptados son ``'A'`` para una frecuencia anual,
            ``'Q'`` para trimestral, ``'M'`` para mensual, ``'D'`` para diaria,
            etc. Este parámetro utiliza el método ``pandas.DataFrame.resample``
            y el listado de argumentos disponibles se pueden encontrar en su
            documentación:
            `DateOffset objects <https://pandas.pydata.org/pandas-docs/stable/user_guide/timeseries.html#dateoffset-objects>`_.
        observado : función, str, list, o dict, opcional
            función utilizada para agrupar los datos cuando se cambia de
            frecuencia. Utiliza el método ``pandas.DataFrame.aggregate``. El
            listado de argumentos disponibles se pueden encontrar en su
            documentación: :meth:`pandas.DataFrame.aggregate`.
        variacion : int o str, opcional
            Calcula la variación porcentual del cuadro con respecto al o los
            periodos anteriores establecidos en este parámetro. Recibe los
            mismos valores disponibles para ``frecuencia``. Por defecto, en
            caso de introducir un numero entero se convierte a meses. A modo
            de ejemplo, establecer ``variacion=12`` mostrará la variación de
            los datos con respecto a su mismo periodo del año anterior.
        resample_kw : dict, opcional
            Argumentos adicionales para el método :meth:`pandas.DataFrame.resample`.
        aggregate_kw : dict, opcional
            Argumentos adicionales para el método :meth:`pandas.DataFrame.aggregate`.
        detener_invalidas : bool, opcional
            Arrojar error si alguna de las series consultadas no existe o no se
            encuentra disponible. True por defecto.

        Returns
        -------
        pandas.DataFrame
            Un cuadro con las series consultadas.

        """
        if isinstance(series, dict):
            k = series.keys()
            v = series.values()
            return self.cuadro(
                v,
                desde,
                hasta,
                nombres=k,
                variacion=variacion,
                frecuencia=frecuencia,
                observado=observado,
                resample_kw=resample_kw,
                aggregate_kw=aggregate_kw,
                detener_invalidas=detener_invalidas,
            )

        if isinstance(series, str):
            series = series.replace(" ", "").split(",")

        # Check that all series are strings
        for i in series:
            if not isinstance(i, str):
                m = f"Los objetos dentro de 'series' deben ser 'str', no '{type(i)}'"
                raise TypeError(m)

        # Get series
        data = []
        failed = []
        for ts in series:
            try:
                serie = self.get(ts, desde, hasta)
            except InvalidSeries as e:
                if detener_invalidas:
                    raise e
                failed.append(ts)
            else:
                data.append(serie)

        if len(data) == 0:
            m = "Ninguna de las series consultadas fue encontrada."
            raise InvalidSeries(m)

        data = [i.to_df() for i in data]
        df = pd.concat(data, axis=1)

        # Rename columns
        if nombres:
            dnames = {k: v for k, v in zip(series, nombres)}
            df = df.rename(columns=dnames)

        # Resample frequency
        if frecuencia:
            if not observado:
                m = "Debe especificar una función de agregación en 'observado'."
                raise ValueError(m)

            if isinstance(observado, dict):
                # delete failed requests.
                for i in failed:
                    observado.pop(i)
            df = df.resample(frecuencia, **resample_kw).aggregate(
                observado, **aggregate_kw
            )

        # percent variations
        if variacion:
            if isinstance(variacion, int):
                # Convert to monthly offset.
                freq = pd.DateOffset(months=variacion)
            else:
                freq = variacion

            df = df.pct_change(freq=freq)

        return df

    def buscar(
        self, contiene: str, ingles: bool = False, cache: bool = True
    ) -> pd.DataFrame:
        """Busca palabras en los nombres de las series.

        Parameters
        ----------
        contiene: str
            Cadena de caracteres a buscar.
        ingles : bool, opcional
            Buscar en los nombres en inglés. False por defecto.
        cache : bool, opcional
            Utilizar datos guardados si existen.

        Returns
        -------
        pandas.DataFrame
            Un cuadro con las metadata de las series encontradas.

        """
        freq = ["DAILY", "MONTHLY", "QUARTERLY", "ANNUAL"]

        if cache and hasattr(self, "_cache"):
            full_data = self._cache  # use cache data
        else:
            full_data = pd.concat([self.search(i).to_df() for i in freq])  # get data
            if cache:
                self._cache = full_data  # save cache

        if ingles:
            column = "englishTitle"
        else:
            column = "spanishTitle"

        criteria = full_data[column].str.upper().str.contains(contiene.upper())

        res = full_data.loc[criteria].reset_index(drop=True)

        return res
