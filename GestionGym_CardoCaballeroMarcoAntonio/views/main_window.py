"""
Ventana principal del sistema de gestión del gimnasio
Interfaz moderna y responsive con CustomTkinter
"""

import customtkinter as ctk
from tkinter import messagebox
from database.db_manager import DatabaseManager
from views.clientes_view import ClientesView
from views.aparatos_view import AparatosView
from views.reservas_view import ReservasView
from views.pagos_view import PagosView


class MainWindow(ctk.CTk):
    """Ventana principal de la aplicación"""
    
    def __init__(self):
        super().__init__()
        
        # Configuración de la ventana
        self.title("GymForTheMoment - Sistema de Gestión")
        self.geometry("1200x700")
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Inicializar base de datos
        self.db = DatabaseManager()
        
        # Variables
        self.current_view = None
        
        # Crear interfaz
        self._create_layout()
        self._load_statistics()
        
        # Mostrar vista de inicio
        self.show_home()
    
    def _create_layout(self):
        """Crea el layout principal de la aplicación"""
        
        # Grid principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # ===== SIDEBAR =====
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(10, weight=1)
        
        # Logo/Título
        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="🏋️ GymForTheMoment",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 30))
        
        # Botones del menú
        self.btn_home = ctk.CTkButton(
            self.sidebar,
            text="🏠 Inicio",
            command=self.show_home,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.btn_home.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_clientes = ctk.CTkButton(
            self.sidebar,
            text="👥 Clientes",
            command=self.show_clientes,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.btn_clientes.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_aparatos = ctk.CTkButton(
            self.sidebar,
            text="🏋️ Aparatos",
            command=self.show_aparatos,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.btn_aparatos.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_reservas = ctk.CTkButton(
            self.sidebar,
            text="📅 Reservas",
            command=self.show_reservas,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.btn_reservas.grid(row=4, column=0, padx=20, pady=10, sticky="ew")
        
        self.btn_pagos = ctk.CTkButton(
            self.sidebar,
            text="💰 Pagos",
            command=self.show_pagos,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.btn_pagos.grid(row=5, column=0, padx=20, pady=10, sticky="ew")
        
        # Separador
        separator = ctk.CTkFrame(self.sidebar, height=2)
        separator.grid(row=6, column=0, padx=20, pady=20, sticky="ew")
        
        # Información
        self.info_label = ctk.CTkLabel(
            self.sidebar,
            text="Sistema de Gestión\nv1.0",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.info_label.grid(row=11, column=0, padx=20, pady=20)
        
        # ===== CONTENIDO PRINCIPAL =====
        self.main_container = ctk.CTkFrame(self, corner_radius=0)
        self.main_container.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.main_container.grid_columnconfigure(0, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
    
    def _clear_main_container(self):
        """Limpia el contenedor principal"""
        if self.current_view:
            self.current_view.destroy()
            self.current_view = None
    
    def show_home(self):
        """Muestra la vista de inicio con estadísticas"""
        self._clear_main_container()
        
        # Frame principal
        home_frame = ctk.CTkFrame(self.main_container)
        home_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        home_frame.grid_columnconfigure((0, 1), weight=1)
        home_frame.grid_rowconfigure(2, weight=1)
        
        self.current_view = home_frame
        
        # Título
        title = ctk.CTkLabel(
            home_frame,
            text="Panel de Control",
            font=ctk.CTkFont(size=32, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 30), sticky="w")
        
        # Cargar estadísticas
        stats = self.db.obtener_estadisticas()
        
        # Tarjetas de estadísticas
        # Clientes
        self.card_clientes = self._create_stat_card(
            home_frame,
            "👥 Clientes Activos",
            str(stats['total_clientes']),
            "Total de clientes registrados"
        )
        self.card_clientes.grid(row=1, column=0, padx=20, pady=10, sticky="new")
        
        # Aparatos
        self.card_aparatos = self._create_stat_card(
            home_frame,
            "🏋️ Aparatos Disponibles",
            str(stats['total_aparatos']),
            "Equipos de entrenamiento"
        )
        self.card_aparatos.grid(row=1, column=1, padx=20, pady=10, sticky="new")
        
        # Reservas
        self.card_reservas = self._create_stat_card(
            home_frame,
            "📅 Reservas Activas",
            str(stats['total_reservas']),
            "Sesiones programadas"
        )
        self.card_reservas.grid(row=2, column=0, padx=20, pady=10, sticky="new")
        
        # Pagos pendientes
        self.card_pendientes = self._create_stat_card(
            home_frame,
            "⚠️ Pagos Pendientes",
            str(stats['total_pendientes']),
            "Recibos sin pagar",
            color="orange"
        )
        self.card_pendientes.grid(row=2, column=1, padx=20, pady=10, sticky="new")
        
        # Ingresos del mes
        self.card_ingresos = self._create_stat_card(
            home_frame,
            "💰 Ingresos del Mes",
            f"${stats['ingresos_mes']:.2f}",
            "Total recaudado este mes",
            color="green"
        )
        self.card_ingresos.grid(row=3, column=0, columnspan=2, padx=20, pady=10, sticky="new")
        
        # Información adicional
        info_frame = ctk.CTkFrame(home_frame)
        info_frame.grid(row=4, column=0, columnspan=2, padx=20, pady=20, sticky="ew")
        
        info_text = ctk.CTkLabel(
            info_frame,
            text="📋 Horario: Lunes a Viernes, 24 horas | 🕐 Sesiones: 30 minutos",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        info_text.pack(padx=20, pady=15)
    
    def _create_stat_card(self, parent, title, value, description, color=None):
        """Crea una tarjeta de estadística"""
        
        if color == "orange":
            fg_color = ("#FF8C00", "#FF6B00")
        elif color == "green":
            fg_color = ("#2E7D32", "#1B5E20")
        else:
            fg_color = ("gray75", "gray25")
        
        card = ctk.CTkFrame(parent, fg_color=fg_color)
        
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_label.pack(padx=20, pady=(20, 5), anchor="w")
        
        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=36, weight="bold")
        )
        value_label.pack(padx=20, pady=5, anchor="w")
        
        desc_label = ctk.CTkLabel(
            card,
            text=description,
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        desc_label.pack(padx=20, pady=(5, 20), anchor="w")
        
        return card
    
    def _load_statistics(self):
        """Recarga las estadísticas"""
        pass  # Se llama desde show_home
    
    def show_clientes(self):
        """Muestra la vista de clientes"""
        self._clear_main_container()
        self.current_view = ClientesView(self.main_container, self.db)
        self.current_view.grid(row=0, column=0, sticky="nsew")
    
    def show_aparatos(self):
        """Muestra la vista de aparatos"""
        self._clear_main_container()
        self.current_view = AparatosView(self.main_container, self.db)
        self.current_view.grid(row=0, column=0, sticky="nsew")
    
    def show_reservas(self):
        """Muestra la vista de reservas"""
        self._clear_main_container()
        self.current_view = ReservasView(self.main_container, self.db)
        self.current_view.grid(row=0, column=0, sticky="nsew")
    
    def show_pagos(self):
        """Muestra la vista de pagos"""
        self._clear_main_container()
        self.current_view = PagosView(self.main_container, self.db)
        self.current_view.grid(row=0, column=0, sticky="nsew")
    
    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        if messagebox.askokcancel("Salir", "¿Desea cerrar la aplicación?"):
            self.db.cerrar()
            self.destroy()
