"""
Vista de gestión de pagos y recibos
"""

import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from utils.validators import Validators


class PagosView(ctk.CTkFrame):
    """Vista para gestionar pagos y recibos"""
    
    def __init__(self, parent, db):
        super().__init__(parent, corner_radius=0)
        
        self.db = db
        self.recibos = []
        
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
            text="Gestión de Pagos",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.grid(row=0, column=0, columnspan=2, padx=20, pady=20, sticky="w")
        
        # ===== PANEL IZQUIERDO: Acciones =====
        actions_frame = ctk.CTkFrame(self)
        actions_frame.grid(row=1, column=0, padx=(20, 10), pady=(0, 20), sticky="nsew")
        
        # Generar recibos
        ctk.CTkLabel(
            actions_frame,
            text="Generar Recibos Mensuales",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(padx=20, pady=(20, 10), anchor="w")
        
        ctk.CTkLabel(
            actions_frame,
            text="Genera recibos para todos los clientes activos",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(padx=20, pady=(0, 15), anchor="w")
        
        # Mes
        ctk.CTkLabel(actions_frame, text="Mes *", anchor="w").pack(padx=20, pady=(10, 0), fill="x")
        self.combo_mes = ctk.CTkComboBox(
            actions_frame,
            values=[Validators.obtener_nombre_mes(i) for i in range(1, 13)],
            state="readonly"
        )
        self.combo_mes.pack(padx=20, pady=(5, 0), fill="x")
        mes_actual = datetime.now().month
        self.combo_mes.set(Validators.obtener_nombre_mes(mes_actual))
        
        # Año
        ctk.CTkLabel(actions_frame, text="Año *", anchor="w").pack(padx=20, pady=(10, 0), fill="x")
        anio_actual = datetime.now().year
        self.combo_anio = ctk.CTkComboBox(
            actions_frame,
            values=[str(y) for y in range(anio_actual - 1, anio_actual + 2)],
            state="readonly"
        )
        self.combo_anio.pack(padx=20, pady=(5, 0), fill="x")
        self.combo_anio.set(str(anio_actual))
        
        # Monto
        ctk.CTkLabel(actions_frame, text="Monto Mensual *", anchor="w").pack(padx=20, pady=(10, 0), fill="x")
        self.entry_monto = ctk.CTkEntry(actions_frame, placeholder_text="Ej: 5000")
        self.entry_monto.pack(padx=20, pady=(5, 0), fill="x")
        self.entry_monto.insert(0, "5000")
        
        # Botón generar
        btn_generar = ctk.CTkButton(
            actions_frame,
            text="📋 Generar Recibos",
            command=self._generar_recibos,
            height=40
        )
        btn_generar.pack(padx=20, pady=20, fill="x")
        
        # Separador
        separator = ctk.CTkFrame(actions_frame, height=2)
        separator.pack(padx=20, pady=10, fill="x")
        
        # Registrar pago individual
        ctk.CTkLabel(
            actions_frame,
            text="Registrar Pago",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(padx=20, pady=(20, 10), anchor="w")
        
        # Cliente
        ctk.CTkLabel(actions_frame, text="Cliente *", anchor="w").pack(padx=20, pady=(10, 0), fill="x")
        self.combo_cliente = ctk.CTkComboBox(actions_frame, state="readonly")
        self.combo_cliente.pack(padx=20, pady=(5, 0), fill="x")
        self.combo_cliente.configure(command=lambda x: self._cargar_recibos_pendientes())
        
        # Recibo pendiente
        ctk.CTkLabel(actions_frame, text="Recibo Pendiente *", anchor="w").pack(padx=20, pady=(10, 0), fill="x")
        self.combo_recibo = ctk.CTkComboBox(actions_frame, state="readonly")
        self.combo_recibo.pack(padx=20, pady=(5, 0), fill="x")
        
        # Botón registrar pago
        btn_pagar = ctk.CTkButton(
            actions_frame,
            text="💰 Registrar Pago",
            command=self._registrar_pago,
            height=40,
            fg_color="green",
            hover_color="darkgreen"
        )
        btn_pagar.pack(padx=20, pady=20, fill="x")
        
        # ===== PANEL DERECHO: Listas =====
        right_frame = ctk.CTkFrame(self)
        right_frame.grid(row=1, column=1, padx=(10, 20), pady=(0, 20), sticky="nsew")
        right_frame.grid_columnconfigure(0, weight=1)
        right_frame.grid_rowconfigure(1, weight=1)
        
        # Pestañas
        self.tabview = ctk.CTkTabview(right_frame)
        self.tabview.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Tab Morosos
        self.tab_morosos = self.tabview.add("⚠️ Clientes Morosos")
        self.tab_morosos.grid_columnconfigure(0, weight=1)
        self.tab_morosos.grid_rowconfigure(0, weight=1)
        
        self.list_morosos = ctk.CTkScrollableFrame(self.tab_morosos)
        self.list_morosos.grid(row=0, column=0, sticky="nsew")
        self.list_morosos.grid_columnconfigure(0, weight=1)
        
        # Tab Todos los Recibos
        self.tab_recibos = self.tabview.add("📋 Todos los Recibos")
        self.tab_recibos.grid_columnconfigure(0, weight=1)
        self.tab_recibos.grid_rowconfigure(1, weight=1)
        
        # Filtro
        filter_frame = ctk.CTkFrame(self.tab_recibos, fg_color="transparent")
        filter_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        filter_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(filter_frame, text="Filtrar:").grid(row=0, column=0, padx=5)
        
        self.combo_filtro = ctk.CTkComboBox(
            filter_frame,
            values=["Todos", "Pendientes", "Pagados"],
            state="readonly",
            command=lambda x: self._load_recibos()
        )
        self.combo_filtro.grid(row=0, column=1, padx=5, sticky="ew")
        self.combo_filtro.set("Todos")
        
        btn_refresh = ctk.CTkButton(
            filter_frame,
            text="🔄",
            width=40,
            command=self._load_data
        )
        btn_refresh.grid(row=0, column=2, padx=5)
        
        self.list_recibos = ctk.CTkScrollableFrame(self.tab_recibos)
        self.list_recibos.grid(row=1, column=0, sticky="nsew")
        self.list_recibos.grid_columnconfigure(0, weight=1)
    
    def _load_data(self):
        """Carga datos iniciales"""
        # Cargar clientes
        clientes = self.db.obtener_todos_clientes(solo_activos=True)
        cliente_nombres = [f"{c['nombre']} ({c['dni']})" for c in clientes]
        self.combo_cliente.configure(values=cliente_nombres if cliente_nombres else ["No hay clientes"])
        if cliente_nombres:
            self.combo_cliente.set(cliente_nombres[0])
            self._cargar_recibos_pendientes()
        
        # Cargar morosos
        self._load_morosos()
        
        # Cargar recibos
        self._load_recibos()
    
    def _generar_recibos(self):
        """Genera recibos mensuales para todos los clientes"""
        try:
            # Obtener datos
            mes_nombre = self.combo_mes.get()
            mes = list(Validators.obtener_nombre_mes(i) for i in range(1, 13)).index(mes_nombre) + 1
            anio = int(self.combo_anio.get())
            monto_str = self.entry_monto.get().strip()
            
            # Validar monto
            valido, msg = Validators.validar_monto(monto_str)
            if not valido:
                messagebox.showerror("Error", msg)
                return
            
            monto = float(monto_str)
            
            # Confirmar
            if not messagebox.askyesno("Confirmar", 
                                      f"¿Generar recibos de ${monto} para {mes_nombre} {anio}?"):
                return
            
            # Generar recibos
            cantidad = self.db.generar_recibos_mes(mes, anio, monto)
            
            if cantidad > 0:
                messagebox.showinfo("Éxito", f"Se generaron {cantidad} recibos correctamente")
                self._load_data()
            else:
                messagebox.showinfo("Información", 
                                  "No se generaron recibos. Todos los clientes ya tienen recibo para este mes.")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar recibos:\n{str(e)}")
    
    def _cargar_recibos_pendientes(self):
        """Carga los recibos pendientes del cliente seleccionado"""
        try:
            cliente_text = self.combo_cliente.get()
            if not cliente_text or cliente_text == "No hay clientes":
                self.combo_recibo.configure(values=["No hay recibos"])
                return
            
            clientes = self.db.obtener_todos_clientes(solo_activos=True)
            dni = cliente_text.split("(")[1].split(")")[0]
            cliente = next((c for c in clientes if c['dni'] == dni), None)
            
            if not cliente:
                return
            
            recibos = self.db.obtener_recibos_pendientes(cliente['id_cliente'])
            
            if recibos:
                recibo_textos = [
                    f"{Validators.obtener_nombre_mes(r['mes'])} {r['anio']} - ${r['monto']}"
                    for r in recibos
                ]
                self.combo_recibo.configure(values=recibo_textos)
                self.combo_recibo.set(recibo_textos[0])
            else:
                self.combo_recibo.configure(values=["No hay recibos pendientes"])
                self.combo_recibo.set("No hay recibos pendientes")
        
        except Exception as e:
            print(f"Error al cargar recibos pendientes: {e}")
    
    def _registrar_pago(self):
        """Registra el pago de un recibo"""
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
            
            # Obtener recibo
            recibo_text = self.combo_recibo.get()
            if not recibo_text or recibo_text == "No hay recibos pendientes":
                messagebox.showwarning("Advertencia", "El cliente no tiene recibos pendientes")
                return
            
            # Buscar el recibo
            recibos = self.db.obtener_recibos_pendientes(cliente['id_cliente'])
            mes_anio = recibo_text.split(" - ")[0]
            recibo = None
            
            for r in recibos:
                if f"{Validators.obtener_nombre_mes(r['mes'])} {r['anio']}" == mes_anio:
                    recibo = r
                    break
            
            if not recibo:
                messagebox.showerror("Error", "Recibo no encontrado")
                return
            
            # Confirmar
            if not messagebox.askyesno("Confirmar", 
                                      f"¿Registrar pago de ${recibo['monto']} para {mes_anio}?"):
                return
            
            # Registrar pago
            self.db.registrar_pago(recibo['id_recibo'])
            messagebox.showinfo("Éxito", "Pago registrado correctamente")
            
            # Recargar datos
            self._cargar_recibos_pendientes()
            self._load_data()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar pago:\n{str(e)}")
    
    def _load_morosos(self):
        """Carga la lista de clientes morosos"""
        morosos = self.db.obtener_clientes_morosos()
        self._mostrar_morosos(morosos)
    
    def _mostrar_morosos(self, morosos):
        """Muestra la lista de clientes morosos"""
        # Limpiar lista
        for widget in self.list_morosos.winfo_children():
            widget.destroy()
        
        if not morosos:
            label = ctk.CTkLabel(
                self.list_morosos,
                text="✅ No hay clientes morosos",
                text_color="green",
                font=ctk.CTkFont(size=14, weight="bold")
            )
            label.pack(pady=20)
            return
        
        # Agrupar por cliente
        morosos_por_cliente = {}
        for moroso in morosos:
            id_cliente = moroso['id_cliente']
            if id_cliente not in morosos_por_cliente:
                morosos_por_cliente[id_cliente] = {
                    'info': moroso,
                    'recibos': []
                }
            morosos_por_cliente[id_cliente]['recibos'].append(moroso)
        
        # Mostrar morosos
        for data in morosos_por_cliente.values():
            self._create_moroso_card(data)
    
    def _create_moroso_card(self, data):
        """Crea una tarjeta de cliente moroso"""
        info = data['info']
        recibos = data['recibos']
        
        card = ctk.CTkFrame(self.list_morosos, fg_color=("#FF8C00", "#FF6B00"))
        card.pack(fill="x", pady=5)
        
        # Nombre y DNI
        nombre_label = ctk.CTkLabel(
            card,
            text=f"👤 {info['nombre']}",
            font=ctk.CTkFont(size=14, weight="bold"),
            anchor="w"
        )
        nombre_label.pack(padx=15, pady=(15, 2), fill="x")
        
        dni_label = ctk.CTkLabel(
            card,
            text=f"DNI: {info['dni']}",
            font=ctk.CTkFont(size=11),
            anchor="w"
        )
        dni_label.pack(padx=15, pady=2, fill="x")
        
        # Contacto
        if info['telefono']:
            tel_label = ctk.CTkLabel(
                card,
                text=f"📞 {info['telefono']}",
                font=ctk.CTkFont(size=11),
                anchor="w"
            )
            tel_label.pack(padx=15, pady=2, fill="x")
        
        # Recibos pendientes
        total_deuda = sum(r['monto'] for r in recibos)
        deuda_label = ctk.CTkLabel(
            card,
            text=f"💰 Deuda total: ${total_deuda:.2f} ({len(recibos)} recibo{'s' if len(recibos) > 1 else ''})",
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        deuda_label.pack(padx=15, pady=(10, 2), fill="x")
        
        # Detalle de recibos
        for recibo in recibos:
            recibo_text = f"• {Validators.obtener_nombre_mes(recibo['mes'])} {recibo['anio']} - ${recibo['monto']} ({int(recibo['dias_mora'])} días)"
            recibo_label = ctk.CTkLabel(
                card,
                text=recibo_text,
                font=ctk.CTkFont(size=10),
                anchor="w"
            )
            recibo_label.pack(padx=25, pady=1, fill="x")
        
        # Espaciado final
        ctk.CTkLabel(card, text="").pack(pady=5)
    
    def _load_recibos(self):
        """Carga la lista de recibos según el filtro"""
        filtro = self.combo_filtro.get()
        
        if filtro == "Pendientes":
            recibos = self.db.obtener_recibos_pendientes()
        elif filtro == "Pagados":
            # Obtener todos y filtrar pagados
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT r.*, c.nombre as nombre_cliente, c.dni
                    FROM recibos r
                    JOIN clientes c ON r.id_cliente = c.id_cliente
                    WHERE r.pagado = 1
                    ORDER BY r.anio DESC, r.mes DESC
                """)
                recibos = [dict(row) for row in cursor.fetchall()]
        else:  # Todos
            with self.db.get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT r.*, c.nombre as nombre_cliente, c.dni
                    FROM recibos r
                    JOIN clientes c ON r.id_cliente = c.id_cliente
                    ORDER BY r.anio DESC, r.mes DESC, r.pagado ASC
                """)
                recibos = [dict(row) for row in cursor.fetchall()]
        
        self._mostrar_recibos(recibos)
    
    def _mostrar_recibos(self, recibos):
        """Muestra la lista de recibos"""
        # Limpiar lista
        for widget in self.list_recibos.winfo_children():
            widget.destroy()
        
        if not recibos:
            label = ctk.CTkLabel(
                self.list_recibos,
                text="No hay recibos para mostrar",
                text_color="gray"
            )
            label.pack(pady=20)
            return
        
        # Mostrar recibos
        for recibo in recibos:
            self._create_recibo_card(recibo)
    
    def _create_recibo_card(self, recibo):
        """Crea una tarjeta de recibo"""
        color = "green" if recibo['pagado'] else None
        
        card = ctk.CTkFrame(self.list_recibos)
        card.pack(fill="x", pady=3)
        card.grid_columnconfigure(0, weight=1)
        
        # Info
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.grid(row=0, column=0, padx=10, pady=8, sticky="ew")
        
        # Cliente y período
        texto = f"{'✅' if recibo['pagado'] else '⏳'} {recibo['nombre_cliente']} - {Validators.obtener_nombre_mes(recibo['mes'])} {recibo['anio']}"
        label = ctk.CTkLabel(
            info_frame,
            text=texto,
            font=ctk.CTkFont(size=12, weight="bold"),
            anchor="w"
        )
        label.pack(fill="x")
        
        # Monto y estado
        estado = f"Pagado el {recibo['fecha_pago']}" if recibo['pagado'] else "Pendiente de pago"
        detalle = f"${recibo['monto']:.2f} - {estado}"
        label_detalle = ctk.CTkLabel(
            info_frame,
            text=detalle,
            font=ctk.CTkFont(size=10),
            text_color="gray",
            anchor="w"
        )
        label_detalle.pack(fill="x")
