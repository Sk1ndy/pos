import serial
import random
from config import TPS_RATE, TVQ_RATE
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
        facture_id = random.randint(1000, 9999)
        
        """Imprime le ticket avec les 4 arguments."""
        if not self.device: return

        # Entête
        self.device.text("--- RECU DE VENTE ---\n\n")
        self.device.text(f"Facture n° : {facture_id}\n\n")
        
        # Articles
        self.device.set(align="left")
        for item in cart:
            nom = str(item[0])[:20]
            prix = float(item[1])
            self.device.text(f"{nom:<22}{prix:>7.2f} $\n")
        
        # Totaux
        self.device.text("--------------------------------\n")
        self.device.text(f"Sous Total : {(total_ht):.2f} $\n")
        self.device.text(f"Taxes TPS (0.05%) : {(total_ht * TPS_RATE):.2f} $\n")
        self.device.text(f"Taxes TVQ (0.09975%) : {(total_ht * TVQ_RATE):.2f} $\n")
        self.device.text(f"\nTOTAL : {(total_ttc):.2f} $\n\n")

        # Fin
        self.device.text("Merci !\n\n\n")
        self.device.cut()
        
        # Le tiroir s'ouvre a la fin
        ser = serial.Serial(DRAWER_PORT, 9600, timeout=1)
        ser.write(b'\x01')
        ser.close()
        self.open_drawer() 
