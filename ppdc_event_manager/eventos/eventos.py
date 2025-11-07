import datetime as dt
from enum import Enum
from typing import Any, Callable, Dict, List, Optional

from .tipos_evento import TipoEvento


class Evento:
    # Variable de la clase.
    # Con esto podemos conseguir el id desde la misma clase,
    # en vez de depender del [EstadoDeSimulacion].
    next_id_evento = 0

    def __init__(
        self,
        tipo: TipoEvento,
        ocurrencia: dt.datetime,
        handler: Callable,
        prioridad: int = 0,
        ha_ocurrido: bool = False,
    ) -> None:
        """
        Parameters
        ----------
        tipo: TipoEvento
            Utiliza los enum [TipoEvento], de manera de que no tenemos que inventar algún nombre
            para el evento.
        ocurrencia: dt.datetime
            Fecha exacta en la que debería ocurrir el evento.
        handler: Callable
            Está será la función que será ejecutada una vez el evento deba ocurrir.
        ha_ocurrido: bool = False
            Indica si efectivamente el evento ha sido procesado por la simulación. Esto indica
            que debería moverse al historial de eventos correspondiente.
        prioridad: int
            Valor que ayuda a ordenar eventos que tengan la misma fecha de ocurrencia.
            Mientras más cerca de 0, más adelante estará en la lista de eventos.

        Other attributes
        ----------
        id: int
            La clase Evento va a establecer un id para el evento,
            de esta manera podremos buscar el evento por su id de ser necesario.
            Esto es principalmente útil para el caso donde queramos cambiar el destino
            de un tren. Deberemos reemplazar su evento de llegada anterior,
            por el nuevo (a una estación distinta).

        datos: dict[str, Any]
            Diccionario disponible para agregar cualquier otro dato que sea necesario para su evento.
        """
        self.tipo: TipoEvento = tipo
        self.ocurrencia: dt.datetime = ocurrencia
        self.handler = handler

        self.ha_ocurrido: bool = ha_ocurrido
        self.prioridad: int = prioridad

        # Asignamos un id utilizando el atributo de la clase.
        self.id = Evento.next_id_evento
        Evento.next_id_evento += 1

        # Dejamos disponible un diccionario para datos adicionales.
        self.datos: dict[str, Any] = dict()

    def ejecutar(self):
        if self.ha_ocurrido:
            raise Exception(
                '[Error] No se puede ejecutar un evento que ya está marcado como "ocurrido".'
            )
        self.handler()
        self.ha_ocurrido = True
