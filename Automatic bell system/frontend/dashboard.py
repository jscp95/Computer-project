import customtkinter as ctk
from backend.bell_controller import BellController

class Dashboard(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.bell = BellController()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        title = ctk.CTkLabel(
            self,
            text="Automatic School Bell System",
            font=("Segoe UI", 30, "bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=30)

        self.status_label = ctk.CTkLabel(
            self,
            text="Status: Ready",
            font=("Segoe UI", 18)
        )
        self.status_label.grid(row=1, column=0, columnspan=2, pady=10)

        ring_button = ctk.CTkButton(
            self,
            text="🔔 Ring Bell Now",
            command=self.ring_bell,
            height=55,
            font=("Segoe UI", 20, "bold")
        )
        ring_button.grid(row=2, column=0, padx=25, pady=25, sticky="ew")

        stop_button = ctk.CTkButton(
            self,
            text="⛔ Stop Bell",
            command=self.stop_bell,
            height=55,
            fg_color="#d9534f",
            hover_color="#c9302c",
            font=("Segoe UI", 20, "bold")
        )
        stop_button.grid(row=2, column=1, padx=25, pady=25, sticky="ew")

    def ring_bell(self):
        self.status_label.configure(text="Status: Bell ringing through Bluetooth speaker")
        self.bell.ring_bell(duration=10)

    def stop_bell(self):
        self.bell.stop_bell()
        self.status_label.configure(text="Status: Bell stopped")
