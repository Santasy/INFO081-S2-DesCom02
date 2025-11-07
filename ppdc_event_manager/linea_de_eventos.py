import datetime as dt
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Iterable

from ppdc_event_manager.eventos import TipoEvento, Evento


class LineaDeEventos:
    """Esta instancia se encargará de administrar los eventos,
    que han ocurrido y los que están por ocurrir, de forma ordenada para tener un rápido
    acceso a los próximos eventos a ocurrir.
    Para eso también dejamos disponibles un enlace al [EstadoDeSimulacion], lo que nos permitirá
    tener acceso a todos los otros componentes que necesitemos.
    """

    def __init__(self, estado_simulacion: Any, fecha_inicial: dt.datetime):
        self.estado_simulacion: Any = estado_simulacion
        self.fecha_inicial = fecha_inicial
        self.fecha_actual = fecha_inicial

        self.eventos: list[Evento] = []
        self.historial_eventos: list[Evento] = []

    def __insertar_desde_final(self, lista_eventos: list[Evento], evento: Evento):
        """Esta función utilitaria nos sirve para insertar ordenadamente eventos, que posiblemente
        serán más actuales que los registrados.
        La idea es que sólo se utilicen internamente (desde dentro de la clase), no expuesta al usuario."""
        for i in range(len(lista_eventos) - 1, -1, -1):
            ev_en_lista = lista_eventos[i]
            if ev_en_lista.ocurrencia < evento.ocurrencia or (
                ev_en_lista.ocurrencia == evento.ocurrencia
                and ev_en_lista.prioridad < evento.prioridad
            ):
                lista_eventos.insert(i + 1, evento)
                return
        # Si no, lo ponemos al principio.
        lista_eventos.insert(0, evento)

    def __insertar_desde_inicio(self, lista_eventos: list[Evento], evento: Evento):
        """Esta función utilitaria nos sirve para insertar ordenadamente eventos, que posiblemente
        serán más próximos que los registrados.
        La idea es que sólo se utilicen internamente (desde dentro de la clase), no expuesta al usuario."""
        for i in range(len(lista_eventos)):
            ev_en_lista = lista_eventos[i]

            if ev_en_lista.ocurrencia > evento.ocurrencia or (
                ev_en_lista.ocurrencia == evento.ocurrencia
                and ev_en_lista.prioridad > evento.prioridad
            ):
                lista_eventos.insert(i, evento)
                return
        # Si no, lo ponemos al final.
        lista_eventos.append(evento)

    def insertar_evento_pasado(self, evento: Evento) -> None:
        self.__insertar_desde_final(self.historial_eventos, evento)

    def insertar_eventos_pasados(self, eventos: Iterable[Evento]) -> None:
        for e in eventos:
            self.insertar_evento_pasado(e)

    def insertar_evento_futuro(self, evento: Evento) -> None:
        self.__insertar_desde_inicio(self.eventos, evento)

    def obtener_proximos(self, eliminar: bool = True) -> list[Evento]:
        """Devolveremos los eventos sin ejecutar sus handlers,
        ni tampoco añadirlo al historial.
        Por defecto, también los eliminaremos de su lista.
        """
        if not self.eventos:
            return []
        out = [self.eventos[0]]
        fecha_proxima = out[0].ocurrencia
        i = 1
        while i < len(self.eventos) and self.eventos[i].ocurrencia == fecha_proxima:
            out.append(self.eventos[i])
            i += 1
        if eliminar:
            self.eventos = self.eventos[len(out) :]
        return out

    def consumir_eventos(
        self, eventos: list[Evento], historial: bool = True
    ) -> dt.datetime:
        """Los eventos deben ingresarse en orden ascendente. Por lo mismo,
        es recomendable que los consigan utilizando [self.obtener_proximos].

        Returns
        -------
        Entrega la fecha del evento más reciente.
        """
        if not eventos:
            return
        fecha_proxima_previa = eventos[0].ocurrencia
        for e in eventos:
            assert e.ocurrencia >= fecha_proxima_previa
            assert not e.ha_ocurrido

            e.ejecutar()
            fecha_proxima_previa = e.ocurrencia

            if historial:
                self.insertar_evento_pasado(e)
        return fecha_proxima_previa

    def crear_variante(self, fecha_hasta: Optional[dt.datetime]) -> "LineaDeEventos":
        nueva_linea = LineaDeEventos(self.estado_simulacion, self.fecha_inicial)

        if fecha_hasta is None:
            # Tomar todos los eventos
            nueva_linea.historial_eventos = self.historial_eventos.copy()
            nueva_linea.eventos = self.eventos.copy()
            nueva_linea.fecha_actual = self.fecha_actual
        else:
            # Tomar parcialmente los eventos
            nueva_linea.historial_eventos = [
                ev for ev in self.historial_eventos if ev.ocurrencia <= fecha_hasta
            ]
            nueva_linea.fecha_actual = fecha_hasta
            # Los eventos futuros se descartan (nueva línea temporal)
            nueva_linea.eventos = []

        return nueva_linea
