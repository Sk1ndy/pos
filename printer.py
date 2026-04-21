from escpos.printer import Usb
from config import PRINTER_CONFIG

class Printer:
    def __init__(self):
        try:
            self.device = Usb(
                PRINTER_CONFIG["vendor_id"],
                PRINTER_CONFIG["product_id"]
            )
        except:
            self.device = None

    def is_ready(self):
        return self.device is not None

    def print_barcode(self, name, code):
        if not self.device:
            return

        code = str(code).encode('ascii', 'ignore').decode()

        self.device.set(align="center")
        self.device.text(f"{name}\n\n")

        self.device._raw(b'\x1d\x6b\x49' + bytes([len(code)]) + code.encode())

        self.device.text("\n")
        self.device.cut()

    def print_ticket(self, cart, total):
        if not self.device:
            return

        self.device.set(align="center")
        self.device.text("TICKET\n\n")

        for item in cart:
            self.device.text(f"{item[0]} : {item[1]:.2f}\n")

        self.device.text(f"\nTOTAL: {total:.2f}\n")
        self.device.cut()