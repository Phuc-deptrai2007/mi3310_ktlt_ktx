from student_manager import StudentManager
from room_manager import RoomManager
from invoice_manager import InvoiceManager
from facility_manager import FacilityManager
from search_service import SearchService
from report_service import ReportService
import display_service as ui

# Khoi tao tat ca cac module
sm     = StudentManager()
rm     = RoomManager()
im     = InvoiceManager()
fm     = FacilityManager()
search = SearchService(sm, rm)
report = ReportService(rm, im)


def save_all():
    sm.save_data()
    rm.save_data()
    im.save_data()
    fm.save_data()
    print("Da luu du lieu xuong file JSON.")


# ─── MENU CON ────────────────────────────────

def menu_student():
    while True:
        print("\n=== QUAN LY SINH VIEN ===")
        print("1. Xem danh sach sinh vien")
        print("2. Them sinh vien moi")
        print("3. Cap nhat thong tin sinh vien")
        print("4. Xoa sinh vien")
        print("5. Sap xep theo ten (Merge Sort)")
        print("6. Sap xep theo ma SV (QuickSort)")
        print("0. Quay lai")
        choice = input("Chon: ").strip()

        if choice == "1":
            ui.show_students(sm.get_all_students())

        elif choice == "2":
            sid = input("Ma SV: ").strip()
            if not sid:
                print("Ma SV khong duoc de trong!")
                continue
                
            if sm.get_student_by_id(sid) is not None:
                print("Ma sinh vien da ton tai!")
                continue
                
            name = input("Ho ten: ").strip()
            if not name:
                print("Ho ten khong duoc de trong!")
                continue
            phone = input("SDT: ").strip()
            
            data  = {"student_id": sid, "name": name, "phone": phone}
            sm.add_student(data)
            print(f"Da them sinh vien: {name} (Vui long sang menu Quan ly Phong de xep phong)")

        elif choice == "3":
            sid = input("Ma SV can cap nhat: ").strip()
            if not sid:
                print("Ma SV khong duoc de trong!")
                continue
            print("Nhap thong tin moi (Enter de bo qua):")
            name  = input("Ho ten moi: ").strip()
            phone = input("SDT moi: ").strip()
            new_data = {}
            if name:  new_data["name"]  = name
            if phone: new_data["phone"] = phone
            if new_data:
                if sm.update_student(sid, new_data):
                    print(f"Cap nhat thanh cong sinh vien {sid}")
                else:
                    print("Khong tim thay sinh vien!")
            else:
                print("Khong co gi de cap nhat.")

        elif choice == "4":
            sid = input("Ma SV can xoa: ").strip()
            if not sid:
                print("Ma SV khong duoc de trong!")
                continue
            
            # Lay thong tin sv de biet co dang o phong nao khong
            student = sm.get_student_by_id(sid)
            if not student:
                print("Khong tim thay sinh vien!")
                continue

            room_number = student.get("room_number")
            
            if sm.delete_student(sid):
                # Neu sv dang o trong phong thi xoa khoi phong do
                if room_number:
                    rm.remove_student(sid, room_number)
                print(f"Da xoa sinh vien {sid} khoi he thong.")
            else:
                print("Khong tim thay sinh vien!")

        elif choice == "5":
            sm.sort_by_name()
            print("Da sap xep theo ten (Merge Sort)")
            ui.show_students(sm.get_all_students())

        elif choice == "6":
            sm.sort_by_id()
            print("Da sap xep theo ma SV (QuickSort)")
            ui.show_students(sm.get_all_students())

        elif choice == "0":
            break
        else:
            print("Lua chon khong hop le!")


def menu_room():
    while True:
        print("\n=== QUAN LY PHONG ===")
        print("1. Xem trang thai phong")
        print("2. Xep phong cho sinh vien")
        print("3. Chuyen phong sinh vien")
        print("4. Them phong moi")
        print("0. Quay lai")
        choice = input("Chon: ").strip()

        if choice == "1":
            ui.show_rooms(rm.get_all_rooms())

        elif choice == "2":
            student_id  = input("Ma SV: ").strip()
            room_number = input("So phong: ").strip()
            gender      = input("Gioi tinh SV (Nam/Nu): ").strip()
            if not student_id or not room_number or not gender:
                print("Vui long nhap day du thong tin!")
                continue
            if rm.assign_room(student_id, room_number, gender):
                sm.update_student(student_id, {"room_number": room_number})

        elif choice == "3":
            student_id = input("Ma SV: ").strip()
            old_room   = input("Phong cu: ").strip()
            new_room   = input("Phong moi: ").strip()
            gender     = input("Gioi tinh SV (Nam/Nu): ").strip()
            if not student_id or not old_room or not new_room or not gender:
                print("Vui long nhap day du thong tin!")
                continue
            if rm.transfer_room(student_id, old_room, new_room, gender):
                sm.update_student(student_id, {"room_number": new_room})

        elif choice == "4":
            room_number = input("Ma phong (vd: P201): ").strip()
            if not room_number:
                print("Ma phong khong duoc de trong!")
                continue
                
            if rm.get_room_by_number(room_number) is not None:
                print("Ma phong da ton tai tren he thong!")
                continue
                
            gender = input("Gioi tinh phong (Nam/Nu): ").strip()
            room_type = input("Loai phong (Thuong/Dich vu): ").strip()
            try:
                max_beds = int(input("So giuong toi da: "))
                price = float(input("Gia phong: "))
            except ValueError:
                print("Gia tri khong hop le!")
                continue
                
            new_room = {
                "room_number": room_number,
                "gender": gender,
                "room_type": room_type,
                "building": room_number[0] if room_number else "",
                "max_beds": max_beds,
                "available_beds": max_beds,
                "room_price": price,
                "current_students": []
            }
            rm.add_room(new_room)
            print(f"Them phong {room_number} thanh cong!")

        elif choice == "0":
            break
        else:
            print("Lua chon khong hop le!")


