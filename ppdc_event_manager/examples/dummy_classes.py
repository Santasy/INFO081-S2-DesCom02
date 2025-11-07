import datetime as dt
from typing import Any, Callable, Dict, List, Optional

from ppdc_event_manager import LineaDeEventos, Evento, TipoEvento


class Via:
    """Corresponde con una vía entre estaciones."""

    def __init__(self, id: int, estacion_a: Any, estacion_b: Any):
        self.id = id
        self.estacion_a = estacion_a
        self.estacion_b = estacion_b


class Anden:
    """Corresponde con un andén dentro de una estación.
    Puede salir hacia dos rutas."""

    def __init__(self, id: int, via_a: Via, via_b: Optional[Via]) -> None:
        """Para su creación requerimos al menos una vía."""
        self.id = id
        self.via_a: Optional[Via] = via_a
        self.via_b: Optional[Via] = via_b
        self.tren: Optional[Tren] = None

    def tiene_tren(self) -> bool:
        return self.tren is not None


class Estacion:
    def __init__(
        self,
        id: int,
        nombre: str,
        poblacion: int,
        hora_inicio: dt.time,
        hora_final: dt.time,
        usa_via_norte_sur: bool = True,
    ):
        """[Estacion] implementa el uso de dos atributos [Via]s.
        parameters
        ----------
        usa_via_norte_sur: bool
            Usar con True si la estación orienta sus vías hacia el norte y el sur.
            Sino, se interpreta que sus vías son este-oeste.

        """
        self.id = id
        self.nombre = nombre
        self.poblacion = poblacion
        self.hora_inicio = hora_inicio
        self.hora_final = hora_final
        self.usa_via_norte_sur = usa_via_norte_sur

        self.generador = ...  # TODO: Vincular a generador.

        # El uso de vías podría ser un arreglo para permitir más andenes.
        self.anden_a: Optional[Anden] = None
        self.anden_b: Optional[Anden] = None

    def asignar_via(self, via: Via) -> bool:
        """Asigna una vía a la estación.

        Returns:
            True si se asignó exitosamente, False si no hay espacio disponible.
        """
        # Intentar asignar en el primer andén disponible
        if self.anden_a is None:
            self.anden_a = Anden(id=0, via_a=via, via_b=None)
            return True
        elif self.anden_a.via_b is None:
            self.anden_a.via_b = via
            return True
        elif self.anden_b is None:
            self.anden_b = Anden(id=1, via_a=via, via_b=None)
            return True
        elif self.anden_b.via_b is None:
            self.anden_b.via_b = via
            return True

        return False


class Tren:
    def __init__(
        self,
        id: int,
        id_estacion: int,
        nombre: Optional[str],
        id_evento_siguiente: Optional[int],
    ):
        self.id: int = 0
        self.id_estacion: int = id_estacion

        self.nombre: str = nombre
        if nombre is None:
            self.nombre = f"Tren {id}"

        self.id_evento_siguiente: Optional[int] = id_evento_siguiente


