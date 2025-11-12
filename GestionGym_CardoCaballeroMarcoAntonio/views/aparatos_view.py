"""
Vista de gestión de aparatos
"""

import customtkinter as ctk
from tkinter import messagebox


class AparatosView(ctk.CTkFrame):
    """Vista para gestionar aparatos"""
    
    def __init__(self, parent, db):
        super().__init__(parent, corner_radius=0)
        
        self.db = db
        self.aparatos = []
        self.aparato_seleccionado = None
        
        self._create_widgets()
        self._load_aparatos()
    
    def _create_widgets(self):
        """Crea los widgets de la vista"""
        
        # Configurar grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # Título
        title = ctk.CTkLabel(
            self,
            text="Gestión de Aparatos",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="w")
        
        # ===== PANEL IZQUIERDO: Formulario =====
        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=0, padx=(20, 10), pady=(0, 20), sticky="nsew")
        
        # Formulario
        ctk.CTkLabel(
            form_frame,
            text="Datos del Aparato",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(padx=20, pady=(20, 10), anchor="w")
        
        # Nombre
        ctk.CTkLabel(form_frame, text="Nombre del Aparato *", anchor="w").pack(padx=20, pady=(10, 0), fill="x")
        self.entry_nombre = ctk.CTkEntry(form_frame, placeholder_text="Ej: Cinta de Correr #1")
        self.entry_nombre.pack(padx=20, pady=(5, 0), fill="x")
        
        # Tipo
        ctk.CTkLabel(form_frame, text="Tipo *", anchor="w").pack(padx=20, pady=(10, 0), fill="x")
        self.combo_tipo = ctk.CTkComboBox(
            form_frame,
            values=["Cardio", "Fuerza", "Funcional", "Estiramiento", "Otro"],
            state="readonly"
        )
        self.combo_tipo.pack(padx=20, pady=(5, 0), fill="x")
        self.combo_tipo.set("Cardio")
        
        # Descripción
        ctk.CTkLabel(form_frame, text="Descripción", anchor="w").pack(padx=20, pady=(10, 0), fill="x")
        self.text_descripcion = ctk.CTkTextbox(form_frame, height=100)
        self.text_descripcion.pack(padx=20, pady=(5, 0), fill="x")
        
        # Botones
        buttons_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        buttons_frame.pack(padx=20, pady=20, fill="x")
        buttons_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.btn_guardar = ctk.CTkButton(
            buttons_frame,
            text="💾 Guardar",
            command=self._guardar_aparato,
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
            command=self._eliminar_aparato,
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
        list_frame.grid_rowconfigure(1, weight=1)
        
        # Título
        title_frame = ctk.CTkFrame(list_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="ew")
        title_frame.grid_columnconfigure(0, weight=1)
        
        ctk.CTkLabel(
            title_frame,
            text="Aparatos Disponibles",
            font=ctk.CTkFont(size=18, weight="bold")
        ).grid(row=0, column=0, sticky="w")
        
        btn_refresh = ctk.CTkButton(
            title_frame,
            text="🔄 Actualizar",
            width=120,
            command=self._load_aparatos
        )
        btn_refresh.grid(row=0, column=1)
        
        # Lista de aparatos
        self.list_aparatos = ctk.CTkScrollableFrame(list_frame)
        self.list_aparatos.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        self.list_aparatos.grid_columnconfigure(0, weight=1)
    
    def _load_aparatos(self):
        """Carga la lista de aparatos"""
        self.aparatos = self.db.obtener_todos_aparatos(solo_activos=True)
        self._mostrar_aparatos()
    
    def _mostrar_aparatos(self):
        """Muestra la lista de aparatos"""
        # Limpiar lista
        for widget in self.list_aparatos.winfo_children():
            widget.destroy()
        
        if not self.aparatos:
            label = ctk.CTkLabel(
                self.list_aparatos,
                text="No hay aparatos registrados",
                text_color="gray"
            )
            label.pack(pady=20)
            return
        
        # Agrupar por tipo
        aparatos_por_tipo = {}
        for aparato in self.aparatos:
            tipo = aparato['tipo']
            if tipo not in aparatos_por_tipo:
                aparatos_por_tipo[tipo] = []
            aparatos_por_tipo[tipo].append(aparato)
        
        # Mostrar por tipo
        for tipo, aparatos in aparatos_por_tipo.items():
            # Encabezado de tipo
            tipo_label = ctk.CTkLabel(
                self.list_aparatos,
                text=f"🏋️ {tipo} ({len(aparatos)})",
                font=ctk.CTkFont(size=16, weight="bold"),
                anchor="w"
            )
            tipo_label.pack(fill="x", pady=(10, 5))
            
            # Aparatos del tipo
            for aparato in aparatos:
                self._create_aparato_card(aparato)
    
    def _create_aparato_card(self, aparato):
        """Crea una tarjeta de aparato"""
        card = ctk.CTkFrame(self.list_aparatos)
        card.pack(fill="x", pady=3)
        card.grid_columnconfigure(0, weight=1)
        
        # Información
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.grid(row=0, column=0, padx=10, pady=8, sticky="ew")
        
        # Nombre
        nombre_label = ctk.CTkLabel(
            info_frame,
            text=aparato['nombre'],
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w"
        )
        nombre_label.pack(fill="x")
        
        # Descripción
        if aparato['descripcion']:
            desc_label = ctk.CTkLabel(
                info_frame,
                text=aparato['descripcion'][:50] + ("..." if len(aparato['descripcion']) > 50 else ""),
                font=ctk.CTkFont(size=10),
                text_color="gray",
                anchor="w"
            )
            desc_label.pack(fill="x")
        
        # Botón seleccionar
        btn_seleccionar = ctk.CTkButton(
            card,
            text="✏️",
            width=40,
            command=lambda a=aparato: self._seleccionar_aparato(a)
        )
        btn_seleccionar.grid(row=0, column=1, padx=10)
    
    def _seleccionar_aparato(self, aparato):
        """Selecciona un aparato para editar"""
        self.aparato_seleccionado = aparato
        
        # Llenar formulario
        self.entry_nombre.delete(0, "end")
        self.entry_nombre.insert(0, aparato['nombre'])
        
        self.combo_tipo.set(aparato['tipo'])
        
        self.text_descripcion.delete("1.0", "end")
        if aparato['descripcion']:
            self.text_descripcion.insert("1.0", aparato['descripcion'])
        
        # Habilitar botón eliminar
        self.btn_eliminar.configure(state="normal")
        self.btn_guardar.configure(text="💾 Actualizar")
    
    def _limpiar_formulario(self):
        """Limpia el formulario"""
        self.entry_nombre.delete(0, "end")
        self.combo_tipo.set("Cardio")
        self.text_descripcion.delete("1.0", "end")
        
        self.aparato_seleccionado = None
        self.btn_eliminar.configure(state="disabled")
        self.btn_guardar.configure(text="💾 Guardar")
    
    def _guardar_aparato(self):
        """Guarda o actualiza un aparato"""
        # Obtener datos
        nombre = self.entry_nombre.get().strip()
        tipo = self.combo_tipo.get()
        descripcion = self.text_descripcion.get("1.0", "end").strip()
        
        # Validar
        if not nombre:
            messagebox.showerror("Error", "El nombre del aparato es obligatorio")
            return
        
        if len(nombre) < 3:
            messagebox.showerror("Error", "El nombre debe tener al menos 3 caracteres")
            return
        
        try:
            if self.aparato_seleccionado:
                # Actualizar
                self.db.actualizar_aparato(
                    self.aparato_seleccionado['id_aparato'],
                    nombre=nombre,
                    tipo=tipo,
                    descripcion=descripcion
                )
                messagebox.showinfo("Éxito", "Aparato actualizado correctamente")
            else:
                # Crear nuevo
                self.db.crear_aparato(nombre, tipo, descripcion)
                messagebox.showinfo("Éxito", "Aparato creado correctamente")
            
            self._limpiar_formulario()
            self._load_aparatos()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar aparato:\n{str(e)}")
    
    def _eliminar_aparato(self):
        """Desactiva un aparato"""
        if not self.aparato_seleccionado:
            return
        
        if messagebox.askyesno("Confirmar", 
                               f"¿Desactivar el aparato {self.aparato_seleccionado['nombre']}?"):
            try:
                self.db.desactivar_aparato(self.aparato_seleccionado['id_aparato'])
                messagebox.showinfo("Éxito", "Aparato desactivado correctamente")
                self._limpiar_formulario()
                self._load_aparatos()
            except Exception as e:
                messagebox.showerror("Error", f"Error al desactivar aparato:\n{str(e)}")