def menu_invoice():
    while True:
        print("\n=== QUAN LY HOA DON ===")
        print("1. Lap hoa don thang")
        print("2. Cap nhat trang thai thanh toan")
        print("3. Tra cuu hoa don theo phong/thang/nam")
        print("0. Quay lai")
        choice = input("Chon: ").strip()

        if choice == "1":
            room_number = input("So phong: ").strip()
            room = rm.get_room_by_number(room_number)
            if room is None:
                print("Khong tim thay phong!")
                continue
            try:
                elec_old = float(input("Chi so dien cu (kWh): "))
                elec_new = float(input("Chi so dien moi (kWh): "))
                water_old = float(input("Chi so nuoc cu (m3): "))
                water_new = float(input("Chi so nuoc moi (m3): "))
                
                if elec_new < elec_old or water_new < water_old:
                    print("Chi so moi khong duoc nho hon chi so cu!")
                    continue
                
                electricity = elec_new - elec_old
                water = water_new - water_old
            except ValueError:
                print("Gia tri khong hop le!")
                continue
            invoice = im.calculate_monthly_invoice(
                room_number, electricity, water, room["room_price"])
            ui.show_invoice(invoice)

        elif choice == "2":
            invoice_id = input("Ma hoa don: ").strip()
            if not invoice_id:
                print("Ma hoa don khong duoc de trong!")
                continue
            
            pos = im.find_invoice(invoice_id)
            if pos == -1:
                print(f"Khong tim thay hoa don {invoice_id}!")
                continue
                
            invoice = im.invoices[pos]
            if invoice["payment_status"] == "Da thanh toan":
                print("Hoa don nay da duoc thanh toan truoc do.")
                continue
                
            print(f"Tong so tien can thanh toan: {invoice['total_amount']:,.0f} VND")
            print("1. Thanh toan hoa don")
            print("2. Huy")
            sub = input("Chon: ").strip()
            if sub == "1":
                try:
                    amount_paid = float(input("Nhap so tien khach thanh toan: "))
                except ValueError:
                    print("Chi chap nhan so!")
                    continue
                    
                if amount_paid < invoice["total_amount"]:
                    print("So tien thanh toan chua du!")
                    continue
                    
                im.update_payment_status(invoice_id, "Da thanh toan")
                print(f"Da cap nhat hoa don {invoice_id}: Da thanh toan")
            elif sub == "2":
                continue
            else:
                print("Lua chon khong hop le!")

        elif choice == "3":
            room_number = input("So phong: ").strip()
            try:
                month = int(input("Thang: "))
                year  = int(input("Nam: "))
            except ValueError:
                print("Gia tri khong hop le!")
                continue
            results = im.get_invoice_history(room_number, month, year)
            ui.show_invoice_list(results, room_number, month, year)

        elif choice == "0":
            break
        else:
            print("Lua chon khong hop le!")


