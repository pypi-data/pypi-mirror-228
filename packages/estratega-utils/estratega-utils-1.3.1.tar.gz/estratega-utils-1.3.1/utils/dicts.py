from typing import Any
from devtools import debug
from pydantic import BaseModel, create_model
from pydantic.dataclasses import dataclass
from enum import Enum


class Use:
    '''
        Esta clase permite pasarle un diccionario como parámetro para tratarlo como 
        un objeto y acceder a sus elementos con la notación de punto, además de 
        utilizarlo dentro de un contexto con "with".
    '''
    instances: list = []
    diccionario: dict

    def __init__(self, d):
        Use.instances.append(self)
        self.d = d

    def __enter__(self):
        Campos = {k: (type(v), ...) for k, v in self.d.items()}
        self.DiccionarioComoObjeto = create_model(
            'DiccionarioComoObjeto', **Campos)  # type:ignore
        self.o = self.DiccionarioComoObjeto(**self.d)
        return self.o

    def __exit__(self, exc_type, exc_value, traceback):
        Use.diccionario = self.o.dict()

    @staticmethod
    def set(dicc: dict):
        aux = Use.diccionario
        for i in dicc:
            del i
        dicc.update(**aux)
        for instance in Use.instances:
            del instance
        Use.instances = []
