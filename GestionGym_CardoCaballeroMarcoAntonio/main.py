"""
Sistema de Gestión de Gimnasio - GymForTheMoment
Aplicación principal
"""

import sys
from views.main_window import MainWindow


def main():
    """Función principal de la aplicación"""
    try:
        # Crear y ejecutar la aplicación
        app = MainWindow()
        
        # Manejar el cierre de la ventana
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        
        # Iniciar el loop principal
        app.mainloop()
        
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
