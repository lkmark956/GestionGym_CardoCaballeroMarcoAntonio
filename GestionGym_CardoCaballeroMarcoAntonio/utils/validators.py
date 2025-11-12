"""
Utilidades de validación para el sistema de gimnasio
"""

import re
from datetime import datetime
from typing import Tuple


class Validators:
    """Clase con métodos estáticos para validaciones"""
    
    @staticmethod
    def validar_dni(dni: str) -> Tuple[bool, str]:
        """
        Valida un DNI
        
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        if not dni or not dni.strip():
            return False, "El DNI no puede estar vacío"
        
        dni = dni.strip()
        
        if len(dni) < 7 or len(dni) > 10:
            return False, "El DNI debe tener entre 7 y 10 caracteres"
        
        if not dni.replace("-", "").replace(".", "").isalnum():
            return False, "El DNI contiene caracteres inválidos"
        
        return True, ""
    
    @staticmethod
    def validar_email(email: str) -> Tuple[bool, str]:
        """
        Valida un email
        
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        if not email or not email.strip():
            return True, ""  # El email es opcional
        
        email = email.strip()
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(patron, email):
            return False, "El formato del email no es válido"
        
        return True, ""
    
    @staticmethod
    def validar_telefono(telefono: str) -> Tuple[bool, str]:
        """
        Valida un teléfono
        
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        if not telefono or not telefono.strip():
            return True, ""  # El teléfono es opcional
        
        telefono = telefono.strip()
        
        # Remover espacios, guiones y paréntesis
        telefono_limpio = telefono.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        
        if not telefono_limpio.isdigit():
            return False, "El teléfono solo puede contener números"
        
        if len(telefono_limpio) < 7 or len(telefono_limpio) > 15:
            return False, "El teléfono debe tener entre 7 y 15 dígitos"
        
        return True, ""
    
    @staticmethod
    def validar_nombre(nombre: str) -> Tuple[bool, str]:
        """
        Valida un nombre
        
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        if not nombre or not nombre.strip():
            return False, "El nombre no puede estar vacío"
        
        nombre = nombre.strip()
        
        if len(nombre) < 3:
            return False, "El nombre debe tener al menos 3 caracteres"
        
        if len(nombre) > 100:
            return False, "El nombre no puede superar los 100 caracteres"
        
        return True, ""
    
    @staticmethod
    def validar_dia_semana(dia: int) -> Tuple[bool, str]:
        """
        Valida que el día sea de lunes (1) a viernes (5)
        
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        if dia < 1 or dia > 5:
            return False, "El gimnasio solo opera de Lunes a Viernes"
        
        return True, ""
    
    @staticmethod
    def validar_hora(hora: str) -> Tuple[bool, str]:
        """
        Valida formato de hora HH:MM y que sean intervalos de 30 minutos
        
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        if not hora or not hora.strip():
            return False, "La hora no puede estar vacía"
        
        hora = hora.strip()
        
        # Validar formato HH:MM
        patron = r'^([0-1]?[0-9]|2[0-3]):([0-5][0-9])$'
        if not re.match(patron, hora):
            return False, "El formato de hora debe ser HH:MM (ej: 09:00)"
        
        # Validar que los minutos sean 00 o 30
        minutos = int(hora.split(':')[1])
        if minutos not in [0, 30]:
            return False, "Las sesiones solo pueden comenzar a las :00 o :30"
        
        return True, ""
    
    @staticmethod
    def validar_monto(monto: float) -> Tuple[bool, str]:
        """
        Valida que el monto sea positivo
        
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        try:
            monto_float = float(monto)
            if monto_float <= 0:
                return False, "El monto debe ser mayor a 0"
            return True, ""
        except (ValueError, TypeError):
            return False, "El monto debe ser un número válido"
    
    @staticmethod
    def validar_mes_anio(mes: int, anio: int) -> Tuple[bool, str]:
        """
        Valida mes y año
        
        Returns:
            Tupla (es_valido, mensaje_error)
        """
        if mes < 1 or mes > 12:
            return False, "El mes debe estar entre 1 y 12"
        
        anio_actual = datetime.now().year
        if anio < 2020 or anio > anio_actual + 1:
            return False, f"El año debe estar entre 2020 y {anio_actual + 1}"
        
        return True, ""
    
    @staticmethod
    def obtener_nombre_dia(dia: int) -> str:
        """Convierte número de día a nombre"""
        dias = {
            1: "Lunes",
            2: "Martes",
            3: "Miércoles",
            4: "Jueves",
            5: "Viernes"
        }
        return dias.get(dia, "Día inválido")
    
    @staticmethod
    def obtener_nombre_mes(mes: int) -> str:
        """Convierte número de mes a nombre"""
        meses = {
            1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril",
            5: "Mayo", 6: "Junio", 7: "Julio", 8: "Agosto",
            9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
        }
        return meses.get(mes, "Mes inválido")
    
    @staticmethod
    def generar_horarios_dia() -> list:
        """
        Genera lista de todos los horarios posibles del día (48 sesiones)
        
        Returns:
            Lista de strings con formato HH:MM
        """
        horarios = []
        for hora in range(24):
            for minuto in [0, 30]:
                horarios.append(f"{hora:02d}:{minuto:02d}")
        return horarios
