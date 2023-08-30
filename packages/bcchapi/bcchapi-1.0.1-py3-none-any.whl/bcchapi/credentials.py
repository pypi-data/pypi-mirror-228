"""Funciones para obtener credenciales."""

from getpass import getpass


def get_credentials() -> tuple:
    """Pide usuario y contraseña.

    Returns
    -------
    tuple
        Una tupla de dos strings: usuario y la contraseña.
    """
    user = input("user: ")
    password = getpass("pass: ")
    return user, password


def read_credentials(file: str) -> tuple:
    """Lee credenciales desde un archivo de texto.

    La primera línea debe ser el usuario y la segunda la contraseña.

    Parameters
    ----------
    file : str o ruta
        Ubicación el archivo con credenciales.

    Returns
    -------
    tuple
        Una tupla de dos strings: usuario y la contraseña.
    """

    with open(file, "r") as f:
        user = next(f).rstrip("\n")
        password = next(f).rstrip("\n")

    return user, password
