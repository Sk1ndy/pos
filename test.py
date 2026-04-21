import serial
import time

# Remplace par le port trouvé (souvent /dev/ttyUSB0)
PORT = "/dev/ttyUSB0" 

def test_drawer():
    print(f"Tentative d'ouverture sur {PORT}...")
    try:
        # Configuration standard pour les adaptateurs Prolific
        ser = serial.Serial(
            port=PORT,
            baudrate=9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        
        # Test de plusieurs signaux courants pour les tiroirs USB
        print("Envoi du signal \x01...")
        ser.write(b'\x01')
        time.sleep(0.5)
        
        print("Envoi du signal 'open'...")
        ser.write(b'open')
        
        ser.close()
        print("Fin du test.")
    except Exception as e:
        print(f"Erreur : {e}")
        print("Astuce : Essaie de lancer le script avec 'sudo python debug_drawer.py'")

if __name__ == "__main__":
    test_drawer()