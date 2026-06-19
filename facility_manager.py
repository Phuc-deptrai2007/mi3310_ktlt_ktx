import os
from utils import read_json, write_json
from datetime import date

FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "facilities.json")


class FacilityManager:
    def __init__(self):
        self.facilities = read_json(FILE_PATH)

    def save_data(self):
        write_json(FILE_PATH, self.facilities)

    def find_facility(self, facility_id):
        for i in range(len(self.facilities)):
            if self.facilities[i]["facility_id"] == facility_id:
                return i
        return -1

    def generate_facility_id(self):
        # Tu dong tao ma TB001, TB002,...
        if len(self.facilities) == 0:
            return "TB001"
        num = len(self.facilities) + 1
        return f"TB{num:03d}"

    def report_damage(self, room_number, facility_name, description, reported_by):
        # Kiem tra thiet bi co ton tai trong phong do khong
        for item in self.facilities:
            if item["room_number"] == room_number and item["facility_name"] == facility_name:
                # Them bao cao hong vao lich su sua chua
                report = {
                    "report_date"  : str(date.today()),
                    "reported_by"  : reported_by,
                    "description"  : description,
                    "repair_status": "Dang cho",
                    "repair_date"  : None
                }
                item["repair_history"].append(report)
                item["status"] = "Dang cho sua"
                self.save_data()
                return True

        # Neu khong tim thay thi tao thiet bi moi va ghi nhan luon
        new_facility = {
            "facility_id"   : self.generate_facility_id(),
            "room_number"   : room_number,
            "facility_name" : facility_name,
            "brand"         : "Chua ro",
            "install_date"  : "Chua ro",
            "status"        : "Dang cho sua",
            "repair_history": [
                {
                    "report_date"  : str(date.today()),
                    "reported_by"  : reported_by,
                    "description"  : description,
                    "repair_status": "Dang cho",
                    "repair_date"  : None
                }
            ]
        }
        self.facilities.append(new_facility)
        self.save_data()
        return True

    def update_repair_status(self, facility_id, status):
        pos = self.find_facility(facility_id)
        if pos == -1:
            return False

        item = self.facilities[pos]
        item["status"] = status

        # Cap nhat trang thai bao cao cuoi cung trong lich su
        if len(item["repair_history"]) > 0:
            last_report = item["repair_history"][-1]
            last_report["repair_status"] = status
            if status == "Da sua xong":
                last_report["repair_date"] = str(date.today())

        self.save_data()
        return True

    def get_facilities_by_room(self, room_number):
        results = []
        for item in self.facilities:
            if item["room_number"] == room_number:
                results.append(item)
        return results

    def add_facility_manual(self, facility_data):
        # Kiem tra trung ma thiet bi
        if self.find_facility(facility_data["facility_id"]) != -1:
            return False
        # Kiem tra trung ten thiet bi trong cung 1 phong
        for item in self.facilities:
            if item["room_number"] == facility_data["room_number"] and item["facility_name"] == facility_data["facility_name"]:
                return -1 # Da ton tai trong phong
        self.facilities.append(facility_data)
        self.save_data()
        return True

    def get_all_facilities(self):
        return self.facilities