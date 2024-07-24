import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

class LoginView(tk.Tk):
    def __init__(self, controller):
        super().__init__()
        self.title("Inicio de Sesión")
        self.geometry("500x350")
        self.controller = controller
        self.label_username = ttk.Label(self, text="Usuario:")
        self.label_password = ttk.Label(self, text="Contraseña:")
        self.entry_username = ttk.Entry(self)
        self.entry_password = ttk.Entry(self, show="*")
        self.button_login = ttk.Button(self, text="Iniciar Sesión", command=self.login)

        self.label_username.pack()
        self.entry_username.pack()
        self.label_password.pack()
        self.entry_password.pack()
        self.button_login.pack()

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        self.controller.login(username, password)

class HRManagementView(tk.Tk):
    def __init__(self, controller, tipo_usuario):
        super().__init__()
        self.title("Gestión de Recursos Humanos")
        self.geometry("800x600")

        self.controller = controller
        self.tipo_usuario = tipo_usuario
   
        # Menú de navegación
        self.menu_bar = tk.Menu(self)
        self.configure(menu=self.menu_bar)

        if self.tipo_usuario == 'jefe_rrhh':
            self.menu_rrhh = tk.Menu(self.menu_bar, tearoff=0)
            self.menu_bar.add_cascade(label="Opciones RR.HH...", menu=self.menu_rrhh)
            self.menu_rrhh.add_command(label="Editar Perfil", command=self.editar_perfil)
            self.menu_rrhh.add_command(label="Listar Trabajadores", command=self.listar_trabajadores)
            self.menu_rrhh.add_command(label="Gestionar Fichas Pendientes", command=self.gestionar_fichas_pendientes)
              # Crear una tabla para mostrar los trabajadores
            self.table = ttk.Treeview(self, columns=("ID","rut", "Nombre", "Cargo", "Departamento","Estado"))
            self.table.heading("#1", text="ID")
            self.table.heading("#2", text="RUT")
            self.table.heading("#3", text="Nombre")
            self.table.heading("#4", text="Cargo")
            self.table.heading("#5", text="Departamento")
            self.table.heading("#6", text="Estado")
            self.table.pack(expand=True, fill="both")

        elif self.tipo_usuario == 'personal_rrhh':
            self.menu_rrhh = tk.Menu(self.menu_bar, tearoff=0)
            self.menu_bar.add_cascade(label="Opciones RR.HH...", menu=self.menu_rrhh)
            self.menu_rrhh.add_command(label="Editar Perfil", command=self.editar_perfil)
            self.menu_rrhh.add_command(label="Ver Fichas", command=self.ver_fichas)
            self.menu_rrhh.add_command(label="Agregar Ficha Trabajador", command=self.agregar_ficha_trabajador)
             # Crear una tabla para mostrar los trabajadores
            self.table = ttk.Treeview(self, columns=("ID","Nombre", "Cargo", "Departamento", "fecha ingreso","Estado"))
            self.table.heading("#1", text="ID")
            self.table.heading("#2", text="Nombre")
            self.table.heading("#3", text="Cargo")
            self.table.heading("#4", text="Departamento")
            self.table.heading("#5", text="fecha ingreso")
            self.table.heading("#6", text="Estado")
            self.table.pack(expand=True, fill="both")

        elif self.tipo_usuario == 'empleado':
            self.menu_empleado = tk.Menu(self.menu_bar, tearoff=0)
            self.menu_bar.add_cascade(label="Empleado", menu=self.menu_empleado)
            self.menu_empleado.add_command(label="Configurar Datos", command=self.editar_perfil)
    #listar trabajadores realizado
    def listar_trabajadores(self):
        workers_list = self.controller.get_workers_list()
        self.table.delete(*self.table.get_children())  # Limpiar tabla antes de actualizar
        for worker in workers_list:
            self.table.insert("", "end", values=(worker.get('id', 'N/A'), worker.get('rut', 'N/A'),
                                                worker.get('nombre', 'N/A'), worker.get('nombre_cargo', 'N/A'),
                                                worker.get('nombre_departamento', 'N/A'), worker.get('estado_ficha', 'N/A')))

    def editar_perfil(self):
        self.controller.show_edit_profile_window()
        
    #Gestion de fichas
    def gestionar_fichas_pendientes(self):
        # Crear una nueva ventana para gestionar las fichas pendientes
        ficha_window = tk.Toplevel(self.root)
        ficha_window.title("Fichas Pendientes")

        # Crear el Treeview con columnas especificadas
        columns = ("id", "nombre", "fecha_ingreso", "estado", "acciones")
        tree = ttk.Treeview(ficha_window, columns=columns, show="headings")
        tree.heading("id", text="ID")
        tree.heading("nombre", text="Nombre")
        tree.heading("fecha_ingreso", text="Fecha Ingreso")
        tree.heading("estado", text="Estado")
        tree.heading("acciones", text="Acciones")

        # Definir las acciones de aceptar y denegar
        def aceptar(id):
            # Lógica para aceptar la ficha
            messagebox.showinfo("Aceptar", f"Ficha con ID {id} aceptada.")
            # Actualizar el estado en la base de datos (lógica aquí)

        def denegar(id):
            # Lógica para denegar la ficha
            messagebox.showinfo("Denegar", f"Ficha con ID {id} denegada.")
            # Actualizar el estado en la base de datos (lógica aquí)

        # Insertar datos en el Treeview
        for form in self.user_model.get_pending_forms():
            tree.insert("", "end", values=(form['id_ficha'], form['nombre_trabajador'], form['fecha_ingreso'], form['estado']))

        # Agregar botones de acción
        for child in tree.get_children():
            item = tree.item(child)
            id = item['values'][0]
            accept_button = tk.Button(ficha_window, text="Aceptar", command=lambda id=id: aceptar(id), bg="green", fg="white")
            deny_button = tk.Button(ficha_window, text="Denegar", command=lambda id=id: denegar(id), bg="red", fg="white")
            tree.set(child, "acciones", f"{accept_button} {deny_button}")

        tree.pack(fill=tk.BOTH, expand=True)
   
    def ver_fichas(self):
        forms_list = self.controller.get_user_forms()
        self.table.delete(*self.table.get_children())  # Limpiar tabla antes de actualizar
        for form in forms_list:
           self.table.insert("", "end", values=(form.get('id', 'N/A'), form.get('nombre', 'N/A'),
                                                form.get('nombre_cargo', 'N/A'), form.get('nombre_departamento', 'N/A'),
                                                form.get('fechaIngreso', 'N/A'), form.get('estado_ficha', 'N/A')))

    def agregar_ficha_trabajador(self):
        self.controller.agregar_ficha_trabajador()


