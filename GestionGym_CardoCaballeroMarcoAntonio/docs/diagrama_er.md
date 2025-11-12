# Diagrama Entidad-Relación - Sistema de Gestión de Gimnasio

## Modelo Conceptual

### Entidades Principales

#### 1. CLIENTE
Representa a los usuarios del gimnasio.

**Atributos**:
- `id_cliente` (PK): Identificador único
- `dni`: Documento de identidad (UNIQUE)
- `nombre`: Nombre completo
- `telefono`: Número de contacto
- `email`: Correo electrónico (UNIQUE)
- `fecha_registro`: Fecha de alta en el sistema
- `activo`: Estado del cliente (booleano)

---

#### 2. APARATO
Representa los equipos de entrenamiento del gimnasio.

**Atributos**:
- `id_aparato` (PK): Identificador único
- `nombre`: Nombre del aparato
- `tipo`: Categoría del aparato (Cardio, Fuerza, etc.)
- `descripcion`: Descripción adicional
- `activo`: Estado del aparato (booleano)

---

#### 3. RESERVA
Representa las sesiones de entrenamiento programadas.

**Atributos**:
- `id_reserva` (PK): Identificador único
- `id_cliente` (FK): Referencia al cliente
- `id_aparato` (FK): Referencia al aparato
- `dia_semana`: Día (Lunes=1, Martes=2, ..., Viernes=5)
- `hora_inicio`: Hora de inicio (formato HH:MM)
- `fecha_reserva`: Fecha en que se hizo la reserva
- `estado`: Estado (Activa, Cancelada, Completada)

---

#### 4. RECIBO
Representa los pagos mensuales de los clientes.

**Atributos**:
- `id_recibo` (PK): Identificador único
- `id_cliente` (FK): Referencia al cliente
- `mes`: Mes del recibo (1-12)
- `anio`: Año del recibo
- `monto`: Cantidad a pagar
- `fecha_generacion`: Fecha de creación del recibo
- `fecha_pago`: Fecha en que se realizó el pago (NULL si no pagado)
- `pagado`: Estado del pago (booleano)

---

## Relaciones

### 1. CLIENTE ──(1:N)── RESERVA
- Un cliente puede tener múltiples reservas
- Una reserva pertenece a un solo cliente
- **Cardinalidad**: (1,N) del lado Cliente, (1,1) del lado Reserva

### 2. APARATO ──(1:N)── RESERVA
- Un aparato puede tener múltiples reservas
- Una reserva es para un solo aparato
- **Cardinalidad**: (1,N) del lado Aparato, (1,1) del lado Reserva

### 3. CLIENTE ──(1:N)── RECIBO
- Un cliente puede tener múltiples recibos
- Un recibo pertenece a un solo cliente
- **Cardinalidad**: (1,N) del lado Cliente, (1,1) del lado Recibo

---

## Diagrama E-R (Representación Visual)

```
┌─────────────────────────────────────────┐
│              CLIENTE                    │
├─────────────────────────────────────────┤
│ • id_cliente (PK)                       │
│ • dni (UNIQUE)                          │
│ • nombre                                │
│ • telefono                              │
│ • email (UNIQUE)                        │
│ • fecha_registro                        │
│ • activo                                │
└──────────────┬──────────────────────────┘
               │ 1
               │
               │ N
┌──────────────┴──────────────────────────┐
│              RESERVA                    │
├─────────────────────────────────────────┤
│ • id_reserva (PK)                       │
│ • id_cliente (FK)                       │
│ • id_aparato (FK)                       │
│ • dia_semana                            │
│ • hora_inicio                           │
│ • fecha_reserva                         │
│ • estado                                │
└──────────────┬──────────────────────────┘
               │ N
               │
               │ 1
┌──────────────┴──────────────────────────┐
│              APARATO                    │
├─────────────────────────────────────────┤
│ • id_aparato (PK)                       │
│ • nombre                                │
│ • tipo                                  │
│ • descripcion                           │
│ • activo                                │
└─────────────────────────────────────────┘


┌─────────────────────────────────────────┐
│              CLIENTE                    │
└──────────────┬──────────────────────────┘
               │ 1
               │
               │ N
┌──────────────┴──────────────────────────┐
│              RECIBO                     │
├─────────────────────────────────────────┤
│ • id_recibo (PK)                        │
│ • id_cliente (FK)                       │
│ • mes                                   │
│ • anio                                  │
│ • monto                                 │
│ • fecha_generacion                      │
│ • fecha_pago                            │
│ • pagado                                │
└─────────────────────────────────────────┘
```

---

## Restricciones y Reglas de Negocio

### Restricciones de Integridad

1. **Unicidad de DNI y Email**: No pueden existir dos clientes con el mismo DNI o email
2. **Unicidad de Reserva**: No puede haber dos reservas para el mismo aparato, día y hora
3. **Unicidad de Recibo**: Un cliente no puede tener dos recibos para el mismo mes/año
4. **Integridad Referencial**: Si se elimina un cliente, se deben manejar sus reservas y recibos

### Reglas de Negocio

1. **RN-01**: Las reservas solo pueden hacerse de Lunes (1) a Viernes (5)
2. **RN-02**: Las sesiones tienen duración fija de 30 minutos
3. **RN-03**: Las horas de inicio válidas son: 00:00, 00:30, 01:00, ..., 23:30
4. **RN-04**: Un cliente es moroso si tiene recibos con `pagado = False`
5. **RN-05**: El monto de todos los recibos es igual (mensualidad fija)
6. **RN-06**: Los recibos se generan automáticamente al inicio de cada mes
7. **RN-07**: No se pueden crear reservas para aparatos inactivos
8. **RN-08**: No se pueden generar recibos para clientes inactivos

---

## Modelo Relacional Normalizado (3FN)

### Tabla: clientes
```sql
CREATE TABLE clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    dni TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    telefono TEXT,
    email TEXT UNIQUE,
    fecha_registro DATE NOT NULL,
    activo BOOLEAN DEFAULT 1
);
```

### Tabla: aparatos
```sql
CREATE TABLE aparatos (
    id_aparato INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT 1
);
```

### Tabla: reservas
```sql
CREATE TABLE reservas (
    id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    id_aparato INTEGER NOT NULL,
    dia_semana INTEGER NOT NULL CHECK (dia_semana BETWEEN 1 AND 5),
    hora_inicio TIME NOT NULL,
    fecha_reserva DATE NOT NULL,
    estado TEXT DEFAULT 'Activa',
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_aparato) REFERENCES aparatos(id_aparato),
    UNIQUE(id_aparato, dia_semana, hora_inicio)
);
```

### Tabla: recibos
```sql
CREATE TABLE recibos (
    id_recibo INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    mes INTEGER NOT NULL CHECK (mes BETWEEN 1 AND 12),
    anio INTEGER NOT NULL,
    monto REAL NOT NULL,
    fecha_generacion DATE NOT NULL,
    fecha_pago DATE,
    pagado BOOLEAN DEFAULT 0,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    UNIQUE(id_cliente, mes, anio)
);
```

---

## Análisis de Normalización

### Primera Forma Normal (1FN)
✓ Todos los atributos contienen valores atómicos
✓ No hay grupos repetitivos

### Segunda Forma Normal (2FN)
✓ Cumple 1FN
✓ Todos los atributos no clave dependen completamente de la clave primaria

### Tercera Forma Normal (3FN)
✓ Cumple 2FN
✓ No existen dependencias transitivas
✓ Cada atributo no clave depende directamente de la clave primaria

### Conclusión
El modelo está completamente normalizado en 3FN, eliminando redundancias y anomalías de actualización.
