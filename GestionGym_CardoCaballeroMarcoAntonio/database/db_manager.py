"""
Gestor de Base de Datos para el Sistema de Gimnasio
Maneja todas las operaciones con SQLite
"""

import sqlite3
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple, Any


class DatabaseManager:
    """Clase para gestionar todas las operaciones con la base de datos"""
    
    def __init__(self, db_path: str = "gimnasio.db"):
        """
        Inicializa el gestor de base de datos
        
        Args:
            db_path: Ruta al archivo de base de datos SQLite
        """
        self.db_path = db_path
        self.connection = None
        self._initialize_database()
    
    def _initialize_database(self):
        """Inicializa la base de datos con el esquema"""
        # Leer el esquema SQL
        schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
        
        with sqlite3.connect(self.db_path) as conn:
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            conn.executescript(schema_sql)
            conn.commit()
    
    def get_connection(self) -> sqlite3.Connection:
        """Obtiene una conexión a la base de datos"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Para acceder a columnas por nombre
        return conn
    
    # ==================== CLIENTES ====================
    
    def crear_cliente(self, dni: str, nombre: str, telefono: str = "", 
                      email: str = "") -> int:
        """
        Crea un nuevo cliente
        
        Returns:
            ID del cliente creado
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO clientes (dni, nombre, telefono, email, fecha_registro)
                VALUES (?, ?, ?, ?, date('now'))
            """, (dni, nombre, telefono, email))
            conn.commit()
            return cursor.lastrowid
    
    def obtener_cliente(self, id_cliente: int) -> Optional[Dict]:
        """Obtiene un cliente por su ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes WHERE id_cliente = ?", (id_cliente,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def obtener_todos_clientes(self, solo_activos: bool = True) -> List[Dict]:
        """Obtiene todos los clientes"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if solo_activos:
                cursor.execute("SELECT * FROM clientes WHERE activo = 1 ORDER BY nombre")
            else:
                cursor.execute("SELECT * FROM clientes ORDER BY nombre")
            return [dict(row) for row in cursor.fetchall()]
    
    def actualizar_cliente(self, id_cliente: int, nombre: str = None, 
                          telefono: str = None, email: str = None) -> bool:
        """Actualiza los datos de un cliente"""
        updates = []
        params = []
        
        if nombre is not None:
            updates.append("nombre = ?")
            params.append(nombre)
        if telefono is not None:
            updates.append("telefono = ?")
            params.append(telefono)
        if email is not None:
            updates.append("email = ?")
            params.append(email)
        
        if not updates:
            return False
        
        params.append(id_cliente)
        query = f"UPDATE clientes SET {', '.join(updates)} WHERE id_cliente = ?"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
    
    def desactivar_cliente(self, id_cliente: int) -> bool:
        """Desactiva un cliente (no lo elimina)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE clientes SET activo = 0 WHERE id_cliente = ?", 
                          (id_cliente,))
            conn.commit()
            return cursor.rowcount > 0
    
    def buscar_clientes(self, termino: str) -> List[Dict]:
        """Busca clientes por nombre o DNI"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM clientes 
                WHERE (nombre LIKE ? OR dni LIKE ?) AND activo = 1
                ORDER BY nombre
            """, (f"%{termino}%", f"%{termino}%"))
            return [dict(row) for row in cursor.fetchall()]
    
    # ==================== APARATOS ====================
    
    def crear_aparato(self, nombre: str, tipo: str, descripcion: str = "") -> int:
        """Crea un nuevo aparato"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO aparatos (nombre, tipo, descripcion)
                VALUES (?, ?, ?)
            """, (nombre, tipo, descripcion))
            conn.commit()
            return cursor.lastrowid
    
    def obtener_aparato(self, id_aparato: int) -> Optional[Dict]:
        """Obtiene un aparato por su ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM aparatos WHERE id_aparato = ?", (id_aparato,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def obtener_todos_aparatos(self, solo_activos: bool = True) -> List[Dict]:
        """Obtiene todos los aparatos"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if solo_activos:
                cursor.execute("SELECT * FROM aparatos WHERE activo = 1 ORDER BY tipo, nombre")
            else:
                cursor.execute("SELECT * FROM aparatos ORDER BY tipo, nombre")
            return [dict(row) for row in cursor.fetchall()]
    
    def actualizar_aparato(self, id_aparato: int, nombre: str = None,
                          tipo: str = None, descripcion: str = None) -> bool:
        """Actualiza los datos de un aparato"""
        updates = []
        params = []
        
        if nombre is not None:
            updates.append("nombre = ?")
            params.append(nombre)
        if tipo is not None:
            updates.append("tipo = ?")
            params.append(tipo)
        if descripcion is not None:
            updates.append("descripcion = ?")
            params.append(descripcion)
        
        if not updates:
            return False
        
        params.append(id_aparato)
        query = f"UPDATE aparatos SET {', '.join(updates)} WHERE id_aparato = ?"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return cursor.rowcount > 0
    
    def desactivar_aparato(self, id_aparato: int) -> bool:
        """Desactiva un aparato"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE aparatos SET activo = 0 WHERE id_aparato = ?", 
                          (id_aparato,))
            conn.commit()
            return cursor.rowcount > 0
    
    # ==================== RESERVAS ====================
    
    def crear_reserva(self, id_cliente: int, id_aparato: int, 
                      dia_semana: int, hora_inicio: str) -> int:
        """
        Crea una nueva reserva
        
        Args:
            dia_semana: 1=Lunes, 2=Martes, 3=Miércoles, 4=Jueves, 5=Viernes
            hora_inicio: Formato HH:MM (ej: "09:00", "14:30")
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO reservas (id_cliente, id_aparato, dia_semana, hora_inicio)
                VALUES (?, ?, ?, ?)
            """, (id_cliente, id_aparato, dia_semana, hora_inicio))
            conn.commit()
            return cursor.lastrowid
    
    def obtener_reserva(self, id_reserva: int) -> Optional[Dict]:
        """Obtiene una reserva por su ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.*, c.nombre as nombre_cliente, c.dni,
                       a.nombre as nombre_aparato, a.tipo as tipo_aparato
                FROM reservas r
                JOIN clientes c ON r.id_cliente = c.id_cliente
                JOIN aparatos a ON r.id_aparato = a.id_aparato
                WHERE r.id_reserva = ?
            """, (id_reserva,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def obtener_reservas_por_dia(self, dia_semana: int) -> List[Dict]:
        """Obtiene todas las reservas activas de un día específico"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.*, c.nombre as nombre_cliente, c.dni,
                       a.nombre as nombre_aparato, a.tipo as tipo_aparato
                FROM reservas r
                JOIN clientes c ON r.id_cliente = c.id_cliente
                JOIN aparatos a ON r.id_aparato = a.id_aparato
                WHERE r.dia_semana = ? AND r.estado = 'Activa'
                ORDER BY r.hora_inicio, a.nombre
            """, (dia_semana,))
            return [dict(row) for row in cursor.fetchall()]
    
    def obtener_reservas_cliente(self, id_cliente: int) -> List[Dict]:
        """Obtiene todas las reservas de un cliente"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.*, a.nombre as nombre_aparato, a.tipo as tipo_aparato
                FROM reservas r
                JOIN aparatos a ON r.id_aparato = a.id_aparato
                WHERE r.id_cliente = ? AND r.estado = 'Activa'
                ORDER BY r.dia_semana, r.hora_inicio
            """, (id_cliente,))
            return [dict(row) for row in cursor.fetchall()]
    
    def verificar_disponibilidad(self, id_aparato: int, dia_semana: int, 
                                 hora_inicio: str) -> bool:
        """Verifica si un aparato está disponible en un horario específico"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) as count FROM reservas
                WHERE id_aparato = ? AND dia_semana = ? AND hora_inicio = ?
                AND estado = 'Activa'
            """, (id_aparato, dia_semana, hora_inicio))
            result = cursor.fetchone()
            return result['count'] == 0
    
    def cancelar_reserva(self, id_reserva: int) -> bool:
        """Cancela una reserva (cambia su estado)"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE reservas SET estado = 'Cancelada'
                WHERE id_reserva = ? AND estado = 'Activa'
            """, (id_reserva,))
            conn.commit()
            return cursor.rowcount > 0
    
    def eliminar_reserva(self, id_reserva: int) -> bool:
        """Elimina completamente una reserva"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM reservas WHERE id_reserva = ?", (id_reserva,))
            conn.commit()
            return cursor.rowcount > 0
    
    # ==================== RECIBOS Y PAGOS ====================
    
    def generar_recibos_mes(self, mes: int, anio: int, monto: float) -> int:
        """
        Genera recibos para todos los clientes activos de un mes
        
        Returns:
            Cantidad de recibos generados
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Obtener clientes activos que no tengan recibo para este mes
            cursor.execute("""
                SELECT id_cliente FROM clientes
                WHERE activo = 1 AND id_cliente NOT IN (
                    SELECT id_cliente FROM recibos WHERE mes = ? AND anio = ?
                )
            """, (mes, anio))
            
            clientes = cursor.fetchall()
            count = 0
            
            for cliente in clientes:
                cursor.execute("""
                    INSERT INTO recibos (id_cliente, mes, anio, monto)
                    VALUES (?, ?, ?, ?)
                """, (cliente['id_cliente'], mes, anio, monto))
                count += 1
            
            conn.commit()
            return count
    
    def obtener_recibo(self, id_recibo: int) -> Optional[Dict]:
        """Obtiene un recibo por su ID"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT r.*, c.nombre as nombre_cliente, c.dni, c.telefono, c.email
                FROM recibos r
                JOIN clientes c ON r.id_cliente = c.id_cliente
                WHERE r.id_recibo = ?
            """, (id_recibo,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def obtener_recibos_cliente(self, id_cliente: int) -> List[Dict]:
        """Obtiene todos los recibos de un cliente"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM recibos
                WHERE id_cliente = ?
                ORDER BY anio DESC, mes DESC
            """, (id_cliente,))
            return [dict(row) for row in cursor.fetchall()]
    
    def obtener_recibos_pendientes(self, id_cliente: int = None) -> List[Dict]:
        """Obtiene recibos pendientes de pago"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if id_cliente:
                cursor.execute("""
                    SELECT r.*, c.nombre as nombre_cliente, c.dni
                    FROM recibos r
                    JOIN clientes c ON r.id_cliente = c.id_cliente
                    WHERE r.pagado = 0 AND r.id_cliente = ?
                    ORDER BY r.anio DESC, r.mes DESC
                """, (id_cliente,))
            else:
                cursor.execute("""
                    SELECT r.*, c.nombre as nombre_cliente, c.dni
                    FROM recibos r
                    JOIN clientes c ON r.id_cliente = c.id_cliente
                    WHERE r.pagado = 0
                    ORDER BY r.anio DESC, r.mes DESC
                """)
            return [dict(row) for row in cursor.fetchall()]
    
    def registrar_pago(self, id_recibo: int) -> bool:
        """Registra el pago de un recibo"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE recibos 
                SET pagado = 1, fecha_pago = date('now')
                WHERE id_recibo = ? AND pagado = 0
            """, (id_recibo,))
            conn.commit()
            return cursor.rowcount > 0
    
    def obtener_clientes_morosos(self) -> List[Dict]:
        """Obtiene listado de clientes con pagos pendientes"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM vista_morosos")
            return [dict(row) for row in cursor.fetchall()]
    
    # ==================== ESTADÍSTICAS ====================
    
    def obtener_estadisticas(self) -> Dict[str, Any]:
        """Obtiene estadísticas generales del gimnasio"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total de clientes activos
            cursor.execute("SELECT COUNT(*) as total FROM clientes WHERE activo = 1")
            total_clientes = cursor.fetchone()['total']
            
            # Total de aparatos activos
            cursor.execute("SELECT COUNT(*) as total FROM aparatos WHERE activo = 1")
            total_aparatos = cursor.fetchone()['total']
            
            # Total de reservas activas
            cursor.execute("SELECT COUNT(*) as total FROM reservas WHERE estado = 'Activa'")
            total_reservas = cursor.fetchone()['total']
            
            # Total de recibos pendientes
            cursor.execute("SELECT COUNT(*) as total FROM recibos WHERE pagado = 0")
            total_pendientes = cursor.fetchone()['total']
            
            # Ingresos del mes actual
            cursor.execute("""
                SELECT COALESCE(SUM(monto), 0) as ingresos
                FROM recibos
                WHERE pagado = 1 
                AND mes = strftime('%m', 'now')
                AND anio = strftime('%Y', 'now')
            """)
            ingresos_mes = cursor.fetchone()['ingresos']
            
            return {
                'total_clientes': total_clientes,
                'total_aparatos': total_aparatos,
                'total_reservas': total_reservas,
                'total_pendientes': total_pendientes,
                'ingresos_mes': ingresos_mes
            }
    
    def cerrar(self):
        """Cierra la conexión a la base de datos"""
        if self.connection:
            self.connection.close()
