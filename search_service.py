from student_manager import StudentManager
from room_manager import RoomManager

# Kich thuoc bang bam (Hash Table)
HASH_TABLE_SIZE = 101  # So nguyen to de giam xung dot


class SearchService:
    def __init__(self, student_manager, room_manager):
        self.sm = student_manager
        self.rm = room_manager

    # ─── Binary Search theo ma SV ───
    def binary_search_student(self, student_id):
        # Sap xep truoc khi tim
        self.sm.sort_by_id()
        students = self.sm.get_all_students()

        left = 0
        right = len(students) - 1

        while left <= right:
            mid = (left + right) // 2
            if students[mid]["student_id"] == student_id:
                return students[mid]
            elif students[mid]["student_id"] < student_id:
                left = mid + 1
            else:
                right = mid - 1

        return None

    # ─── Hash Table tim sinh vien theo ma ───
    def _hash_function(self, key):
        # Tinh hash bang cach cong gia tri ASCII cua tung ky tu
        total = 0
        for char in key:
            total += ord(char)
        return total % HASH_TABLE_SIZE

    def _build_hash_table(self, students):
        # Tao bang bam voi linear probing
        table = [None] * HASH_TABLE_SIZE
        for sv in students:
            index = self._hash_function(sv["student_id"])
            # Linear probing: neu vi tri da co nguoi thi tim vi tri tiep theo
            while table[index] is not None:
                index = (index + 1) % HASH_TABLE_SIZE
            table[index] = sv
        return table

    def _hash_lookup(self, table, student_id):
        # Tim kiem trong bang bam
        index = self._hash_function(student_id)
        start = index
        while table[index] is not None:
            if table[index]["student_id"] == student_id:
                return table[index]
            index = (index + 1) % HASH_TABLE_SIZE
            if index == start:
                break  # Da duyet het bang
        return None

    def hash_search_student(self, student_id):
        students = self.sm.get_all_students()
        if len(students) == 0:
            return None
        table = self._build_hash_table(students)
        return self._hash_lookup(table, student_id)

    # ─── Loc phong theo nhieu tieu chi ───
    def filter_rooms(self, criteria):
        # criteria la dict, vi du:
        # {"available": True}          -> loc phong con cho
        # {"gender": "Nam"}            -> loc phong nam
        # {"room_type": "Dich vu"}     -> loc phong dich vu
        results = []
        for room in self.rm.get_all_rooms():
            is_valid = True

            # Loc phong con cho trong
            if "available" in criteria:
                if criteria["available"] and room.get("available_beds", 0) <= 0:
                    is_valid = False
                if not criteria["available"] and room.get("available_beds", 0) > 0:
                    is_valid = False

            # Loc theo gioi tinh
            if "gender" in criteria:
                if room.get("gender") != criteria["gender"]:
                    is_valid = False

            # Loc theo loai phong
            if "room_type" in criteria:
                if room.get("room_type") != criteria["room_type"]:
                    is_valid = False

            # Loc theo toa nha
            if "building" in criteria:
                if room.get("building") != criteria["building"]:
                    is_valid = False

            if is_valid:
                results.append(room)

        return results