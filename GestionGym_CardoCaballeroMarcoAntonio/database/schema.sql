-- Schema para la base de datos del gimnasio
-- Sistema de Gestión GymForTheMoment

-- Tabla de Clientes
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
    dni TEXT NOT NULL UNIQUE,
    nombre TEXT NOT NULL,
    telefono TEXT,
    email TEXT UNIQUE,
    fecha_registro DATE NOT NULL DEFAULT (date('now')),
    activo BOOLEAN DEFAULT 1,
    CHECK (length(dni) > 0),
    CHECK (length(nombre) > 0)
);

-- Tabla de Aparatos
CREATE TABLE IF NOT EXISTS aparatos (
    id_aparato INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL,
    descripcion TEXT,
    activo BOOLEAN DEFAULT 1,
    CHECK (length(nombre) > 0),
    CHECK (length(tipo) > 0)
);

-- Tabla de Reservas
CREATE TABLE IF NOT EXISTS reservas (
    id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    id_aparato INTEGER NOT NULL,
    dia_semana INTEGER NOT NULL CHECK (dia_semana BETWEEN 1 AND 5),
    hora_inicio TEXT NOT NULL,
    fecha_reserva DATE NOT NULL DEFAULT (date('now')),
    estado TEXT DEFAULT 'Activa' CHECK (estado IN ('Activa', 'Cancelada', 'Completada')),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    FOREIGN KEY (id_aparato) REFERENCES aparatos(id_aparato) ON DELETE RESTRICT,
    UNIQUE(id_aparato, dia_semana, hora_inicio)
);

-- Tabla de Recibos
CREATE TABLE IF NOT EXISTS recibos (
    id_recibo INTEGER PRIMARY KEY AUTOINCREMENT,
    id_cliente INTEGER NOT NULL,
    mes INTEGER NOT NULL CHECK (mes BETWEEN 1 AND 12),
    anio INTEGER NOT NULL CHECK (anio >= 2020),
    monto REAL NOT NULL CHECK (monto > 0),
    fecha_generacion DATE NOT NULL DEFAULT (date('now')),
    fecha_pago DATE,
    pagado BOOLEAN DEFAULT 0,
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente) ON DELETE CASCADE,
    UNIQUE(id_cliente, mes, anio)
);

-- Índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_reservas_cliente ON reservas(id_cliente);
CREATE INDEX IF NOT EXISTS idx_reservas_aparato ON reservas(id_aparato);
CREATE INDEX IF NOT EXISTS idx_reservas_dia_hora ON reservas(dia_semana, hora_inicio);
CREATE INDEX IF NOT EXISTS idx_recibos_cliente ON recibos(id_cliente);
CREATE INDEX IF NOT EXISTS idx_recibos_pagado ON recibos(pagado);
CREATE INDEX IF NOT EXISTS idx_clientes_dni ON clientes(dni);
CREATE INDEX IF NOT EXISTS idx_clientes_activo ON clientes(activo);

-- Vista para clientes morosos
CREATE VIEW IF NOT EXISTS vista_morosos AS
SELECT 
    c.id_cliente,
    c.dni,
    c.nombre,
    c.telefono,
    c.email,
    r.mes,
    r.anio,
    r.monto,
    r.fecha_generacion,
    julianday('now') - julianday(r.fecha_generacion) as dias_mora
FROM clientes c
INNER JOIN recibos r ON c.id_cliente = r.id_cliente
WHERE r.pagado = 0 AND c.activo = 1
ORDER BY r.anio DESC, r.mes DESC;

-- Vista para disponibilidad de aparatos
CREATE VIEW IF NOT EXISTS vista_disponibilidad AS
SELECT 
    a.id_aparato,
    a.nombre as nombre_aparato,
    a.tipo,
    r.dia_semana,
    r.hora_inicio,
    r.estado,
    c.nombre as nombre_cliente,
    c.dni
FROM aparatos a
LEFT JOIN reservas r ON a.id_aparato = r.id_aparato AND r.estado = 'Activa'
LEFT JOIN clientes c ON r.id_cliente = c.id_cliente
WHERE a.activo = 1
ORDER BY a.nombre, r.dia_semana, r.hora_inicio;