def menu_facility():
    while True:
        print("\n=== CO SO VAT CHAT ===")
        print("1. Xem thiet bi theo phong")
        print("2. Bao hong thiet bi")
        print("3. Cap nhat trang thai sua chua")
        print("4. Them thiet bi moi")
        print("0. Quay lai")
        choice = input("Chon: ").strip()

        if choice == "1":
            room_number = input("So phong: ").strip()
            results = fm.get_facilities_by_room(room_number)
            ui.show_facilities(results, room_number)

        elif choice == "2":
            room_number   = input("So phong: ").strip()
            facility_name = input("Ten thiet bi: ").strip()
            description   = input("Mo ta tinh trang hong: ").strip()
            reported_by   = input("Ma SV bao hong: ").strip()
            if not room_number or not facility_name or not description:
                print("Vui long nhap day du thong tin!")
                continue
            if fm.report_damage(room_number, facility_name, description, reported_by):
                print(f"Da ghi nhan bao hong: {facility_name} phong {room_number}")

        elif choice == "3":
            facility_id = input("Ma thiet bi: ").strip()
            if not facility_id:
                print("Ma thiet bi khong duoc de trong!")
                continue
            print("1. Da sua xong")
            print("2. Dang cho")
            sub = input("Chon: ").strip()
            if sub == "1":
                status = "Da sua xong"
            elif sub == "2":
                status = "Dang cho"
            else:
                print("Lua chon khong hop le!")
                continue
            if fm.update_repair_status(facility_id, status):
                print(f"Da cap nhat thiet bi {facility_id}: {status}")
            else:
                print(f"Khong tim thay thiet bi {facility_id}!")

        elif choice == "4":
            facility_id = input("Ma thiet bi (vd: TB001): ").strip()
            if not facility_id:
                print("Ma thiet bi khong duoc de trong!")
                continue
                
            if fm.find_facility(facility_id) != -1:
                print("Ma thiet bi da ton tai tren he thong!")
                continue
                
            room_number = input("So phong: ").strip()
            facility_name = input("Ten thiet bi: ").strip()
            if not room_number or not facility_name:
                print("Vui long nhap day du thong tin!")
                continue
            
            new_facility = {
                "facility_id": facility_id,
                "room_number": room_number,
                "facility_name": facility_name,
                "brand": "Chua ro",
                "install_date": "Chua ro",
                "status": "Dang hoat dong",
                "repair_history": []
            }
            
            res = fm.add_facility_manual(new_facility)
            if res == True:
                print(f"Da them thiet bi {facility_id} thanh cong!")
            elif res == -1:
                print("Thiet bi da ton tai trong phong!")

        elif choice == "0":
            break
        else:
            print("Lua chon khong hop le!")


def menu_search():
    while True:
        print("\n=== TIM KIEM & TRA CUU ===")
        print("1. Tim sinh vien theo ma (Binary Search)")
        print("2. Tim sinh vien theo ma (Hash Table)")
        print("3. Loc phong theo tieu chi")
        print("0. Quay lai")
        choice = input("Chon: ").strip()

        if choice == "1":
            student_id = input("Nhap ma SV can tim: ").strip()
            if not student_id:
                print("Ma SV khong duoc de trong!")
                continue
            result = search.binary_search_student(student_id)
            if result:
                ui.show_student_info(result)
            else:
                print(f"Khong tim thay sinh vien co ma {student_id}")

        elif choice == "2":
            student_id = input("Nhap ma SV can tim: ").strip()
            if not student_id:
                print("Ma SV khong duoc de trong!")
                continue
            result = search.hash_search_student(student_id)
            if result:
                print("(Tim bang Hash Table)")
                ui.show_student_info(result)
            else:
                print(f"Khong tim thay sinh vien co ma {student_id}")

        elif choice == "3":
            print("Loc theo (Enter de bo qua):")
            criteria  = {}
            gender    = input("Gioi tinh (Nam/Nu): ").strip()
            room_type = input("Loai phong (Thuong/Dich vu): ").strip()
            available = input("Chi hien phong con cho? (co/khong): ").strip()
            if gender:    criteria["gender"]    = gender
            if room_type: criteria["room_type"] = room_type
            if available == "co": criteria["available"] = True
            results = search.filter_rooms(criteria)
            ui.show_filter_results(results)

        elif choice == "0":
            break
        else:
            print("Lua chon khong hop le!")


def menu_report():
    while True:
        print("\n=== THONG KE & BAO CAO ===")
        print("1. Ti le lap day KTX")
        print("2. Doanh thu theo thang")
        print("0. Quay lai")
        choice = input("Chon: ").strip()

        if choice == "1":
            data = report.get_occupancy_rate()
            if data is None:
                print("Khong co du lieu phong!")
            else:
                ui.show_occupancy(data["total_beds"], data["occupied"],
                                  data["empty"], data["rate"])

        elif choice == "2":
            try:
                month = int(input("Thang: "))
                year  = int(input("Nam: "))
            except ValueError:
                print("Gia tri khong hop le!")
                continue
            data = report.revenue_statistics(month, year)
            ui.show_revenue(month, year, data["num_invoices"],
                            data["total_revenue"], data["paid"], data["unpaid"])

        elif choice == "0":
            break
        else:
            print("Lua chon khong hop le!")


# ─── MENU CHINH ──────────────────────────────

def main():
    print("=" * 45)
    print("   HE THONG QUAN LY KI TUC XA - HUST")
    print("=" * 45)

    while True:
        print("\n=== MENU CHINH ===")
        print("1. Quan ly sinh vien")
        print("2. Quan ly phong o")
        print("3. Quan ly hoa don & dien nuoc")
        print("4. Quan ly co so vat chat")
        print("5. Tim kiem & tra cuu")
        print("6. Thong ke & bao cao")
        print("0. Thoat va luu du lieu")
        choice = input("Chon: ").strip()

        if choice == "1":
            menu_student()
        elif choice == "2":
            menu_room()
        elif choice == "3":
            menu_invoice()
        elif choice == "4":
            menu_facility()
        elif choice == "5":
            menu_search()
        elif choice == "6":
            menu_report()
        elif choice == "0":
            save_all()
            print("Cam on ban da su dung he thong. Tam biet!")
            break
        else:
            print("Lua chon khong hop le!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nChuong trinh bi ngat. Tam biet!")