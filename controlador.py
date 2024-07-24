from modelo import UserModel
from vista import HRManagementView
import tkinter as tk
from tkinter import simpledialog, messagebox, ttk

class HRManagementController:
    def __init__(self):
        self.user_model = UserModel()
        self.login_view = None
        self.logged_user = None
    
    #Login 
    def set_login_view(self, view):
        self.login_view = view

    def login(self, username, password):
        result = self.user_model.verify_user_credentials(username, password)
        if result:
            self.logged_user = username
            tipo_usuario = result[0]['tipo_usuario']
            self.show_main_view(tipo_usuario)
        else:
            self.show_login_error()

    def show_main_view(self, tipo_usuario):
        if self.login_view:
            self.login_view.destroy()  # Aquí aseguramos que self.login_view no sea None antes de llamar a destroy()
        self.main_app = HRManagementView(self, tipo_usuario)
        self.main_app.mainloop()

    def show_login_error(self):
        messagebox.showerror("Error de Inicio de Sesión", "Credenciales incorrectas.")
   
    #listar trabajadores LISTO
    def get_workers_list(self):
        return self.user_model.get_workers_list()

    def listar_trabajadores(self):
        workers_list = self.user_model.get_workers_list()
        self.main_app.text_area.delete(1.0, tk.END)
        for worker in workers_list:
            print(worker) 
            self.main_app.text_area.insert(tk.END, f"ID: {worker['id']},Rut: {worker['rut']}, Nombre: {worker['nombre']}, Cargo: {worker['nombre_cargo']}, Departamento: {worker['nombre_departamento']}, Estado: {worker['estado_ficha']}\n")
        self.main_app.text_area.insert(tk.END, "\n")
    
    #Editar perfil
    def get_logged_username(self):
        return self.logged_user
    def get_user_profile(self):
        username = self.get_logged_username()
        return self.user_model.get_user_profile(username)

    def editar_perfil(self):
        username = self.get_logged_username()
        self.main_app.text_area.delete(1.0, tk.END)
        profile = self.user_model.get_user_profile(username)
        if profile:
            self.main_app.text_area.insert(tk.END, f"Correo: {profile['correo_trabajador']}\n")
            self.main_app.text_area.insert(tk.END, f"Contactos de Emergencia: {profile['contactos_emergencia']}\n")
            self.main_app.text_area.insert(tk.END, f"Cargas Familiares: {profile['cargas_familiares']}\n")
            self.show_edit_profile_window(profile)
        else:
            self.main_app.text_area.insert(tk.END, "No se encontró el perfil.\n")

    def show_edit_profile_window(self, profile=None):
        # Obtener el perfil del usuario si no se pasa como argumento
        if profile is None:
            profile = self.user_model.get_user_profile(self.logged_user)

        # Verificar si profile es None
        if profile is None:
            messagebox.showerror("Error", "No se pudo obtener el perfil del usuario.")
            return

        # Verificar si los campos existen en el perfil
        emergency_contacts = profile.get('contactos_emergencia', 'No especificado')
        cargas_familiares = profile.get('cargas_familiares', 'No especificado')
        email = profile.get('correo_trabajador', 'No especificado')

        def update_profile():
            # Obtener los valores nuevos solo para campos editables
            new_contacts = entry_contacts.get()
            new_cargas = entry_cargas.get()
            username = self.get_logged_username() 
            
            # Llamar al modelo para actualizar solo los campos permitidos
            success = self.user_model.edit_user_profile(username, None, new_contacts, new_cargas)
            if success:
                messagebox.showinfo("Éxito", "Perfil actualizado correctamente.")
            else:
                messagebox.showerror("Error", "No se pudo actualizar el perfil.")

        # Crear ventana de edición de perfil
        edit_profile_window = tk.Toplevel(self.main_app)
        edit_profile_window.title("Editar Perfil")
        edit_profile_window.geometry("400x300")

        label_email = ttk.Label(edit_profile_window, text="Correo:")
        label_contacts = ttk.Label(edit_profile_window, text="Contactos de Emergencia:")
        label_cargas = ttk.Label(edit_profile_window, text="Cargas Familiares:")

        entry_email = ttk.Entry(edit_profile_window, width=30)
        entry_contacts = ttk.Entry(edit_profile_window, width=30)
        entry_cargas = ttk.Entry(edit_profile_window, width=30)

        # Configurar el campo de correo como no editable
        entry_email.insert(0, email)
        entry_email.config(state='disabled')  # Desactivar el campo para evitar edición

        entry_contacts.insert(0, emergency_contacts)
        entry_cargas.insert(0, cargas_familiares)

        button_update = ttk.Button(edit_profile_window, text="Actualizar", command=update_profile)

        label_email.pack(pady=10)
        entry_email.pack()
        label_contacts.pack(pady=10)
        entry_contacts.pack()
        label_cargas.pack(pady=10)
        entry_cargas.pack()
        button_update.pack(pady=20)
        
    #Ver fichas pendientes JEFE RRHH
    def gestionar_fichas_pendientes(self):
            forms_list = self.user_model.get_pending_forms()
            self.main_app.text_area.delete(1.0, tk.END)
            for form in forms_list:
                self.main_app.text_area.insert(tk.END, f"ID: {form['id_ficha']}, Nombre: {form['nombre_trabajador']}, fecha_ingreso: {form['fecha_ingreso']}, Estado: {form['estado']}\n")
            self.main_app.text_area.insert(tk.END, "\n")
        
        #Ver fichas personal rrhh LISTO
    def get_user_forms(self):
            return self.user_model.get_user_forms()
        
    def ver_fichas(self):
            forms_list = self.user_model.get_user_forms()
            self.main_app.text_area.delete(1.0, tk.END)
            for form in forms_list:
                self.main_app.text_area.insert(tk.END, f"ID: {form['id']}, Nombre: {form['nombre']}, Cargo: {form['nombre_cargo']}, departamento: {form['nombre_departamento']}, fechaIngreso: {form['fechaIngreso']}, Estado: {form['estado_ficha']}\n")
            self.main_app.text_area.insert(tk.END, "\n")
    
    #Registrar ficha
    def agregar_ficha_trabajador(self):
        def save_form():
            nombre = entry_nombre.get()
            rut = entry_rut.get()
            correo = entry_correo.get()
            cargo = combo_cargo.get()
            departamento = combo_departamento.get()

    # Obtener listas de cargas familiares y contactos de emergencia
            cargas_familiares = []
            for i in range(len(entry_nombre_familiar)):
                nombre_familiar = entry_nombre_familiar[i].get()
                parentesco = entry_parentesco[i].get()
                sexo = entry_sexo[i].get()
                if nombre_familiar and parentesco and sexo:
                    cargas_familiares.append({
                        'nombre': nombre_familiar,
                        'parentesco': parentesco,
                        'sexo': sexo
                    })

            contactos_emergencia = []
            for i in range(len(entry_nombre_contacto)):
                nombre_contacto = entry_nombre_contacto[i].get()
                telefono = entry_telefono[i].get()
                if nombre_contacto and telefono:
                    contactos_emergencia.append({
                        'nombre': nombre_contacto,
                        'telefono': telefono
                    })

            prevision = combo_prevision.get()
            afp = combo_afp.get()

            self.user_model.add_worker_form(
                nombre, rut, correo, cargo, departamento, 
                cargas_familiares, contactos_emergencia, 
                prevision, afp
            )
            messagebox.showinfo("Éxito", "Ficha de trabajador agregada correctamente.")
            add_form_window.destroy()

        add_form_window = tk.Toplevel(self.main_app)
        add_form_window.title("Agregar Ficha de Trabajador")
        add_form_window.geometry("1000x800")

    # Recuadro para Nombre, RUT, Correo, Previsión y AFP
        frame_basic_info = ttk.Frame(add_form_window, padding="5", borderwidth=2, relief='sunken')
        frame_basic_info.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        ttk.Label(frame_basic_info, text="Nombre:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        entry_nombre = ttk.Entry(frame_basic_info, width=40)
        entry_nombre.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        ttk.Label(frame_basic_info, text="RUT:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        entry_rut = ttk.Entry(frame_basic_info, width=40)
        entry_rut.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        ttk.Label(frame_basic_info, text="Correo:").grid(row=2, column=0, padx=10, pady=5, sticky='w')
        entry_correo = ttk.Entry(frame_basic_info, width=40)
        entry_correo.grid(row=2, column=1, padx=10, pady=5, sticky='w')

        ttk.Label(frame_basic_info, text="Previsión:").grid(row=3, column=0, padx=10, pady=5, sticky='w')
        combo_prevision = ttk.Combobox(frame_basic_info, values=["Fonasa", "Isapre"], state="readonly")
        combo_prevision.grid(row=3, column=1, padx=10, pady=5, sticky='w')

        ttk.Label(frame_basic_info, text="AFP:").grid(row=4, column=0, padx=10, pady=5, sticky='w')
        combo_afp = ttk.Combobox(frame_basic_info, values=["AFP1", "AFP2"], state="readonly")
        combo_afp.grid(row=4, column=1, padx=10, pady=5, sticky='w')

    # Recuadro para Cargo y Departamento
        frame_job_info = ttk.Frame(add_form_window, padding="5", borderwidth=2, relief='sunken')
        frame_job_info.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')

        ttk.Label(frame_job_info, text="Cargo:").grid(row=0, column=0, padx=10, pady=5, sticky='w')
        combo_cargo = ttk.Combobox(frame_job_info, values=[
            "Jefe RR.HH", "Jefe Finanzas", "Jefe Marketing",
            "Empleado RRHH", "Empleado Finanzas", "Empleado Marketing"
        ], state="readonly")
        combo_cargo.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        ttk.Label(frame_job_info, text="Departamento:").grid(row=1, column=0, padx=10, pady=5, sticky='w')
        combo_departamento = ttk.Combobox(frame_job_info, values=[
            "Recursos Humanos", "Finanzas", "Marketing"
        ], state="readonly")
        combo_departamento.grid(row=1, column=1, padx=10, pady=5, sticky='w')

    # Recuadro para Cargas Familiares
        frame_cargas_familiares = ttk.Frame(add_form_window, padding="5", borderwidth=2, relief='sunken')
        frame_cargas_familiares.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        ttk.Label(frame_cargas_familiares, text="Cargas Familiares:").grid(row=0, column=0, padx=10, pady=5, sticky='w', columnspan=2)

        entry_nombre_familiar = []
        entry_parentesco = []
        entry_sexo = []

        for i in range(1):  # Tres filas para cargas familiares
            ttk.Label(frame_cargas_familiares, text=f"Nombre Familiar {i+1}:").grid(row=1+i*3, column=0, padx=10, pady=5, sticky='w')
            entry_nombre_familiar.append(ttk.Entry(frame_cargas_familiares, width=40))
            entry_nombre_familiar[-1].grid(row=1+i*3, column=1, padx=10, pady=5, sticky='w')

            ttk.Label(frame_cargas_familiares, text=f"Parentesco {i+1}:").grid(row=2+i*3, column=0, padx=10, pady=5, sticky='w')
            entry_parentesco.append(ttk.Entry(frame_cargas_familiares, width=40))
            entry_parentesco[-1].grid(row=2+i*3, column=1, padx=10, pady=5, sticky='w')

            ttk.Label(frame_cargas_familiares, text=f"Sexo {i+1}:").grid(row=3+i*3, column=0, padx=10, pady=5, sticky='w')
            entry_sexo.append(ttk.Entry(frame_cargas_familiares, width=40))
            entry_sexo[-1].grid(row=3+i*3, column=1, padx=10, pady=5, sticky='w')

    # Recuadro para Contactos de Emergencia
        frame_contactos_emergencia = ttk.Frame(add_form_window, padding="5", borderwidth=2, relief='sunken')
        frame_contactos_emergencia.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        ttk.Label(frame_contactos_emergencia, text="Contactos de Emergencia:").grid(row=0, column=0, padx=10, pady=5, sticky='w', columnspan=2)

        entry_nombre_contacto = []
        entry_telefono = []

        for i in range(2):  # Dos filas para contactos de emergencia
            ttk.Label(frame_contactos_emergencia, text=f"Nombre Contacto {i+1}:").grid(row=1+i*2, column=0, padx=10, pady=5, sticky='w')
            entry_nombre_contacto.append(ttk.Entry(frame_contactos_emergencia, width=40))
            entry_nombre_contacto[-1].grid(row=1+i*2, column=1, padx=10, pady=5, sticky='w')

            ttk.Label(frame_contactos_emergencia, text=f"Teléfono {i+1}:").grid(row=2+i*2, column=0, padx=10, pady=5, sticky='w')
            entry_telefono.append(ttk.Entry(frame_contactos_emergencia, width=40))
            entry_telefono[-1].grid(row=2+i*2, column=1, padx=10, pady=5, sticky='w')

    # Botón Guardar
        button_save = tk.Button(add_form_window, text="Guardar", command=save_form, bg="blue", fg="white")
        button_save.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky='ew')
