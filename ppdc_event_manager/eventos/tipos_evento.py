import datetime as dt
from enum import Enum


class TipoEvento(Enum):
    """Tipos de eventos en la simulación.
    Las clases tipo [Enum], que viene de "enumeración", tendrán valores que pueden ser
    utilizados sin instanciar, y que serán recurrentes en nuestro sistema.
    Se utilizan de manera muy similar a como utilizaríamos variables constantes
    (cuyos valores no cambian durante la ejecución).

    Ejemplo: Puedes utilizar [TipoEvento.GENERACION_DEMANDA] en el constructor de [Evento]
    para indicar a qué tipo de evento corresponde.
    """

    ### Hacia abajo se encuentran las descripciones para cada TipoEvento ###

    GENERACION_DEMANDA = "generacion_demanda"
    TREN_LLEGADA = "tren_llegada"
    MODIFICACION_SISTEMA = "modificacion_sistema"


""" === GENERACION_DEMANDA ===
        Ocurre cuando una estación genera clientes.

Datos:
----------
["id_estacion"]: int
    Corresponde con el identificador de la estación que debe generar
    clientes.
["fecha_previa"]: dt.datetime
    Fecha en la cual se encontraba el generador de la estación,
    desde la cual deben calcularse los minutos transcurridos.
["fecha_actual"]: dt.datetime
    Fecha a la cual se actualizará la estación. Junto a la fecha previa,
    podremos calcular la cantidad de minutos transcurridos.
"""


""" === TREN_LLEGADA ===
        Ocurre cuando un tren llega a una nueva estación.

Datos:
----------
["entidad"] = "Tren"
    Identifica el tipo de entidad en este evento. Para la llegada de un tren, trabajamos con un [Tren].
["id_tren"]: int
    El id identificador del tren.
["nombre_tren"]: str
    El nombre establecido del tren.
["id_estacion_origen"]: int
    Id identificador de la estación de origen.
["id_estacion_destino"]: int
    Id identificador de la estación destino.
"""


""" === MODIFICACION_SISTEMA ===
        Ocurre cuando el usuario crea o modifica componentes de la Simulación.

Datos:
----------
["entidad"]: str
    Se debe identificar la entidad que está siendo creada (como "Tren", "Estacion", etc).
...
    Lo que le sigue, es el resto de información necesaria para poder re-crear el evento.
"""
