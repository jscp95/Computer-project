import customtkinter as ctk

from backend.schedule_manager import (
    add_schedule,
    get_all_schedules,
    update_schedule,
    delete_schedule,
    toggle_schedule
)

from backend.bell_controller import BellController
from backend.log_manager import save_bell_log


class SchedulePage(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.selected_schedule_id = None
        self.bell = BellController()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=2)

        title = ctk.CTkLabel(
            self,
            text="Bell Schedule Management",
            font=("Segoe UI", 26, "bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=20)

        # ---------------- LEFT SIDE: FORM ----------------

        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        form_frame.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            form_frame,
            text="Period Name",
            font=("Segoe UI", 15)
        ).grid(row=0, column=0, padx=15, pady=10, sticky="w")

        self.period_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="Example: Period 1",
            height=38
        )
        self.period_entry.grid(row=0, column=1, padx=15, pady=10, sticky="ew")

        ctk.CTkLabel(
            form_frame,
            text="Bell Time",
            font=("Segoe UI", 15)
        ).grid(row=1, column=0, padx=15, pady=10, sticky="w")

        self.time_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="HH:MM:SS",
            height=38
        )
        self.time_entry.grid(row=1, column=1, padx=15, pady=10, sticky="ew")

        ctk.CTkLabel(
            form_frame,
            text="Duration (seconds)",
            font=("Segoe UI", 15)
        ).grid(row=2, column=0, padx=15, pady=10, sticky="w")

        self.duration_entry = ctk.CTkEntry(
            form_frame,
            placeholder_text="10",
            height=38
        )
        self.duration_entry.grid(row=2, column=1, padx=15, pady=10, sticky="ew")

        ctk.CTkLabel(
            form_frame,
            text="Days",
            font=("Segoe UI", 15)
        ).grid(row=3, column=0, padx=15, pady=10, sticky="w")

        self.days_option = ctk.CTkComboBox(
            form_frame,
            values=[
                "MON,TUE,WED,THU,FRI",
                "MON,TUE,WED,THU,FRI,SAT",
                "MON",
                "TUE",
                "WED",
                "THU",
                "FRI",
                "SAT"
            ],
            height=38
        )
        self.days_option.set("MON,TUE,WED,THU,FRI")
        self.days_option.grid(row=3, column=1, padx=15, pady=10, sticky="ew")

        self.active_switch = ctk.CTkSwitch(
            form_frame,
            text="Active"
        )
        self.active_switch.select()
        self.active_switch.grid(row=4, column=0, columnspan=2, pady=15)

        button_frame = ctk.CTkFrame(
            form_frame,
            fg_color="transparent"
        )
        button_frame.grid(row=5, column=0, columnspan=2, pady=10)

        self.add_button = ctk.CTkButton(
            button_frame,
            text="Add Schedule",
            command=self.add_schedule,
            width=130,
            height=40
        )
        self.add_button.grid(row=0, column=0, padx=8)

        self.update_button = ctk.CTkButton(
            button_frame,
            text="Update Selected",
            command=self.update_schedule,
            width=150,
            height=40,
            fg_color="#f0ad4e",
            hover_color="#ec971f"
        )
        self.update_button.grid(row=0, column=1, padx=8)

        self.delete_button = ctk.CTkButton(
            button_frame,
            text="Delete Selected",
            command=self.delete_schedule,
            width=150,
            height=40,
            fg_color="#d9534f",
            hover_color="#c9302c"
        )
        self.delete_button.grid(row=0, column=2, padx=8)

        self.toggle_button = ctk.CTkButton(
            button_frame,
            text="Enable / Disable",
            command=self.toggle_schedule,
            width=150,
            height=40,
            fg_color="#6c757d",
            hover_color="#5a6268"
        )
        self.toggle_button.grid(row=0, column=3, padx=8)

        # ---------------- MANUAL BELL CONTROLS ----------------

        manual_frame = ctk.CTkFrame(
            form_frame,
            fg_color="transparent"
        )
        manual_frame.grid(row=6, column=0, columnspan=2, pady=10)

        ring_now_button = ctk.CTkButton(
            manual_frame,
            text="🔔 Ring Bell Now",
            command=self.ring_bell_now,
            width=170,
            height=45,
            font=("Segoe UI", 16, "bold")
        )
        ring_now_button.grid(row=0, column=0, padx=8)

        stop_bell_button = ctk.CTkButton(
            manual_frame,
            text="⛔ Stop Bell",
            command=self.stop_bell_now,
            width=130,
            height=45,
            fg_color="#d9534f",
            hover_color="#c9302c",
            font=("Segoe UI", 16, "bold")
        )
        stop_bell_button.grid(row=0, column=1, padx=8)

        self.message_label = ctk.CTkLabel(
            form_frame,
            text="",
            font=("Segoe UI", 14),
            text_color="#adb5bd"
        )
        self.message_label.grid(row=7, column=0, columnspan=2, pady=10)

        # ---------------- RIGHT SIDE: SCHEDULE LIST ----------------

        table_frame = ctk.CTkFrame(self)
        table_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        table_frame.grid_rowconfigure(1, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            table_frame,
            text="Saved Bell Schedules",
            font=("Segoe UI", 20, "bold")
        ).grid(row=0, column=0, pady=15)

        self.schedule_textbox = ctk.CTkTextbox(
            table_frame,
            font=("Consolas", 14)
        )
        self.schedule_textbox.grid(row=1, column=0, padx=15, pady=10, sticky="nsew")

        refresh_button = ctk.CTkButton(
            table_frame,
            text="Refresh Schedule List",
            command=self.load_schedules,
            height=40
        )
        refresh_button.grid(row=2, column=0, pady=10)

        self.load_schedules()

    # ---------------- HELPER FUNCTIONS ----------------

    def show_message(self, message, success=True):
        self.message_label.configure(
            text=message,
            text_color="#2ecc71" if success else "#e74c3c"
        )

    def clear_form(self):
        self.period_entry.delete(0, "end")
        self.time_entry.delete(0, "end")
        self.duration_entry.delete(0, "end")
        self.days_option.set("MON,TUE,WED,THU,FRI")
        self.active_switch.select()
        self.selected_schedule_id = None

    # ---------------- MANUAL BELL ----------------

    def ring_bell_now(self):
        self.bell.ring_bell(duration=10)

        success, message = save_bell_log(
            schedule_id=None,
            period_name="Manual Bell",
            bell_type="MANUAL",
            status="SUCCESS"
        )

        if success:
            self.show_message("Manual bell is ringing through Bluetooth speaker.")
        else:
            self.show_message(message, False)

    def stop_bell_now(self):
        self.bell.stop_bell()
        self.show_message("Bell stopped.")

    # ---------------- DATABASE OPERATIONS ----------------

    def load_schedules(self):
        schedules = get_all_schedules()
        self.schedule_textbox.delete("1.0", "end")

        if not schedules:
            self.schedule_textbox.insert("end", "No schedules found.")
            return

        header = (
            f"{'ID':<5}"
            f"{'Period':<20}"
            f"{'Time':<12}"
            f"{'Duration':<12}"
            f"{'Days':<30}"
            f"{'Active':<8}\n"
        )

        self.schedule_textbox.insert("end", header)
        self.schedule_textbox.insert("end", "-" * 100 + "\n")

        for schedule in schedules:
            line = (
                f"{schedule['schedule_id']:<5}"
                f"{schedule['period_name']:<20}"
                f"{schedule['bell_time']:<12}"
                f"{schedule['duration_seconds']:<12}"
                f"{schedule['days']:<30}"
                f"{'Yes' if schedule['is_active'] else 'No':<8}\n"
            )

            self.schedule_textbox.insert("end", line)

    def add_schedule(self):
        period_name = self.period_entry.get().strip()
        bell_time = self.time_entry.get().strip()
        duration = self.duration_entry.get().strip()
        days = self.days_option.get().strip()
        is_active = bool(self.active_switch.get())

        if not period_name or not bell_time or not duration:
            self.show_message("Please fill period name, time, and duration.", False)
            return

        try:
            duration_seconds = int(duration)
        except ValueError:
            self.show_message("Duration must be a number.", False)
            return

        success, message = add_schedule(
            period_name,
            bell_time,
            duration_seconds,
            days,
            is_active
        )

        self.show_message(message, success)

        if success:
            self.clear_form()
            self.load_schedules()

    def update_schedule(self):
        schedule_id = self.period_entry.get().strip()

        if not schedule_id.isdigit():
            self.show_message("Enter the schedule ID in the Period Name box to update.", False)
            return

        period_name = self.time_entry.get().strip()
        bell_time = self.duration_entry.get().strip()
        duration = self.days_option.get().strip()
        days = self.days_option.get().strip()
        is_active = bool(self.active_switch.get())

        # Use the proper fields instead
        period_name = self.period_entry.get().strip()
        bell_time = self.time_entry.get().strip()
        duration = self.duration_entry.get().strip()

        try:
            duration_seconds = int(duration)
        except ValueError:
            self.show_message("Duration must be a number.", False)
            return

        success, message = update_schedule(
            int(schedule_id),
            period_name,
            bell_time,
            duration_seconds,
            days,
            is_active
        )

        self.show_message(message, success)

        if success:
            self.clear_form()
            self.load_schedules()

    def delete_schedule(self):
        schedule_id = self.period_entry.get().strip()

        if not schedule_id.isdigit():
            self.show_message("Enter the schedule ID in the Period Name box to delete.", False)
            return

        success, message = delete_schedule(int(schedule_id))
        self.show_message(message, success)

        if success:
            self.clear_form()
            self.load_schedules()

    def toggle_schedule(self):
        schedule_id = self.period_entry.get().strip()

        if not schedule_id.isdigit():
            self.show_message("Enter the schedule ID in the Period Name box.", False)
            return

        schedules = get_all_schedules()

        for schedule in schedules:
            if schedule["schedule_id"] == int(schedule_id):
                new_status = not schedule["is_active"]

                success, message = toggle_schedule(
                    int(schedule_id),
                    new_status
                )

                self.show_message(message, success)

                if success:
                    self.load_schedules()

                return

        self.show_message("Schedule ID not found.", False)
