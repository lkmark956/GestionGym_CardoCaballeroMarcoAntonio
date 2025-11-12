# Diagrama de Casos de Uso - Sistema de Gestión de Gimnasio

## Actores

### Actor Principal: Administrador del Gimnasio
Persona encargada de gestionar todo el sistema del gimnasio.

## Casos de Uso

### CU-01: Gestionar Clientes
**Actor**: Administrador
**Descripción**: Permite crear, modificar, eliminar y consultar clientes.
**Precondiciones**: El administrador debe tener acceso al sistema.
**Flujo Principal**:
1. El administrador selecciona la opción "Gestión de Clientes"
2. El sistema muestra el listado de clientes existentes
3. El administrador puede:
   - Agregar nuevo cliente
   - Modificar datos de cliente existente
   - Eliminar cliente
   - Buscar cliente por nombre o DNI

**Postcondiciones**: Los datos del cliente quedan registrados en el sistema.

---

### CU-02: Gestionar Aparatos
**Actor**: Administrador
**Descripción**: Permite registrar y administrar los aparatos del gimnasio.
**Precondiciones**: El administrador debe tener acceso al sistema.
**Flujo Principal**:
1. El administrador selecciona "Gestión de Aparatos"
2. El sistema muestra el listado de aparatos
3. El administrador puede:
   - Registrar nuevo aparato con nombre y tipo
   - Modificar información del aparato
   - Eliminar aparato (si no tiene reservas activas)
   - Consultar aparatos disponibles

**Postcondiciones**: Los aparatos quedan registrados en el sistema.

---

### CU-03: Crear Reserva
**Actor**: Administrador
**Descripción**: Permite reservar un aparato para un cliente en un día y hora específicos.
**Precondiciones**: 
- Debe existir al menos un cliente registrado
- Debe existir al menos un aparato disponible
- El horario debe estar dentro del rango permitido (Lunes-Viernes, 24 horas)

**Flujo Principal**:
1. El administrador selecciona "Nueva Reserva"
2. Selecciona el cliente
3. Selecciona el día de la semana
4. Selecciona la hora de inicio
5. Selecciona el aparato deseado
6. El sistema valida disponibilidad
7. El sistema confirma la reserva

**Flujo Alternativo**:
- Si el aparato está ocupado, el sistema muestra mensaje de error
- Si es fin de semana, el sistema rechaza la reserva

**Postcondiciones**: La reserva queda registrada en el sistema.

---

### CU-04: Consultar Disponibilidad de Aparatos
**Actor**: Administrador
**Descripción**: Permite visualizar qué aparatos están ocupados en un día específico.
**Precondiciones**: Debe haber aparatos registrados.
**Flujo Principal**:
1. El administrador selecciona "Consultar Disponibilidad"
2. Selecciona el día de la semana
3. El sistema muestra un listado con:
   - Hora
   - Aparato
   - Estado (Libre/Ocupado)
   - Cliente (si está ocupado)

**Postcondiciones**: Se visualiza la información solicitada.

---

### CU-05: Cancelar Reserva
**Actor**: Administrador
**Descripción**: Permite eliminar una reserva existente.
**Precondiciones**: Debe existir al menos una reserva.
**Flujo Principal**:
1. El administrador busca la reserva
2. Selecciona la reserva a cancelar
3. Confirma la cancelación
4. El sistema elimina la reserva

**Postcondiciones**: La reserva se elimina y el horario queda disponible.

---

### CU-06: Generar Recibos Mensuales
**Actor**: Administrador
**Descripción**: Genera automáticamente todos los recibos del mes para los clientes.
**Precondiciones**: Debe haber clientes registrados.
**Flujo Principal**:
1. El administrador selecciona "Generar Recibos del Mes"
2. Selecciona el mes y año
3. El sistema crea un recibo para cada cliente activo
4. El sistema muestra confirmación del número de recibos generados

**Postcondiciones**: Se crean recibos pendientes de pago para todos los clientes.

---

### CU-07: Registrar Pago
**Actor**: Administrador
**Descripción**: Registra el pago de un cliente para un mes específico.
**Precondiciones**: Debe existir un recibo pendiente.
**Flujo Principal**:
1. El administrador selecciona "Registrar Pago"
2. Busca al cliente
3. Selecciona el recibo pendiente
4. Registra la fecha de pago
5. El sistema marca el recibo como pagado

**Postcondiciones**: El recibo queda marcado como pagado.

---

### CU-08: Consultar Clientes Morosos
**Actor**: Administrador
**Descripción**: Genera un listado de clientes con pagos pendientes.
**Precondiciones**: Deben existir recibos generados.
**Flujo Principal**:
1. El administrador selecciona "Clientes Morosos"
2. El sistema busca todos los recibos no pagados
3. El sistema muestra listado con:
   - Nombre del cliente
   - DNI
   - Mes/Año del recibo pendiente
   - Monto adeudado
   - Días de mora

**Postcondiciones**: Se visualiza el listado de morosos.

---

## Diagrama Visual de Casos de Uso (Representación en Texto)

```
                    ╔══════════════════════════════════╗
                    ║   Sistema Gestión Gimnasio      ║
                    ╠══════════════════════════════════╣
                    ║                                  ║
┌─────────────┐     ║  • CU-01: Gestionar Clientes    ║
│             │◄────╫  • CU-02: Gestionar Aparatos    ║
│Administrador│     ║  • CU-03: Crear Reserva         ║
│             │◄────╫  • CU-04: Consultar Disponib.   ║
└─────────────┘     ║  • CU-05: Cancelar Reserva      ║
                    ║  • CU-06: Generar Recibos       ║
                    ║  • CU-07: Registrar Pago        ║
                    ║  • CU-08: Consultar Morosos     ║
                    ║                                  ║
                    ╚══════════════════════════════════╝
```

## Relaciones entre Casos de Uso

### Includes (Incluye)
- CU-03 (Crear Reserva) <<include>> CU-04 (Consultar Disponibilidad)
- CU-07 (Registrar Pago) <<include>> CU-08 (Actualizar estado morosos)

### Extends (Extiende)
- CU-05 (Cancelar Reserva) <<extend>> CU-04 (Consultar Disponibilidad)
- CU-08 (Consultar Morosos) <<extend>> CU-07 (Registrar Pago)
