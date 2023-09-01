from abc import abstractmethod
from typing import Any
from pydantic import field_validator
from pydantic.dataclasses import dataclass
from devtools import debug
from enum import Enum
import sys
import os
import re
import pymysql

# from utils.query_builder.mysql import Condition
relative_path = os.getcwd()
sys.path.append(relative_path)
if True:
    from utils.strings import clean


class Filters(Enum):
    GROUP = 'group'
    ORDER = 'order'


class Operators(Enum):
    IGUAL = '='
    DIFERENTE = '<>'
    MAYOR = '>'
    MENOR = '<'
    MAYORIGUAL = '>='
    MENORIGUAL = '<='
    AND = 'AND'
    OR = 'OR'
    NOT = 'NOT'
    ISNULL = 'IS NULL'
    ISNOTNULL = 'IS NOT NULL'
    LIKE = 'LIKE'
    IN = 'IN'


class Joins(Enum):
    INNER = 'INNER'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'
    FULL = 'FULL'
    SELF = 'SELF'


class Aggregations(Enum):
    COUNT = 'COUNT'
    AVG = 'AVG'
    SUM = 'SUM'


@dataclass
class Tabla:
    nombre: str
    alias: str | None = None

    def __str__(self) -> str:
        return f'{clean(self.nombre)} `{clean(self.alias)}`'

    @property
    def value(self) -> str:
        return self.alias if self.alias is not None else self.nombre


@dataclass
class Condition:
    columna: str
    operador: Operators
    valor: str | list
    siguiente: Operators | None = None
    negar: bool = False
    like_left: int | None = None
    like_right: int | None = None
    # @field_validator('negacion')
    # def validator_negacion(cls, v):
    #     if v not in (LogicOperators.NOT, None):
    #         raise ValueError("Valor inválido"


@dataclass
class Join:
    tabla: str
    tipo: Joins
    columna_clave: str


@dataclass
class Aggregate:
    tipo: Aggregations
    columna: str
    tabla: str = ''

    def __str__(self) -> str:
        return f'{self.tipo.value}({tabla.value}.{self.columna})'


@dataclass
class Case:
    resultado: str
    condicion: str | None = None

    def __str__(self) -> str:
        if self.condicion is None:
            return f' ELSE {self.resultado} '
        else:
            return f' WHEN {clean(self.condicion)} THEN "{clean(self.resultado)}" '


class QueryBasics:
    def __init__(self,
                 table: Tabla,
                 columns: list[str] | None = None,
                 conditions: list[Condition] | None = None,
                 ) -> None:
        self.columns = [
            f'{clean(table.value)}.{clean(x)}' for x in columns] if columns is not None else None
        self.table = table
        self.conditions = conditions
        self.s_conditions = ''

    def _format_columns(self) -> str:
        if self.columns is None:
            return ' * '
        s_columns: str = ", ".join(self.columns)
        return s_columns

    def _make_conditions(self) -> str:
        if self.conditions is None:
            return ''
        s_condiciones: str = ' WHERE '
        if self.conditions is None:
            raise ValueError("No se han pasado condiciones.")
        for c in self.conditions:
            s_condicion: str = ''
            valor: str | list
            if c.operador == Operators.LIKE:
                s_left: str = c.like_left*'_' if c.like_left else '%'
                s_right: str = c.like_right*'_' if c.like_right else '%'
                valor = f'{s_left}{c.valor}{s_right}'
            else:
                valor = c.valor
            if c.negar:
                s_condicion += Operators.NOT.value

            if type(valor) == str:
                s_condicion += f' {c.columna} {c.operador.value} "{valor}" '
            else:
                s_valor: str = f'({",".join(valor)})'
                s_condicion += f' {c.columna} {c.operador.value} {s_valor} '
            if c.siguiente:
                s_condicion += c.siguiente.value
            s_condiciones += s_condicion

        return s_condiciones

    def _make_filters(self, fields: list[str],
                      tipo: str,
                      desc: bool | None = None
                      ) -> str:
        s_filter: str
        s_fields: str = ', '.join(fields)
        if not fields:
            raise ValueError("Debe proporcionar al menos un campo.")
        match tipo:
            case Filters.ORDER.value:
                s_order = ' DESC ' if desc else ' ASC '
                s_filter = ' ORDER BY ' + s_fields + s_order
            case Filters.GROUP.value:
                s_filter = ' GROUP BY ' + s_fields
            case _:
                raise ValueError("No se ha proporcionado un tipo de filtro.")
        return s_filter

    @abstractmethod
    def clean_query(self, query: str) -> str:
        query = re.sub(r'', '', query, flags=re.IGNORECASE)
        query = re.sub(r',+FROM', ' FROM', query, flags=re.IGNORECASE)
        query = re.sub(r'\s{2,}', ' ', query)
        query = re.sub(r'\s+;', ';', query)
        return query


class Delete(QueryBasics):
    def __init__(self, table: Tabla, conditions: list[Condition] | None = None) -> None:
        super().__init__(table, None, conditions)

    @property
    def query(self):
        query: str = f'DELETE FROM {self.table.value} {self._make_conditions()};'
        return self.clean_query(query)


