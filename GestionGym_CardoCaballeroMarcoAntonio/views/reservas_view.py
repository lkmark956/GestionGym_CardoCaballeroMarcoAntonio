"""
Vista de gestión de reservas
"""

import customtkinter as ctk
from tkinter import messagebox
from utils.validators import Validators


class ReservasView(ctk.CTkFrame):
    """Vista para gestionar reservas"""
    
    def __init__(self, parent, db):
        super().__init__(parent, corner_radius=0)
        
        self.db = db
        self.reservas = []
        
        self._create_widgets()
        self._load_data()
    
    def _create_widgets(self):
        """Crea los widgets de la vista"""
        
        # Configurar grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            self,
            text="Gestión de Reservas",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="w")
        
        # ===== PANEL IZQUIERDO: Formulario =====
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=0, padx=(20, 10), pady=(0, 20), sticky="nsew")
        
        # Formulario
        ctk.CTkLabel(
            form_frame,
            text="Nueva Reserva",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(padx=20, pady=(20, 10), anchor="w")
        
        # Cliente
        ctk.CTkLabel(form_frame, text="Cliente *", anchor="w").pack(padx=20, pady=(10, 0), fill="x")
        self.combo_cliente = ctk.CTkComboBox(form_frame, state="readonly")
        self.combo_cliente.pack(padx=20, pady=(5, 0), fill="x")
        
        # Día de la semana
        ctk.CTkLabel(form_frame, text="Día de la Semana *", anchor="w").pack(padx=20, pady=(10, 0), fill="x")
        self.combo_dia = ctk.CTkComboBox(
            form_frame,
            values=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"],
            state="readonly"
        )
        self.combo_dia.pack(padx=20, pady=(5, 0), fill="x")
        self.combo_dia.set("Lunes")
        self.combo_dia.configure(command=self._on_dia_changed)
        
        # Hora
        ctk.CTkLabel(form_frame, text="Hora de Inicio *", anchor="w").pack(padx=20, pady=(10, 0), fill="x")
        
        # Frame para hora
        hora_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        hora_frame.pack(padx=20, pady=(5, 0), fill="x")
        hora_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.combo_hora = ctk.CTkComboBox(
            hora_frame,
            values=[f"{h:02d}" for h in range(24)],
            state="readonly",
            width=100
        )
        self.combo_hora.grid(row=0, column=0, padx=(0, 5))
        self.combo_hora.set("09")
        
        self.combo_minuto = ctk.CTkComboBox(
            hora_frame,
            values=["00", "30"],
            state="readonly",
            width=100
        )
        self.combo_minuto.grid(row=0, column=1, padx=(5, 0))
        self.combo_minuto.set("00")
        
        # Aparato
        ctk.CTkLabel(form_frame, text="Aparato *", anchor="w").pack(padx=20, pady=(10, 0), fill="x")
        self.combo_aparato = ctk.CTkComboBox(form_frame, state="readonly")
        self.combo_aparato.pack(padx=20, pady=(5, 0), fill="x")
        
        # Info
        self.label_disponibilidad = ctk.CTkLabel(
            form_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.label_disponibilidad.pack(padx=20, pady=10)
        
        # Botones
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(padx=20, pady=20, fill="x")
        buttons_frame.grid_columnconfigure(0, weight=1)
        
        self.btn_crear = ctk.CTkButton(
            buttons_frame,
            text="📅 Crear Reserva",
            command=self._crear_reserva,
            height=40
        )
        self.btn_crear.grid(row=0, column=0, sticky="ew")
        
        btn_verificar = ctk.CTkButton(
            buttons_frame,
            text="🔍 Verificar Disponibilidad",
            command=self._verificar_disponibilidad,
            height=35,
            fg_color="gray",
            hover_color="darkgray"
        )
        btn_verificar.grid(row=1, column=0, pady=(10, 0), sticky="ew")
        
        # ===== PANEL DERECHO: Consulta y Lista =====
        right_frame = ctk.CTkFrame(self)
        right_frame.grid(row=1, column=1, padx=(10, 20), pady=(0, 20), sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(2, weight=1)
        
        # Título
        ctk.CTkLabel(
            right_frame,
            text="Consultar Reservas",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Selector de día para consulta
        filter_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        filter_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        filter_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(filter_frame, text="Ver reservas del:").grid(row=0, column=0, sticky="w")
        
        self.combo_dia_consulta = ctk.CTkComboBox(
            filter_frame,
            values=["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"],
            state="readonly",
            command=lambda x: self._load_reservas()
        )
        self.combo_dia_consulta.grid(row=0, column=1, padx=10)
        self.combo_dia_consulta.set("Lunes")
        
        btn_refresh = ctk.CTkButton(
            filter_frame,
            text="🔄",
            width=40,
            command=self._load_reservas
        )
        btn_refresh.grid(row=0, column=2)
        
        # Lista de reservas
        self.list_reservas = ctk.CTkScrollableFrame(right_frame)
        self.list_reservas.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.list_reservas.grid_columnconfigure(0, weight=1)
    
    def _load_data(self):
        """Carga datos iniciales"""
        # Cargar clientes
        clientes = self.db.obtener_todos_clientes(solo_activos=True)
        cliente_nombres = [f"{c['nombre']} ({c['dni']})" for c in clientes]
        self.combo_cliente.configure(values=cliente_nombres if cliente_nombres else ["No hay clientes"])
        if cliente_nombres:
            self.combo_cliente.set(cliente_nombres[0])
        
        # Cargar aparatos
        self._cargar_aparatos()
        
        # Cargar reservas
        self._load_reservas()
    
    def _cargar_aparatos(self):
        """Carga la lista de aparatos"""
        aparatos = self.db.obtener_todos_aparatos(solo_activos=True)
        aparato_nombres = [f"{a['nombre']} - {a['tipo']}" for a in aparatos]
        self.combo_aparato.configure(values=aparato_nombres if aparato_nombres else ["No hay aparatos"])
        if aparato_nombres:
            self.combo_aparato.set(aparato_nombres[0])
    
    def _on_dia_changed(self, choice):
        """Se ejecuta cuando cambia el día seleccionado"""
        self.label_disponibilidad.configure(text="")
    
    def _verificar_disponibilidad(self):
        """Verifica si el aparato está disponible"""
        try:
            # Obtener datos
            aparato_text = self.combo_aparato.get()
            if not aparato_text or aparato_text == "No hay aparatos":
                messagebox.showwarning("Advertencia", "Seleccione un aparato")
                return
            
            aparatos = self.db.obtener_todos_aparatos(solo_activos=True)
            aparato_nombre = aparato_text.split(" - ")[0]
            aparato = next((a for a in aparatos if a['nombre'] == aparato_nombre), None)
            
            if not aparato:
                messagebox.showerror("Error", "Aparato no encontrado")
                return
            
            dia = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"].index(self.combo_dia.get()) + 1
            hora = f"{self.combo_hora.get()}:{self.combo_minuto.get()}"
            
            disponible = self.db.verificar_disponibilidad(aparato['id_aparato'], dia, hora)
            
            if disponible:
                self.label_disponibilidad.configure(
                    text="✅ Aparato disponible para esta fecha y hora",
                    text_color="green"
                )
            else:
                self.label_disponibilidad.configure(
                    text="❌ Aparato ocupado en este horario",
                    text_color="red"
                )
        except Exception as e:
            messagebox.showerror("Error", f"Error al verificar disponibilidad:\n{str(e)}")
    
    def _crear_reserva(self):
        """Crea una nueva reserva"""
        try:
            # Obtener cliente
            cliente_text = self.combo_cliente.get()
            if not cliente_text or cliente_text == "No hay clientes":
                messagebox.showwarning("Advertencia", "Seleccione un cliente")
                return
            
            clientes = self.db.obtener_todos_clientes(solo_activos=True)
            dni = cliente_text.split("(")[1].split(")")[0]
            cliente = next((c for c in clientes if c['dni'] == dni), None)
            
            if not cliente:
                messagebox.showerror("Error", "Cliente no encontrado")
                return
            
            # Obtener aparato
            aparato_text = self.combo_aparato.get()
            if not aparato_text or aparato_text == "No hay aparatos":
                messagebox.showwarning("Advertencia", "Seleccione un aparato")
                return
            
            aparatos = self.db.obtener_todos_aparatos(solo_activos=True)
            aparato_nombre = aparato_text.split(" - ")[0]
            aparato = next((a for a in aparatos if a['nombre'] == aparato_nombre), None)
            
            if not aparato:
                messagebox.showerror("Error", "Aparato no encontrado")
                return
            
            # Obtener día y hora
            dia = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"].index(self.combo_dia.get()) + 1
            hora = f"{self.combo_hora.get()}:{self.combo_minuto.get()}"
            
            # Verificar disponibilidad
            if not self.db.verificar_disponibilidad(aparato['id_aparato'], dia, hora):
                messagebox.showerror("Error", "El aparato ya está reservado en este horario")
                return
            
            # Crear reserva
            self.db.crear_reserva(cliente['id_cliente'], aparato['id_aparato'], dia, hora)
            messagebox.showinfo("Éxito", "Reserva creada correctamente")
            
            self.label_disponibilidad.configure(text="")
            self._load_reservas()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear reserva:\n{str(e)}")
    
    def _load_reservas(self):
        """Carga las reservas del día seleccionado"""
        dia_nombre = self.combo_dia_consulta.get()
        dia = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"].index(dia_nombre) + 1
        
        self.reservas = self.db.obtener_reservas_por_dia(dia)
        self._mostrar_reservas()
    
    def _mostrar_reservas(self):
        """Muestra la lista de reservas"""
        # Limpiar lista
        for widget in self.list_reservas.winfo_children():
            widget.destroy()
        
        if not self.reservas:
            label = ctk.CTkLabel(
                self.list_reservas,
                text="No hay reservas para este día",
                text_color="gray"
            )
            label.pack(pady=20)
            return
        
        # Ordenar por hora
        reservas_ordenadas = sorted(self.reservas, key=lambda x: x['hora_inicio'])
        
        # Mostrar reservas
        for reserva in reservas_ordenadas:
            self._create_reserva_card(reserva)
    
    def _create_reserva_card(self, reserva):
        """Crea una tarjeta de reserva"""
        card = ctk.CTkFrame(self.list_reservas)
        card.pack(fill="x", pady=3)
        card.grid_columnconfigure(0, weight=1)
        
        # Información
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.grid(row=0, column=0, padx=10, pady=8, sticky="ew")
        
        # Hora y aparato
        hora_label = ctk.CTkLabel(
            info_frame,
            text=f"🕐 {reserva['hora_inicio']} - {reserva['nombre_aparato']}",
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        hora_label.pack(fill="x")
        
        # Cliente
        cliente_label = ctk.CTkLabel(
            info_frame,
            text=f"Cliente: {reserva['nombre_cliente']} ({reserva['dni']})",
            font=ctk.CTkFont(size=11),
            text_color="gray",
            anchor="w"
        )
        cliente_label.pack(fill="x")
        
        # Tipo
        tipo_label = ctk.CTkLabel(
            info_frame,
            text=f"Tipo: {reserva['tipo_aparato']}",
            font=ctk.CTkFont(size=10),
            text_color="gray",
            anchor="w"
        )
        tipo_label.pack(fill="x")
        
        # Botón cancelar
        btn_cancelar = ctk.CTkButton(
            card,
            text="❌",
            width=40,
            fg_color="red",
            hover_color="darkred",
            command=lambda r=reserva: self._cancelar_reserva(r)
        )
        btn_cancelar.grid(row=0, column=1, padx=10)
    
    def _cancelar_reserva(self, reserva):
        """Cancela una reserva"""
        if messagebox.askyesno("Confirmar", 
                               f"¿Cancelar la reserva de {reserva['nombre_cliente']} para {reserva['nombre_aparato']}?"):
            try:
                self.db.cancelar_reserva(reserva['id_reserva'])
                messagebox.showinfo("Éxito", "Reserva cancelada correctamente")
                self._load_reservas()
            except Exception as e:
                messagebox.showerror("Error", f"Error al cancelar reserva:\n{str(e)}")
