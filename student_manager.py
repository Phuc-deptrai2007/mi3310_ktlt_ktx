import os
from utils import read_json, write_json

FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "students.json")


class StudentManager:
    def __init__(self):
        self.students = read_json(FILE_PATH)

    def save_data(self):
        write_json(FILE_PATH, self.students)

    def find_index(self, student_id):
        for i in range(len(self.students)):
            if self.students[i]["student_id"] == student_id:
                return i
        return -1

    def add_student(self, student_data):
        # Kiem tra trung ma
        if self.find_index(student_data["student_id"]) != -1:
            return False
        self.students.append(student_data)
        return True

    def update_student(self, student_id, new_data):
        pos = self.find_index(student_id)
        if pos == -1:
            return False
        # Khong cho doi ma sv
        if "student_id" in new_data:
            del new_data["student_id"]
        self.students[pos].update(new_data)
        return True

    def delete_student(self, student_id):
        pos = self.find_index(student_id)
        if pos == -1:
            return False
        del self.students[pos]
        return True

    # ─── Merge Sort theo ten (ten cuoi cung - kieu Viet Nam) ───
    def merge_sort_by_name(self, arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        left = self.merge_sort_by_name(arr[:mid])
        right = self.merge_sort_by_name(arr[mid:])
        return self._merge_by_name(left, right)

    def _merge_by_name(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            # So sanh theo ten cuoi cung (phan sau dau cach cuoi)
            name_l = left[i].get("name","").split()[-1].lower() if left[i].get("name") else ""
            name_r = right[j].get("name","").split()[-1].lower() if right[j].get("name") else ""
            if name_l <= name_r:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        # Them phan con lai
        while i < len(left):
            result.append(left[i])
            i += 1
        while j < len(right):
            result.append(right[j])
            j += 1
        return result

    def sort_by_name(self):
        self.students = self.merge_sort_by_name(self.students)

    # ─── QuickSort theo ma SV (phuc vu Binary Search) ───
    def quicksort_by_id(self, arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]["student_id"]
        left   = [x for x in arr if x["student_id"] < pivot]
        middle = [x for x in arr if x["student_id"] == pivot]
        right  = [x for x in arr if x["student_id"] > pivot]
        return self.quicksort_by_id(left) + middle + self.quicksort_by_id(right)

    def sort_by_id(self):
        self.students = self.quicksort_by_id(self.students)

    def get_student_by_id(self, student_id):
        pos = self.find_index(student_id)
        if pos != -1:
            return self.students[pos]
        return None

    def get_all_students(self):
        return self.students
