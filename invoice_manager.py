import os
from utils import read_json, write_json
from datetime import date

FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "invoices.json")

# Don gia mac dinh
ELECTRICITY_PRICE = 3500   # dong/kwh
WATER_PRICE       = 15000  # dong/m3


class InvoiceManager:
    def __init__(self):
        self.invoices = read_json(FILE_PATH)

    def save_data(self):
        write_json(FILE_PATH, self.invoices)

    def find_invoice(self, invoice_id):
        for i in range(len(self.invoices)):
            if self.invoices[i]["invoice_id"] == invoice_id:
                return i
        return -1

    def generate_invoice_id(self):
        # Tu dong tao ma HD001, HD002,...
        if len(self.invoices) == 0:
            return "HD001"
        num = len(self.invoices) + 1
        return f"HD{num:03d}"

    def calculate_monthly_invoice(self, room_number, electricity_used, water_used, room_price):
        # Tinh tien
        electricity_cost = electricity_used * ELECTRICITY_PRICE
        water_cost       = water_used * WATER_PRICE
        total            = room_price + electricity_cost + water_cost

        today = date.today()

        invoice = {
            "invoice_id"              : self.generate_invoice_id(),
            "room_number"             : room_number,
            "month"                   : today.month,
            "year"                    : today.year,
            "room_price"              : room_price,
            "electricity_used"        : electricity_used,
            "electricity_price_per_unit": ELECTRICITY_PRICE,
            "water_used"              : water_used,
            "water_price_per_unit"    : WATER_PRICE,
            "total_electricity"       : electricity_cost,
            "total_water"             : water_cost,
            "total_amount"            : total,
            "payment_status"          : "Chua thanh toan",
            "payment_date"            : None,
            "created_date"            : str(today)
        }

        self.invoices.append(invoice)
        self.save_data()
        return invoice

    def update_payment_status(self, invoice_id, status):
        pos = self.find_invoice(invoice_id)
        if pos == -1:
            return False

        self.invoices[pos]["payment_status"] = status
        # Neu da thanh toan thi ghi ngay thanh toan
        if status == "Da thanh toan":
            self.invoices[pos]["payment_date"] = str(date.today())

        self.save_data()
        return True

    def get_invoice_history(self, room_number, month, year):
        results = []
        for inv in self.invoices:
            if (inv["room_number"] == room_number
                    and inv["month"] == month
                    and inv["year"] == year):
                results.append(inv)
        return results

    def get_all_invoices(self):
        return self.invoices