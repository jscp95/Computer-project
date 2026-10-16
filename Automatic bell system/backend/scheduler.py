from datetime import datetime
import threading
import time

from backend.schedule_manager import get_all_schedules
from backend.log_manager import save_bell_log


class BellScheduler:
    def __init__(self, bell_controller, on_ring=None):
        self.bell = bell_controller
        self.on_ring = on_ring
        self.running = False

    def start(self):
        if not self.running:
            self.running = True

            threading.Thread(
                target=self.run,
                daemon=True
            ).start()

            print("Bell scheduler started")

    def stop(self):
        self.running = False
        print("Bell scheduler stopped")

    def run(self):
        already_rang = set()

        while self.running:
            now = datetime.now()

            current_time = now.strftime("%H:%M:%S")
            current_day = now.strftime("%a").upper()

            schedules = get_all_schedules()

            for schedule in schedules:
                schedule_id = schedule["schedule_id"]
                schedule_time = str(schedule["bell_time"])
                schedule_days = schedule["days"].upper().split(",")
                is_active = schedule["is_active"]

                print(
                    f"Checking: {schedule_time} | "
                    f"Now: {current_time} | "
                    f"Day: {current_day} | "
                    f"Days: {schedule_days} | "
                    f"Active: {is_active}"
                )

                if (
                    schedule_time == current_time
                    and current_day in schedule_days
                    and is_active
                    and schedule_id not in already_rang
                ):
                    print(f"RINGING BELL: {schedule['period_name']}")

                    self.bell.ring_bell(
                        duration=schedule["duration_seconds"]
                    )

                    save_bell_log(
                        schedule_id=schedule_id,
                        period_name=schedule["period_name"],
                        bell_type="AUTO",
                        status="SUCCESS"
                    )

                    if self.on_ring:
                        self.on_ring(schedule)

                    already_rang.add(schedule_id)

            if current_time == "00:00:00":
                already_rang.clear()

            time.sleep(1)
