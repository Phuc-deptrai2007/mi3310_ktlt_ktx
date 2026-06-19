# display_service.py — Tach phan hien thi UI ra rieng


def show_students(students):
    if len(students) == 0:
        print("Danh sach sinh vien trong!")
        return
    print("\n" + "=" * 65)
    print(f"{'Ma SV':<10} {'Ho ten':<25} {'SDT':<13} {'Phong':<8}")
    print("-" * 65)
    for sv in students:
        print(f"{sv.get('student_id',''):<10} {sv.get('name',''):<25} "
              f"{sv.get('phone',''):<13} {sv.get('room_number','Chua xep'):<8}")
    print("=" * 65)
    print(f"Tong: {len(students)} sinh vien\n")


def show_student_info(sv):
    print("\n--- Tim thay sinh vien ---")
    print(f"Ma SV  : {sv.get('student_id', '')}")
    print(f"Ho ten : {sv.get('name', '')}")
    print(f"SDT    : {sv.get('phone', '')}")
    print(f"Phong  : {sv.get('room_number', 'Chua xep')}")


def show_rooms(rooms):
    if len(rooms) == 0:
        print("Danh sach phong trong!")
        return
    print("\n" + "=" * 72)
    print(f"{'Phong':<8} {'Toa':<6} {'Loai':<10} {'GT':<6} "
          f"{'Max GD':<8} {'Dang o':<8} {'Con trong':<10}")
    print("-" * 72)
    for p in rooms:
        print(f"{p.get('room_number',''):<8} {p.get('building',''):<6} "
              f"{p.get('room_type',''):<10} {p.get('gender',''):<6} "
              f"{p.get('max_beds',0):<8} "
              f"{len(p.get('current_students',[])):<8} "
              f"{p.get('available_beds',0):<10}")
    print("=" * 72)
    print(f"Tong: {len(rooms)} phong\n")


def show_invoice(invoice):
    print(f"\n--- Hoa don {invoice['invoice_id']} ---")
    print(f"So phong   : {invoice['room_number']}")
    print(f"Thang/Nam  : {invoice['month']}/{invoice['year']}")
    print(f"Tien phong : {invoice['room_price']:,} dong")
    print(f"Tien dien  : {invoice['electricity_used']} kWh x "
          f"{invoice['electricity_price_per_unit']:,} = "
          f"{invoice['total_electricity']:,} dong")
    print(f"Tien nuoc  : {invoice['water_used']} m3 x "
          f"{invoice['water_price_per_unit']:,} = "
          f"{invoice['total_water']:,} dong")
    print("-" * 40)
    print(f"Tong cong  : {invoice['total_amount']:,} dong")
    print(f"Trang thai : {invoice['payment_status']}")


def show_invoice_list(invoices, room_number, month, year):
    if len(invoices) == 0:
        print(f"Khong co hoa don nao cho phong {room_number} "
              f"thang {month}/{year}")
        return
    print(f"\n--- Lich su hoa don phong {room_number} thang {month}/{year} ---")
    for hd in invoices:
        print(f"Ma HD: {hd['invoice_id']} | "
              f"Tong: {hd['total_amount']:,} dong | "
              f"Trang thai: {hd['payment_status']}")


def show_facilities(facilities, room_number):
    if len(facilities) == 0:
        print(f"Khong co thiet bi nao trong phong {room_number}")
        return
    print(f"\n--- Thiet bi phong {room_number} ---")
    print(f"{'Ma TB':<8} {'Ten thiet bi':<20} {'Hang':<15} {'Trang thai'}")
    print("-" * 60)
    for tb in facilities:
        print(f"{tb['facility_id']:<8} {tb['facility_name']:<20} "
              f"{tb.get('brand',''):<15} {tb['status']}")


def show_filter_results(rooms):
    if len(rooms) == 0:
        print("Khong tim thay phong nao phu hop!")
        return
    print(f"\n--- Ket qua loc ({len(rooms)} phong) ---")
    print(f"{'Phong':<8} {'Loai':<10} {'GT':<6} {'Con trong':<10}")
    print("-" * 38)
    for p in rooms:
        print(f"{p.get('room_number',''):<8} {p.get('room_type',''):<10} "
              f"{p.get('gender',''):<6} {p.get('available_beds',0):<10}")


def show_occupancy(total_beds, occupied, empty, rate):
    print("\n--- Ti le lap day KTX ---")
    print(f"Tong so giuong  : {total_beds}")
    print(f"Dang co nguoi   : {occupied}")
    print(f"Con trong       : {empty}")
    print(f"Ti le lap day   : {rate:.1f}%")


def show_revenue(month, year, num_invoices, total_revenue, paid, unpaid):
    if num_invoices == 0:
        print(f"Khong co hoa don nao trong thang {month}/{year}")
        return
    print(f"\n--- Doanh thu thang {month}/{year} ---")
    print(f"So hoa don phat sinh    : {num_invoices}")
    print(f"Tong doanh thu du kien  : {total_revenue:,} dong")
    print(f"So tien da thu          : {paid:,} dong")
    print(f"So tien chua thu (no)   : {unpaid:,} dong")
