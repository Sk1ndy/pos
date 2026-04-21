import serial
from escpos.printer import Usb
from datetime import datetime
from config import PRINTER_CONFIG, DRAWER_CONFIG

class Printer:
    def __init__(self):
        try:
            self.device = Usb(PRINTER_CONFIG["vendor_id"], PRINTER_CONFIG["product_id"])
        except:
            self.device = None
        self.drawer_config = DRAWER_CONFIG

    def open_drawer(self):
        try:
            ser = serial.Serial(port=self.drawer_config["port"], 
                                baudrate=self.drawer_config["baudrate"], 
                                timeout=1)
            ser.write(b'\x01')
            ser.close()
        except Exception as e:
            print(f"Erreur tiroir : {e}")

    def print_ticket(self, cart, total_ht, taxes, total_ttc):
        if not self.device: return

        # --- Impression ---
        self.device.set(align="center")
        self.device.text("RECU DE VENTE\n")
        self.device.text("-" * 32 + "\n")

        self.device.set(align="left")
        for item in cart:
            nom = str(item[0])[:20].ljust(22)
            prix = f"{float(item[1]):.2f} $"
            self.device.text(f"{nom}{prix:>10}\n")

        self.device.text("-" * 32 + "\n")
        
        self.device.set(align="right")
        self.device.text(f"Sous-total : {total_ht:.2f} $\n")
        self.device.text(f"Taxes (15%) : {taxes:.2f} $\n")
        
        self.device.set(align="center", bold=True)
        self.device.text(f"\nTOTAL A PAYER : {total_ttc:.2f} $\n\n")
        self.device.set(bold=False)

        self.device.text("Merci de votre visite !\n\n\n")
        self.device.cut()
        
        # Ouverture du tiroir après l'impression
        self.open_drawer()