class EstadoDeSimulacion:
    def __init__(self, fecha_inicial: dt.datetime):
        self.fecha_inicial = fecha_inicial
        self.fecha_actual = fecha_inicial

        self.admin_eventos: LineaDeEventos = LineaDeEventos(
            self,
            fecha_inicial,
        )

        self.estaciones: dict[int, Estacion] = dict()
        self.next_id_estaciones: int = 0

        self.trenes: dict[int, Tren] = dict()
        self.next_id_trenes: int = 0

        self.next_id_vias: int = 0

    def crear_estacion_dummy(
        self, nombre: str = "Ferroviario Valdivia", poblacion: int = 100_000
    ) -> Estacion:
        estacion = Estacion(
            id=self.next_id_estaciones,
            nombre=nombre,
            poblacion=poblacion,
            hora_inicio=dt.time(7, 0),
            hora_final=dt.time(20, 0),
        )
        self.next_id_estaciones += 1
        self.estaciones[estacion.id] = estacion

        # Ahora creamos el evento:
        evento = Evento(
            TipoEvento.MODIFICACION_SISTEMA,
            self.fecha_actual,
            lambda: print("[LOG] ¡Evento de creación de Estación!"),
            ha_ocurrido=True,
        )
        # Con todos los atributos adicionales que necesite el evento:
        evento.datos["entidad"] = "Estacion"
        evento.datos["nombre"] = estacion.nombre
        evento.datos["poblacion"] = estacion.poblacion
        evento.datos["hora_inicio"] = estacion.hora_inicio
        evento.datos["hora_final"] = estacion.hora_final
        evento.datos["id"] = estacion.id

        self.admin_eventos.insertar_evento_pasado(evento)

        return estacion

    def crear_tren_dummy(self, nombre: str = "Trenesito") -> Tren:
        # Crearemos un tren en la primera estación configurada.
        assert len(self.estaciones) > 0
        e1 = self.estaciones[0]

        tren = Tren(self.next_id_trenes, e1.id, nombre, None)
        self.next_id_trenes += 1
        self.trenes[tren.id] = tren

        # Ahora creamos el evento:
        evento = Evento(
            TipoEvento.MODIFICACION_SISTEMA,
            self.fecha_actual,
            lambda: print("[LOG] ¡Evento de creación de Tren!"),
            ha_ocurrido=True,
        )
        # Con todos los atributos adicionales que necesite el evento:
        evento.datos["entidad"] = "Tren"
        evento.datos["id"] = tren.id
        evento.datos["nombre"] = tren.nombre
        evento.datos["id_estacion"] = tren.id_estacion
        evento.datos["id_evento_siguiente"] = tren.id_evento_siguiente

        self.admin_eventos.insertar_evento_pasado(evento)

        return tren

    def conectar_estaciones(self, estacion_a: Estacion, estacion_b: Estacion):
        """Conecta dos estaciones mediante una vía bidireccional.
        La vía se asigna en via_a de una estación y via_b de la otra."""
        # Crear la vía
        via = Via(id=self.next_id_vias, estacion_a=estacion_a, estacion_b=estacion_b)
        self.next_id_vias += 1

        ### TODO: Esta lógica se puede mejorar notablemente.

        # Asignar la vía: via_a en estacion_a
        if estacion_a.anden_a is None:
            estacion_a.anden_a = Anden(id=0, via_a=via, via_b=None)
        elif estacion_a.anden_a.via_b is None:
            estacion_a.anden_a.via_b = via
        elif estacion_a.anden_b is None:
            estacion_a.anden_b = Anden(id=1, via_a=via, via_b=None)
        elif estacion_a.anden_b.via_b is None:
            estacion_a.anden_b.via_b = via
        else:
            return None  # No hay espacio

        # Asignar la vía: via_b en estacion_b
        if estacion_b.anden_a is None:
            estacion_b.anden_a = Anden(id=0, via_a=None, via_b=via)
        elif estacion_b.anden_a.via_a is None:
            estacion_b.anden_a.via_a = via
        elif estacion_b.anden_b is None:
            estacion_b.anden_b = Anden(id=1, via_a=None, via_b=via)
        elif estacion_b.anden_b.via_a is None:
            estacion_b.anden_b.via_a = via
        else:
            return None  # No hay espacio

        # Crear evento de conexión
        evento = Evento(
            TipoEvento.MODIFICACION_SISTEMA,
            self.fecha_actual,
            lambda: print(
                f"[LOG] ¡Evento de conexión de Estaciones {estacion_a.nombre} - {estacion_b.nombre}!"
            ),
            ha_ocurrido=True,
        )
        evento.datos["entidad"] = "Via"
        evento.datos["id"] = via.id
        evento.datos["estacion_a_id"] = estacion_a.id
        evento.datos["estacion_b_id"] = estacion_b.id

        self.admin_eventos.insertar_evento_pasado(evento)

        return via

    def agendar_tren_llegada(self, tren: Tren, id_estacion_destino: int) -> Evento:
        """Programa el movimiento de un tren hacia una estación destino.
        Crea un evento TREN_LLEGADA para 60 minutos después."""
        # Momento de llegada: 60 minutos después del tiempo actual
        momento_llegada = self.fecha_actual + dt.timedelta(minutes=60)

        # Crear evento de llegada
        evento = Evento(
            TipoEvento.TREN_LLEGADA,
            momento_llegada,
            lambda: print(
                f"[LOG] ¡Tren {tren.nombre} llegó a estación {id_estacion_destino}!"
            ),
            ha_ocurrido=False,
        )
        evento.datos["entidad"] = "Tren"
        evento.datos["id_tren"] = tren.id
        evento.datos["nombre_tren"] = tren.nombre
        evento.datos["id_estacion_origen"] = tren.id_estacion
        evento.datos["id_estacion_destino"] = id_estacion_destino

        # Insertar evento futuro sin avanzar el tiempo
        self.admin_eventos.insertar_evento_futuro(evento)

        return evento

    def avanzar_simulacion(self) -> List[Evento]:
        """Esta función se encarga de conseguir los próximos eventos a ocurrir,
        obteniendo todos los que comparten la misma hora de ocurrencia.
        Estos eventos son consumidos, y luego actualizamos la hora del
        [EstadoDeSimulacion].

        Returns
        -------
        Entrega los eventos que fueron consumidos.
        """
        eventos = self.admin_eventos.obtener_proximos()
        fecha_proxima = self.admin_eventos.consumir_eventos(eventos)
        # Actualiza la fecha.
        self.fecha_actual = fecha_proxima
        return eventos
