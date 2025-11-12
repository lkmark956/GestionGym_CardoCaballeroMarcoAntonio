"""
Script para poblar la base de datos con datos de prueba
Ejecutar: python datos_prueba.py
"""

from database.db_manager import DatabaseManager
from datetime import datetime


def poblar_datos():
    """Crea datos de prueba en la base de datos"""
    
    print("🔧 Inicializando base de datos...")
    db = DatabaseManager()
    
    print("\n👥 Creando clientes de prueba...")
    
    # Clientes
    clientes = [
        ("12345678", "Juan Pérez", "1234567890", "juan@email.com"),
        ("87654321", "María García", "0987654321", "maria@email.com"),
        ("11223344", "Carlos López", "1122334455", "carlos@email.com"),
        ("44332211", "Ana Martínez", "5544332211", "ana@email.com"),
        ("55667788", "Pedro Rodríguez", "6677889900", "pedro@email.com"),
    ]
    
    clientes_ids = []
    for dni, nombre, tel, email in clientes:
        try:
            id_cliente = db.crear_cliente(dni, nombre, tel, email)
            clientes_ids.append(id_cliente)
            print(f"   ✓ Cliente creado: {nombre}")
        except Exception as e:
            print(f"   ⚠ Cliente ya existe: {nombre}")
    
    print("\n🏋️ Creando aparatos de prueba...")
    
    # Aparatos
    aparatos = [
        ("Cinta de Correr #1", "Cardio", "Cinta motorizada profesional"),
        ("Cinta de Correr #2", "Cardio", "Cinta motorizada profesional"),
        ("Bicicleta Estática #1", "Cardio", "Bicicleta spinning"),
        ("Bicicleta Estática #2", "Cardio", "Bicicleta spinning"),
        ("Press de Pecho", "Fuerza", "Máquina de press horizontal"),
        ("Press de Piernas", "Fuerza", "Prensa de piernas 45°"),
        ("Remo Sentado", "Fuerza", "Máquina de remo bajo"),
        ("Mancuernas", "Fuerza", "Juego de mancuernas 5-30kg"),
        ("Banda Elástica #1", "Funcional", "Entrenamiento funcional"),
        ("Colchoneta #1", "Estiramiento", "Para yoga y estiramientos"),
    ]
    
    aparatos_ids = []
    for nombre, tipo, desc in aparatos:
        try:
            id_aparato = db.crear_aparato(nombre, tipo, desc)
            aparatos_ids.append(id_aparato)
            print(f"   ✓ Aparato creado: {nombre}")
        except Exception as e:
            print(f"   ⚠ Aparato ya existe: {nombre}")
    
    print("\n📅 Creando reservas de prueba...")
    
    # Reservas (solo si hay clientes y aparatos)
    if clientes_ids and aparatos_ids:
        reservas = [
            (clientes_ids[0], aparatos_ids[0], 1, "09:00"),  # Juan - Cinta #1 - Lunes 9:00
            (clientes_ids[1], aparatos_ids[1], 1, "09:00"),  # María - Cinta #2 - Lunes 9:00
            (clientes_ids[0], aparatos_ids[2], 1, "10:00"),  # Juan - Bici #1 - Lunes 10:00
            (clientes_ids[2], aparatos_ids[0], 2, "14:30"),  # Carlos - Cinta #1 - Martes 14:30
            (clientes_ids[3], aparatos_ids[4], 3, "16:00"),  # Ana - Press Pecho - Miércoles 16:00
            (clientes_ids[4], aparatos_ids[5], 4, "18:30"),  # Pedro - Press Piernas - Jueves 18:30
        ]
        
        for id_cliente, id_aparato, dia, hora in reservas:
            try:
                db.crear_reserva(id_cliente, id_aparato, dia, hora)
                print(f"   ✓ Reserva creada")
            except Exception as e:
                print(f"   ⚠ Error al crear reserva: {e}")
    
    print("\n💰 Generando recibos del mes actual...")
    
    # Generar recibos del mes actual
    mes_actual = datetime.now().month
    anio_actual = datetime.now().year
    
    try:
        cantidad = db.generar_recibos_mes(mes_actual, anio_actual, 5000.0)
        print(f"   ✓ Se generaron {cantidad} recibos de $5000")
    except Exception as e:
        print(f"   ⚠ Error al generar recibos: {e}")
    
    # Registrar algunos pagos
    print("\n💳 Registrando algunos pagos...")
    recibos_pendientes = db.obtener_recibos_pendientes()
    
    if len(recibos_pendientes) >= 2:
        # Pagar los primeros 2 recibos
        for i in range(min(2, len(recibos_pendientes))):
            try:
                db.registrar_pago(recibos_pendientes[i]['id_recibo'])
                print(f"   ✓ Pago registrado para {recibos_pendientes[i]['nombre_cliente']}")
            except Exception as e:
                print(f"   ⚠ Error al registrar pago: {e}")
    
    print("\n📊 Estadísticas finales:")
    stats = db.obtener_estadisticas()
    print(f"   • Clientes activos: {stats['total_clientes']}")
    print(f"   • Aparatos disponibles: {stats['total_aparatos']}")
    print(f"   • Reservas activas: {stats['total_reservas']}")
    print(f"   • Recibos pendientes: {stats['total_pendientes']}")
    print(f"   • Ingresos del mes: ${stats['ingresos_mes']:.2f}")
    
    print("\n✅ ¡Base de datos poblada con éxito!")
    print("\n💡 Ahora puede ejecutar: python main.py")
    
    db.cerrar()


if __name__ == "__main__":
    poblar_datos()
