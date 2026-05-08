import customtkinter as ctk
import requests

class LoginScreen(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Login")
        self.geometry("400x300")
        self.create_widgets()

    def create_widgets(self):
        self.username_label = ctk.CTkLabel(self, text="Email:")
        self.username_label.pack(pady=10)
        self.username_entry = ctk.CTkEntry(self)
        self.username_entry.pack(pady=10)

        self.password_label = ctk.CTkLabel(self, text="Password:")
        self.password_label.pack(pady=10)
        self.password_entry = ctk.CTkEntry(self, show="*")
        self.password_entry.pack(pady=10)

        self.login_button = ctk.CTkButton(self, text="Login", command=self.login)
        self.login_button.pack(pady=20)
        
        self.error_label = ctk.CTkLabel(self, text="", text_color="red")
        self.error_label.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        response = requests.post("http://localhost:8000/login", json={
            "email": username,
            "mot_de_passe": password
        })
        if response.status_code == 200:
            data = response.json()
            self.token = data["access_token"]
            self.role = data["role"]
            self.destroy()
            if self.role == "admin":
                print("Open admin panel")
            else:
                print("Open user panel")
        else:
            self.error_label.configure(text="Invalid email or password !")

if __name__ == "__main__":
    app = LoginScreen()
    app.mainloop()