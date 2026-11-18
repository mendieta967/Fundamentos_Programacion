from frontend.app import App
from frontend.auth.login import LoginWindow


if __name__ == "__main__":

    app = App()
    app.withdraw()
    LoginWindow(app)
    app.mainloop()
