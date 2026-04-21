# Test POS Python (Scanner + Imprimante + Caisse)

## Matériel
- Imprimante: Epson TM-T88IV
- Scanner: CT650 / HK Systems (mode clavier USB)
- Caisse: connectée à l’imprimante

---

## 1. Installer Python
Python 3 recommandé

---

## 2. Installer dépendance
```bash
pip install python-escpos
```

---

## 3. Trouver les IDs USB (IMPORTANT)

### Linux / Mac:
```bash
lsusb
```

Cherche une ligne comme:
```
04b8:0202 Seiko Epson
```

- 04b8 = Vendor ID
- 0202 = Product ID

Remplace dans le code:
```python
VENDOR_ID = 0x04b8
PRODUCT_ID = 0x0202
```

---

### Windows:
- Installer driver Epson (recommandé)
- Sinon utiliser Zadig pour driver USB

---

## 4. Tester le scanner
- Ouvre un bloc-notes
- Scan un code-barres
- Si ça écrit → OK

---

## 5. Lancer le programme
```bash
python test_pos.py
```

---

## 6. Utilisation
- Scanner un code → il s’affiche
- Le ticket s’imprime
- La caisse s’ouvre

---

##  Problèmes possibles

### Imprimante non détectée
- Mauvais Vendor/Product ID
- Driver non installé (Windows)
- Permissions USB (Linux → sudo)

---

### Scanner ne fonctionne pas
- Vérifier mode HID (clavier)
- Tester dans un bloc-notes

---

### Caisse ne s’ouvre pas
- Vérifier branchement RJ11 dans imprimante
- Tester commande brute (déjà incluse)

---

##  Résultat attendu
- Scan → affichage
- Impression ticket
- Ouverture caisse

---

## Bonus
Tu peux modifier:
- texte du ticket
- prix
- boucle de scan

---
