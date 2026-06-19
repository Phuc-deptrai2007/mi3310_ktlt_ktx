class ReportService:
    def __init__(self, room_manager, invoice_manager):
        self.rm = room_manager
        self.im = invoice_manager

    def get_occupancy_rate(self):
        rooms = self.rm.get_all_rooms()
        if len(rooms) == 0:
            return None

        total_beds = 0
        occupied   = 0

        for room in rooms:
            total_beds += room.get("max_beds", 0)
            occupied   += len(room.get("current_students", []))

        empty = total_beds - occupied
        rate  = (occupied / total_beds) * 100 if total_beds > 0 else 0

        return {
            "total_beds": total_beds,
            "occupied"  : occupied,
            "empty"     : empty,
            "rate"      : rate
        }

    def revenue_statistics(self, month, year):
        invoices = self.im.get_all_invoices()

        total_revenue = 0
        total_paid    = 0
        total_unpaid  = 0
        num_invoices  = 0

        for inv in invoices:
            if inv["month"] == month and inv["year"] == year:
                num_invoices  += 1
                total_revenue += inv.get("total_amount", 0)
                if inv.get("payment_status") == "Da thanh toan":
                    total_paid += inv.get("total_amount", 0)
                else:
                    total_unpaid += inv.get("total_amount", 0)

        return {
            "month"        : month,
            "year"         : year,
            "num_invoices" : num_invoices,
            "total_revenue": total_revenue,
            "paid"         : total_paid,
            "unpaid"       : total_unpaid
        }