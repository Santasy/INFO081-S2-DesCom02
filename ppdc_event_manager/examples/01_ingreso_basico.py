import datetime as dt

from ppdc_event_manager import LineaDeEventos

from dummy_classes import EstadoDeSimulacion

if __name__ == "__main__":
    # Nuestro estado principal:
    estado = EstadoDeSimulacion(dt.datetime(2025, 1, 1, 7, 0))

    # Crearé dos estaciones, y un tren que comienza en la primera.
    e1 = estado.crear_estacion_dummy("Ferroviario Valdivia")
    e2 = estado.crear_estacion_dummy("Ferroviario Bio-Bio")
    tren = estado.crear_tren_dummy()

    estado.conectar_estaciones(e1, e2)
    e1.anden_a.tren = tren

    estado.agendar_tren_llegada(tren, e2.id)

    fecha_prev = estado.fecha_actual
    print("Fecha inicial:", fecha_prev)
    assert e1.anden_a.tren == tren

    eventos = estado.avanzar_simulacion()
    print("Fecha nueva  :", estado.fecha_actual)
    assert fecha_prev != estado.fecha_actual

    __tren_esta_en_e1 = (e1.anden_a is not None and e1.anden_a.tren == tren) or (
        e1.anden_b is not None and e1.anden_b.tren == tren
    )
    __tren_esta_en_e2 = (e2.anden_a is not None and e2.anden_a.tren == tren) or (
        e2.anden_b is not None and e2.anden_b.tren == tren
    )
    assert __tren_esta_en_e1 and not __tren_esta_en_e2

    print("¡El ejemplo terminó correctamente!")
