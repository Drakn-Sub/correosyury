from controlador import HRManagementController
from vista  import LoginView

if __name__ == "__main__":
    controlador = HRManagementController()
    login_view = LoginView(controlador)
    controlador.set_login_view(login_view)
    login_view.mainloop()
