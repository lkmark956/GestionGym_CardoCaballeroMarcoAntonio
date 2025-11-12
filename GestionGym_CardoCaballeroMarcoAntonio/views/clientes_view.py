"""
Vista de gestión de clientes
"""

import customtkinter as ctk
from tkinter import messagebox
from utils.validators import Validators


class ClientesView(ctk.CTkFrame):
    """Vista para gestionar clientes"""
    
    def __init__(self, parent, db):
        super().__init__(parent, corner_radius=0)
        
        self.db = db
        self.clientes = []
        self.cliente_seleccionado = None
        
        self._create_widgets()
        self._load_clientes()
    
    def _create_widgets(self):
        """Crea los widgets de la vista"""
        
        # Configurar grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            self,
            text="Gestión de Clientes",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="w")
        
        # ===== PANEL IZQUIERDO: Formulario =====
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=0, padx=(20, 10), pady=(0, 20), sticky="nsew")
        
        # Formulario
        ctk.CTkLabel(
            form_frame,
            text="Datos del Cliente",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(padx=20, pady=(20, 10), anchor="w")
        
        # DNI
        ctk.CTkLabel(form_frame, text="DNI *", anchor="w").pack(padx=20, pady=(10, 0), fill="x")
        self.entry_dni = ctk.CTkEntry(form_frame, placeholder_text="Ej: 12345678")
        self.entry_dni.pack(padx=20, pady=(5, 0), fill="x")
        
        # Nombre
        ctk.CTkLabel(form_frame, text="Nombre Completo *", anchor="w").pack(padx=20, pady=(10, 0), fill="x")
        self.entry_nombre = ctk.CTkEntry(form_frame, placeholder_text="Ej: Juan Pérez")
        self.entry_nombre.pack(padx=20, pady=(5, 0), fill="x")
        
        # Teléfono
        ctk.CTkLabel(form_frame, text="Teléfono", anchor="w").pack(padx=20, pady=(10, 0), fill="x")
        self.entry_telefono = ctk.CTkEntry(form_frame, placeholder_text="Ej: 1234567890")
        self.entry_telefono.pack(padx=20, pady=(5, 0), fill="x")
        
        # Email
        ctk.CTkLabel(form_frame, text="Email", anchor="w").pack(padx=20, pady=(10, 0), fill="x")
        self.entry_email = ctk.CTkEntry(form_frame, placeholder_text="Ej: cliente@email.com")
        self.entry_email.pack(padx=20, pady=(5, 0), fill="x")
        
        # Botones
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(padx=20, pady=20, fill="x")
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.btn_guardar = ctk.CTkButton(
            buttons_frame,
            text="💾 Guardar",
            command=self._guardar_cliente,
            height=40
        )
        self.btn_guardar.grid(row=0, column=0, padx=(0, 5), sticky="ew")
        
        self.btn_limpiar = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Limpiar",
            command=self._limpiar_formulario,
            height=40,
            fg_color="gray",
            hover_color="darkgray"
        )
        self.btn_limpiar.grid(row=0, column=1, padx=(5, 0), sticky="ew")
        
        self.btn_eliminar = ctk.CTkButton(
            buttons_frame,
            text="❌ Desactivar",
            command=self._eliminar_cliente,
            height=40,
            fg_color="red",
            hover_color="darkred"
        )
        self.btn_eliminar.grid(row=1, column=0, columnspan=2, pady=(10, 0), sticky="ew")
        self.btn_eliminar.configure(state="disabled")
        
        # ===== PANEL DERECHO: Lista =====
        list_frame = ctk.CTkFrame(self)
        list_frame.grid(row=1, column=1, padx=(10, 20), pady=(0, 20), sticky="nsew")
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(2, weight=1)
        
        # Título y búsqueda
        ctk.CTkLabel(
            list_frame,
            text="Clientes Registrados",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")
        
        # Búsqueda
        search_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        search_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        search_frame.grid_columnconfigure(0, weight=1)
        
        self.entry_buscar = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Buscar por nombre o DNI..."
        )
        self.entry_buscar.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        self.entry_buscar.bind("<KeyRelease>", lambda e: self._buscar_clientes())
        
        btn_refresh = ctk.CTkButton(
            search_frame,
            text="🔄",
            width=40,
            command=self._load_clientes
        )
        btn_refresh.grid(row=0, column=1)
        
        # Lista de clientes
        self.list_clientes = ctk.CTkScrollableFrame(list_frame)
        self.list_clientes.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.list_clientes.grid_columnconfigure(0, weight=1)
    
    def _load_clientes(self):
        """Carga la lista de clientes"""
        self.clientes = self.db.obtener_todos_clientes(solo_activos=True)
        self._mostrar_clientes(self.clientes)
    
    def _buscar_clientes(self):
        """Busca clientes por término"""
        termino = self.entry_buscar.get().strip()
        if termino:
            self.clientes = self.db.buscar_clientes(termino)
        else:
            self.clientes = self.db.obtener_todos_clientes(solo_activos=True)
        self._mostrar_clientes(self.clientes)
    
    def _mostrar_clientes(self, clientes):
        """Muestra la lista de clientes"""
        # Limpiar lista
        for widget in self.list_clientes.winfo_children():
            widget.destroy()
        
        if not clientes:
            label = ctk.CTkLabel(
                self.list_clientes,
                text="No hay clientes registrados",
                text_color="gray"
            )
            label.pack(pady=20)
            return
        
        # Mostrar clientes
        for cliente in clientes:
            self._create_cliente_card(cliente)
    
    def _create_cliente_card(self, cliente):
        """Crea una tarjeta de cliente"""
        card = ctk.CTkFrame(self.list_clientes)
        card.pack(fill="x", pady=5)
        card.grid_columnconfigure(0, weight=1)
        
        # Información
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # Nombre
        nombre_label = ctk.CTkLabel(
            info_frame,
            text=cliente['nombre'],
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        nombre_label.pack(fill="x")
        
        # Detalles
        detalles = f"DNI: {cliente['dni']}"
        if cliente['telefono']:
            detalles += f" | Tel: {cliente['telefono']}"
        if cliente['email']:
            detalles += f" | Email: {cliente['email']}"
        
        detalles_label = ctk.CTkLabel(
            info_frame,
            text=detalles,
            font=ctk.CTkFont(size=11),
            text_color="gray",
            anchor="w"
        )
        detalles_label.pack(fill="x")
        
        # Botón seleccionar
        btn_seleccionar = ctk.CTkButton(
            card,
            text="✏️",
            width=40,
            command=lambda c=cliente: self._seleccionar_cliente(c)
        )
        btn_seleccionar.grid(row=0, column=1, padx=10)
    
    def _seleccionar_cliente(self, cliente):
        """Selecciona un cliente para editar"""
        self.cliente_seleccionado = cliente
        
        # Llenar formulario
        self.entry_dni.delete(0, "end")
        self.entry_dni.insert(0, cliente['dni'])
        self.entry_dni.configure(state="disabled")  # DNI no se puede editar
        
        self.entry_nombre.delete(0, "end")
        self.entry_nombre.insert(0, cliente['nombre'])
        
        self.entry_telefono.delete(0, "end")
        if cliente['telefono']:
            self.entry_telefono.insert(0, cliente['telefono'])
        
        self.entry_email.delete(0, "end")
        if cliente['email']:
            self.entry_email.insert(0, cliente['email'])
        
        # Habilitar botón eliminar
        self.btn_eliminar.configure(state="normal")
        self.btn_guardar.configure(text="💾 Actualizar")
    
    def _limpiar_formulario(self):
        """Limpia el formulario"""
        self.entry_dni.configure(state="normal")
        self.entry_dni.delete(0, "end")
        self.entry_nombre.delete(0, "end")
        self.entry_telefono.delete(0, "end")
        self.entry_email.delete(0, "end")
        
        self.cliente_seleccionado = None
        self.btn_eliminar.configure(state="disabled")
        self.btn_guardar.configure(text="💾 Guardar")
    
    def _guardar_cliente(self):
        """Guarda o actualiza un cliente"""
        # Obtener datos
        dni = self.entry_dni.get().strip()
        nombre = self.entry_nombre.get().strip()
        telefono = self.entry_telefono.get().strip()
        email = self.entry_email.get().strip()
        
        # Validar
        valido, msg = Validators.validar_dni(dni)
        if not valido:
            messagebox.showerror("Error", msg)
            return
        
        valido, msg = Validators.validar_nombre(nombre)
        if not valido:
            messagebox.showerror("Error", msg)
            return
        
        valido, msg = Validators.validar_telefono(telefono)
        if not valido:
            messagebox.showerror("Error", msg)
            return
        
        valido, msg = Validators.validar_email(email)
        if not valido:
            messagebox.showerror("Error", msg)
            return
        
        try:
            if self.cliente_seleccionado:
                # Actualizar
                self.db.actualizar_cliente(
                    self.cliente_seleccionado['id_cliente'],
                    nombre=nombre,
                    telefono=telefono,
                    email=email
                )
                messagebox.showinfo("Éxito", "Cliente actualizado correctamente")
            else:
                # Crear nuevo
                self.db.crear_cliente(dni, nombre, telefono, email)
                messagebox.showinfo("Éxito", "Cliente creado correctamente")
            
            self._limpiar_formulario()
            self._load_clientes()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar cliente:\n{str(e)}")
    
    def _eliminar_cliente(self):
        """Desactiva un cliente"""
        if not self.cliente_seleccionado:
            return
        
        if messagebox.askyesno("Confirmar", 
                               f"¿Desactivar al cliente {self.cliente_seleccionado['nombre']}?"):
            try:
                self.db.desactivar_cliente(self.cliente_seleccionado['id_cliente'])
                messagebox.showinfo("Éxito", "Cliente desactivado correctamente")
                self._limpiar_formulario()
                self._load_clientes()
            except Exception as e:
                messagebox.showerror("Error", f"Error al desactivar cliente:\n{str(e)}")
