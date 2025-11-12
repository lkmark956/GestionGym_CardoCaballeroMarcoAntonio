# Sistema de Gestión de Gimnasio - GymForTheMoment

## Descripción del Proyecto

Sistema de gestión para gimnasio 24/7 (Lunes a Viernes) que permite:
- Gestión de clientes y membresías
- Reserva de aparatos de entrenamiento por sesiones de 30 minutos
- Control de pagos mensuales y detección de morosos
- Visualización de disponibilidad de aparatos por día

## Requisitos Funcionales

### RF-01: Gestión de Clientes
- Registrar nuevos clientes con datos personales
- Modificar información de clientes existentes
- Eliminar clientes del sistema
- Consultar listado de todos los clientes

### RF-02: Gestión de Aparatos
- Registrar aparatos de entrenamiento
- Identificar cada aparato de forma única
- Consultar listado de aparatos disponibles

### RF-03: Gestión de Reservas
- Crear reservas de aparatos para sesiones de 30 minutos
- Cancelar reservas existentes
- Consultar disponibilidad de aparatos por día y hora
- Generar listado de ocupación por día de la semana

### RF-04: Gestión de Pagos
- Generar recibos mensuales automáticamente
- Registrar pagos de clientes
- Consultar estado de pagos
- Generar listado de clientes morosos

## Características Técnicas

- **Base de Datos**: SQLite
- **Interfaz**: CustomTkinter (moderna y responsive)
- **Lenguaje**: Python 3.x
- **Arquitectura**: MVC (Model-View-Controller)

## Estructura del Proyecto

```
ProyectoGym/
│
├── database/
│   ├── __init__.py
│   ├── db_manager.py
│   └── schema.sql
│
├── models/
│   ├── __init__.py
│   ├── cliente.py
│   ├── aparato.py
│   ├── reserva.py
│   └── pago.py
│
├── views/
│   ├── __init__.py
│   ├── main_window.py
│   ├── clientes_view.py
│   ├── aparatos_view.py
│   ├── reservas_view.py
│   └── pagos_view.py
│
├── controllers/
│   ├── __init__.py
│   ├── cliente_controller.py
│   ├── aparato_controller.py
│   ├── reserva_controller.py
│   └── pago_controller.py
│
├── utils/
│   ├── __init__.py
│   └── validators.py
│
├── docs/
│   ├── casos_de_uso.md
│   ├── diagrama_er.md
│   └── manual_usuario.md
│
├── requirements.txt
├── main.py
└── README.md
```

## Instalación

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

## Horario de Operación

- **Días**: Lunes a Viernes
- **Horario**: 24 horas (00:00 - 23:59)
- **Duración de sesiones**: 30 minutos
- **Sesiones disponibles por día**: 48 (24 horas × 2 sesiones/hora)

## Modelo de Negocio

- Mensualidad fija para todos los clientes
- Pago mensual independiente de la actividad realizada
- Generación automática de recibos al inicio de cada mes
