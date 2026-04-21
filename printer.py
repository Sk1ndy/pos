import serial
from escpos.printer import Usb
from config import PRINTER_CONFIG, DRAWER_PORT

class Printer:
    def __init__(self):
        try:
            self.device = Usb(PRINTER_CONFIG["vendor_id"], PRINTER_CONFIG["product_id"])
        except:
            self.device = None

    def print_barcode(self, name, code):
        if not self.device: return
        
        self.device.set(align="center")
        self.device.text(f"{name}\n")
        try:
            self.device.barcode(str(code).strip(), 'CODE39', height=64, width=2, pos='BELOW', align_ct=True)
        except:
            self.device.text(f"\n{code}\n")
        self.device.text("\n")
        self.device.cut()

    def print_ticket(self, cart, total_ht, taxes, total_ttc):
        """Imprime le ticket avec les 4 arguments."""
        if not self.device: return

        # Entête
        self.device.text("--- RECU DE VENTE ---\n\n")
        
        # Articles
        self.device.set(align="left")
        for item in cart:
            nom = str(item[0])[:20]
            prix = float(item[1])
            self.device.text(f"{nom:<22}{prix:>7.2f} $\n")
        
        # Totaux
        self.device.text("--------------------------------\n")
        self.device.text(f"Prix normal : {(total_ht)} $\n")
        self.device.text(f"Taxes (15%) : {(taxes)} $\n")
        self.device.text(f"\nTOTAL : {(total_ttc)} $\n\n")

        # Fin
        self.device.text("Merci !\n\n\n")
        self.device.cut()
        
        # Le tiroir s'ouvre a la fin
        ser = serial.Serial(DRAWER_PORT, 9600, timeout=1)
        ser.write(b'\x01')
        ser.close()
