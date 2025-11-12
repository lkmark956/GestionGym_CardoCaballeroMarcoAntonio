# Manual de Usuario - Sistema de Gestión de Gimnasio

## Índice
1. [Introducción](#introducción)
2. [Instalación](#instalación)
3. [Inicio de la Aplicación](#inicio-de-la-aplicación)
4. [Gestión de Clientes](#gestión-de-clientes)
5. [Gestión de Aparatos](#gestión-de-aparatos)
6. [Gestión de Reservas](#gestión-de-reservas)
7. [Gestión de Pagos](#gestión-de-pagos)
8. [Solución de Problemas](#solución-de-problemas)

---

## Introducción

Bienvenido al Sistema de Gestión de Gimnasio **GymForTheMoment**. Esta aplicación le permite gestionar de forma eficiente:

- 👥 **Clientes**: Registro y administración de miembros
- 🏋️ **Aparatos**: Catálogo de equipos de entrenamiento
- 📅 **Reservas**: Programación de sesiones de 30 minutos
- 💰 **Pagos**: Control de mensualidades y morosos

### Características Principales
- Interfaz moderna y responsive
- Base de datos SQLite local
- Operación 24 horas (Lunes a Viernes)
- Sesiones de 30 minutos
- Mensualidad fija para todos los clientes

---

## Instalación

### Requisitos Previos
- Python 3.8 o superior
- Sistema operativo: Windows, macOS o Linux

### Pasos de Instalación

1. **Abrir terminal/PowerShell** en la carpeta del proyecto

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verificar instalación**:
   - Se instalarán: CustomTkinter 5.2.1 y Pillow 10.1.0
   - La base de datos se creará automáticamente al ejecutar la aplicación

---

## Inicio de la Aplicación

### Ejecutar la Aplicación

En la terminal, ejecute:

```bash
python main.py
```

### Pantalla de Inicio

Al abrir la aplicación verá:

- **Panel de Control** con estadísticas generales:
  - Total de clientes activos
  - Aparatos disponibles
  - Reservas activas
  - Pagos pendientes
  - Ingresos del mes

- **Menú lateral** con opciones:
  - 🏠 Inicio
  - 👥 Clientes
  - 🏋️ Aparatos
  - 📅 Reservas
  - 💰 Pagos

---

## Gestión de Clientes

### Agregar un Cliente

1. Haga clic en **👥 Clientes** en el menú lateral
2. Complete el formulario:
   - **DNI** * (obligatorio): Documento único
   - **Nombre Completo** * (obligatorio)
   - **Teléfono** (opcional)
   - **Email** (opcional)
3. Haga clic en **💾 Guardar**

### Buscar Clientes

- Utilice la barra de búsqueda en la parte superior derecha
- Escriba el nombre o DNI del cliente
- Los resultados se filtran automáticamente

### Editar un Cliente

1. Busque el cliente en la lista
2. Haga clic en el botón **✏️** (editar)
3. Modifique los datos en el formulario
4. Haga clic en **💾 Actualizar**

### Desactivar un Cliente

1. Seleccione el cliente a desactivar
2. Haga clic en **❌ Desactivar**
3. Confirme la acción

**Nota**: Los clientes desactivados no aparecen en las listas pero sus datos permanecen en el sistema.

---

## Gestión de Aparatos

### Agregar un Aparato

1. Haga clic en **🏋️ Aparatos** en el menú
2. Complete el formulario:
   - **Nombre del Aparato** * (ej: "Cinta de Correr #1")
   - **Tipo** * (Cardio, Fuerza, Funcional, etc.)
   - **Descripción** (opcional)
3. Haga clic en **💾 Guardar**

### Visualizar Aparatos

Los aparatos se organizan automáticamente por tipo:
- 🏋️ Cardio
- 🏋️ Fuerza
- 🏋️ Funcional
- 🏋️ Estiramiento
- 🏋️ Otro

### Editar un Aparato

1. Busque el aparato en la lista
2. Haga clic en **✏️**
3. Modifique los datos
4. Haga clic en **💾 Actualizar**

### Desactivar un Aparato

1. Seleccione el aparato
2. Haga clic en **❌ Desactivar**
3. Confirme

**Importante**: No se pueden desactivar aparatos con reservas activas.

---

## Gestión de Reservas

### Crear una Reserva

1. Haga clic en **📅 Reservas**
2. Complete el formulario:
   - **Cliente**: Seleccione de la lista
   - **Día de la Semana**: Lunes a Viernes
   - **Hora de Inicio**: Seleccione hora y minuto (00 o 30)
   - **Aparato**: Seleccione el equipo
3. (Opcional) Haga clic en **🔍 Verificar Disponibilidad**
4. Haga clic en **📅 Crear Reserva**

### Verificar Disponibilidad

Antes de crear una reserva:
1. Seleccione día, hora y aparato
2. Haga clic en **🔍 Verificar Disponibilidad**
3. El sistema mostrará:
   - ✅ **Disponible**: Puede crear la reserva
   - ❌ **Ocupado**: Elija otro horario

### Consultar Reservas por Día

1. En el panel derecho, seleccione el día de la semana
2. Haga clic en **🔄** para actualizar
3. Verá todas las reservas del día ordenadas por hora

### Cancelar una Reserva

1. Busque la reserva en la lista
2. Haga clic en **❌** (cancelar)
3. Confirme la acción

**Nota**: Las sesiones duran 30 minutos. Una sesión a las 09:00 termina a las 09:30.

---

## Gestión de Pagos

### Generar Recibos Mensuales

**¿Cuándo hacerlo?** Al inicio de cada mes para cobrar la mensualidad.

1. Haga clic en **💰 Pagos**
2. En "Generar Recibos Mensuales":
   - Seleccione **Mes**
   - Seleccione **Año**
   - Ingrese **Monto Mensual** (ej: 5000)
3. Haga clic en **📋 Generar Recibos**
4. Confirme la acción

El sistema creará automáticamente un recibo para cada cliente activo.

### Registrar un Pago

1. En la sección "Registrar Pago":
   - Seleccione el **Cliente**
   - El sistema cargará automáticamente sus recibos pendientes
   - Seleccione el **Recibo Pendiente**
2. Haga clic en **💰 Registrar Pago**
3. Confirme

### Consultar Clientes Morosos

1. Vaya a la pestaña **⚠️ Clientes Morosos**
2. Verá una lista con:
   - Nombre y DNI del cliente
   - Teléfono de contacto
   - Deuda total
   - Detalle de cada recibo pendiente
   - Días de mora

**Código de colores**:
- 🟠 **Naranja**: Cliente con deuda

### Ver Todos los Recibos

1. Vaya a la pestaña **📋 Todos los Recibos**
2. Use el filtro:
   - **Todos**: Muestra todos los recibos
   - **Pendientes**: Solo recibos sin pagar
   - **Pagados**: Solo recibos pagados
3. Haga clic en **🔄** para actualizar

**Iconos**:
- ✅ Recibo pagado
- ⏳ Recibo pendiente

---

## Solución de Problemas

### Error: "La base de datos no se puede abrir"

**Solución**:
- Verifique que tenga permisos de escritura en la carpeta
- Cierre otras instancias de la aplicación

### Error: "No se puede crear la reserva"

**Causas posibles**:
- El aparato ya está reservado en ese horario
- El día seleccionado es fin de semana
- El cliente o aparato está desactivado

**Solución**:
- Verifique disponibilidad antes de crear
- Seleccione un día entre Lunes y Viernes

### Error: "No se pueden generar recibos"

**Causa**: Los clientes ya tienen recibos para ese mes/año

**Solución**: Solo se pueden generar recibos una vez por mes/año por cliente

### La aplicación está lenta

**Soluciones**:
- Cierre y reabra la aplicación
- Verifique que no haya muchas aplicaciones abiertas
- Si tiene muchos registros (miles), considere archivar datos antiguos

### Error al instalar CustomTkinter

**Solución**:
```bash
pip install --upgrade pip
pip install customtkinter pillow
```

### No aparecen los datos

**Solución**:
- Haga clic en el botón **🔄 Actualizar**
- Verifique que los filtros de búsqueda no estén limitando los resultados

---

## Consejos de Uso

### Mejores Prácticas

1. **Genere recibos al inicio de cada mes**
   - Facilita el control de pagos

2. **Revise clientes morosos regularmente**
   - Contacte a clientes con pagos atrasados

3. **Nombre los aparatos de forma única**
   - Use números o ubicaciones (ej: "Cinta #1", "Bicicleta Sala A")

4. **Verifique disponibilidad antes de reservar**
   - Evita errores y ahorra tiempo

5. **Mantenga actualizada la información de contacto**
   - Facilita la comunicación con clientes morosos

### Atajos Útiles

- **Buscar cliente**: Escriba directamente en la barra de búsqueda
- **Actualizar listas**: Use el botón 🔄 en cualquier vista
- **Formularios**: Use Tab para navegar entre campos

---

## Soporte

Para consultas o problemas adicionales:
- Revise la documentación en la carpeta `docs/`
- Consulte el archivo README.md
- Contacte al administrador del sistema

---

**GymForTheMoment v1.0**  
Sistema de Gestión de Gimnasio  
© 2025
