import os
from utils import read_json, write_json

FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "rooms.json")


class RoomManager:
    def __init__(self):
        self.rooms = read_json(FILE_PATH)

    def save_data(self):
        write_json(FILE_PATH, self.rooms)

    def find_room(self, room_number):
        for i in range(len(self.rooms)):
            if self.rooms[i]["room_number"] == room_number:
                return i
        return -1

    def assign_room(self, student_id, room_number, student_gender):
        pos = self.find_room(room_number)
        if pos == -1:
            print(f"Khong tim thay phong {room_number}!")
            return False

        room = self.rooms[pos]

        # Kiem tra gioi tinh
        if room["gender"] != student_gender:
            print(f"Phong {room_number} danh cho {room['gender']}, khong phu hop!")
            return False

        # Kiem tra con cho khong
        if room["available_beds"] <= 0:
            print(f"Phong {room_number} da day!")
            return False

        # Kiem tra sv da o phong nay chua
        if student_id in room["current_students"]:
            print(f"Sinh vien {student_id} da o phong {room_number} roi!")
            return False

        room["current_students"].append(student_id)
        room["available_beds"] -= 1
        print(f"Da xep sinh vien {student_id} vao phong {room_number} "
              f"(con {room['available_beds']} cho trong)")
        return True

    def transfer_room(self, student_id, old_room, new_room, student_gender):
        pos_old = self.find_room(old_room)
        pos_new = self.find_room(new_room)

        if pos_old == -1:
            print(f"Khong tim thay phong cu {old_room}!")
            return False
        if pos_new == -1:
            print(f"Khong tim thay phong moi {new_room}!")
            return False

        room_old = self.rooms[pos_old]
        room_new = self.rooms[pos_new]

        # Kiem tra sv co dang o phong cu khong
        if student_id not in room_old["current_students"]:
            print(f"Sinh vien {student_id} khong o phong {old_room}!")
            return False

        # Kiem tra gioi tinh phong moi
        if room_new["gender"] != student_gender:
            print(f"Phong {new_room} danh cho {room_new['gender']}, khong phu hop!")
            return False

        # Kiem tra phong moi con cho khong
        if room_new["available_beds"] <= 0:
            print(f"Phong {new_room} da day, khong the chuyen!")
            return False

        # Roi phong cu
        room_old["current_students"].remove(student_id)
        room_old["available_beds"] += 1

        # Vao phong moi
        room_new["current_students"].append(student_id)
        room_new["available_beds"] -= 1

        print(f"Da chuyen sinh vien {student_id} tu phong {old_room} sang phong {new_room}")
        return True

    def remove_student(self, student_id, room_number):
        pos = self.find_room(room_number)
        if pos != -1:
            room = self.rooms[pos]
            if student_id in room["current_students"]:
                room["current_students"].remove(student_id)
                room["available_beds"] += 1
                return True
        return False

    def get_room_by_number(self, room_number):
        pos = self.find_room(room_number)
        if pos != -1:
            return self.rooms[pos]
        return None

    def add_room(self, room_data):
        if self.find_room(room_data["room_number"]) != -1:
            return False
        self.rooms.append(room_data)
        self.save_data()
        return True

    def get_all_rooms(self):
        return self.rooms