class Insert(QueryBasics):
    def __init__(self,
                 table: Tabla,
                 columns: list[str],
                 values: list[list],
                 ) -> None:
        super().__init__(table, columns)
        self.values = values

    def format_values(self) -> str:
        s_values: str
        if self.values is None:
            raise ValueError("Debe ingresar valores para insertar.")
        n_cant_cols = len(self.columns) if self.columns else 0
        if not all(len(x) == n_cant_cols for x in self.values):
            debug(n_cant_cols)
            raise ValueError(
                "Verifique la cantidad de valores proporcionados con la cantidad de columnas.")

        s_values: str = ''
        for value in self.values:
            s_value: str = ' ( '
            s_value += ', '.join(value)
            s_value += ' ), '
            s_values += s_value
        return s_values[:len(s_values)-2]  # quito espacio y última coma

    @property
    def query(self):
        s_columns: str = self._format_columns()
        s_values: str = self.format_values()
        query: str = f'INSERT INTO {s_columns} VALUES {s_values};'

        return self.clean_query(query)


class Update(QueryBasics):
    def __init__(self,
                 table: Tabla,
                 column_values: list[list[str]],
                 conditions: list[Condition] | None = None,
                 ) -> None:
        super().__init__(table, None, conditions)
        self.values = column_values
        self.column_values = column_values

    def __format_set(self) -> str:
        s_format_set: str = ''
        for c, v in self.column_values:
            s_format_set += f' {c} = "{v}", '
        # quito espacio y última coma
        return s_format_set[:len(s_format_set)-2]

    @property
    def query(self):
        query: str = f'UPDATE {self.table.nombre} SET {self.__format_set()}'
        return self.clean_query(query)


class Select(QueryBasics):

    def __init__(self,
                 table: Tabla,
                 columns: list[str] | None = None,
                 aggregations: list[Aggregate] | None = None,
                 cases: list[Case] | None = None,
                 group: list[str] | None = None,
                 order: list[str] | None = None,
                 conditions: list[Condition] | None = None,
                 desc: bool | None = None,
                 distinct: bool | None = None,
                 limit: int | None = None,
                 ) -> None:
        super().__init__(table, columns, conditions)
        self.order = [
            clean(x) for x in order] if order is not None else None
        self.group = [
            clean(x) for x in group] if group is not None else None
        self.aggregations = aggregations
        self.cases = cases
        self.desc = desc
        self.distinct = distinct
        self.limit = limit

    def __str__(self) -> str:
        return self.query

    def __repr__(self) -> str:
        return self.__str__()

    def __format_aggregations(self) -> str:
        if self.aggregations is None:
            raise ValueError(
                'No puede formatear una lista vacía de "AGGREGATIONS".')
        else:
            return ', '.join([str(x) for x in self.aggregations])

    def __format_cases(self) -> str:
        if self.cases is None:
            raise ValueError('No puede formatear una lista vacía de "CASE".')
        else:
            return ', '.join(str(x) for x in self.cases)

    @property
    def query(self) -> str:
        s_distinct: str = ' DISTINCT ' if self.distinct else ''
        s_columnas: str = self._format_columns() if self.columns is not None else ' * '
        s_aggrs: str = self.__format_aggregations() if self.aggregations is not None else ''
        s_cases: str = self.__format_cases() if self.cases is not None else ''
        s_group: str = self._make_filters(
            self.group, Filters.GROUP.value) if self.group else ''
        s_order: str = self._make_filters(
            self.order, Filters.ORDER.value, self.desc) if self.order else ''
        s_limit: str = ' LIMIT ' + str(self.limit) if self.limit else ''

        query: str = f'SELECT {s_distinct} {s_columnas}, {s_aggrs}, {s_cases} FROM {self.table} {self._make_conditions()} {s_group} {s_order} {s_limit};'
        return self.clean_query(query)

    @query.setter
    def query(self, value: str):
        self.query = value
        self.query = value

    def join(self, o_join: Join) -> str:
        s_join = f' {o_join.tipo.value} JOIN {o_join.tabla} ON {self.table.value}.{o_join.columna_clave}={o_join.tabla}.{o_join.columna_clave}'
        s_result = self.query.replace(';', '') + s_join
        return s_result

    def union(self, query: str, duplicados: bool = False) -> str:
        union: str = 'UNION' if duplicados else 'UNION ALL'
        return f'{self.query} {union} {query}'


# * ===========================================================================

tabla = Tabla('auth_user', 'a')
columnas = ['id', 'username']
aggs = [Aggregate(Aggregations.COUNT, 'id')]
order = ['nombre']
desc = True
valores = [['Iván', 'Sayavedra'], ['Adrián', 'Ramírez']]
valores2 = [['col1', 'valor1'], ['col2', 'val2']]
# condiciones = ('nombre', 'igual', 'Iván')
condiciones: list[Condition]

condiciones = [
    Condition('nombre', Operators.IGUAL,
              'Iván', Operators.AND),
    Condition('nombre',
              Operators.DIFERENTE, 'Adrián'),
]
condicion = [Condition('nombre', Operators.LIKE, 'iv', None, False, None, 2)]
join = Join('personas', Joins.LEFT, 'id')
# query = Update(table=tabla, column_values=valores2,
#                conditions=condiciones).string
query = Insert(tabla, columnas, valores)
# query: str = Select(tabla).query

print('')
debug(query)
print('')

# conexion_data = {
#     'host': 'localhost',
#     'user': 'root',
#     'passwd': 'root01',
#     'db': 'wpruebas',
#     'port': 3306
# }

# conexion = pymysql.connect(**conexion_data)
# cursor = conexion.cursor()


# cursor.execute(query)

# for id, username in cursor.fetchall():
#     print(f'Usuario: {id} {username}')

# conexion.close()
