import sqlite3
import os
import random

db_path = r'C:\Users\onur\Desktop\it_asset_manager\instance\envanter.db'
if not os.path.exists(db_path):
    db_path = r'C:\Users\onur\Desktop\it_asset_manager\envanter.db'

def rand_ip():
    return f"192.168.1.{random.randint(10, 250)}"

def rand_mac():
    return ":".join([f"{random.randint(0, 255):02X}" for _ in range(6)])

def rand_phone_ext():
    return f"Dahili: {random.randint(100, 500)}"

# All users from the 3 images
base_data = [
    # Image 1
    ("Revir", "Masaüstü", "CASPER OEM", "Revir", "SCH"),
    ("Emrah YILMAZ (Satın Alma Uzmanı)", "Laptop", "DELL VOSTRO", "Satın Alma", "SCH"),
    ("Mesut DURSUN (Satın Alma Uzmanı)", "Laptop", "DELL VOSTRO", "Satın Alma", "SCH"),
    ("Duygu ÜNAL (Satın Alma Uzmanı)", "Laptop", "DELL VOSTRO", "Satın Alma", "SCH"),
    ("Ebru ERCAN (Satın Alma Uzmanı)", "Laptop", "DELL VOSTRO", "Satın Alma", "SCH"),
    ("Cansu ALTAN (Satın Alma Uzmanı)", "Laptop", "DELL VOSTRO", "Satın Alma", "SCH"),
    ("Berkay ERZURUM (Satın Alma Uzmanı)", "Laptop", "DELL VOSTRO", "Satın Alma", "SCH"),
    ("Giga Stajyer 1", "Laptop", "LENOVO V14 G4", "Satın Alma", "SCH"),
    ("Emre ESİRCİ (Satış Sorumlusu)", "Laptop", "DELL VOSTRO", "Satış", "SCH"),
    ("Betül KAHYA (Satış Temsilcisi)", "Laptop", "DELL VOSTRO", "Satış", "SCH"),
    ("Buse PALAZ (Satış Mühendisi)", "Laptop", "DELL VOSTRO", "Satış", "SCH"),
    ("Muhammed Mustafa GÜLER (Satış Mühendisi)", "Laptop", "DELL VOSTRO", "Satış", "SCH"),
    ("Defne GÜNEŞ (Depo Sorumlusu)", "Laptop", "DELL VOSTRO", "Sevkiyat", "SCH"),
    ("Miraç GÜREŞİR (Depo Sorumlusu)", "Laptop", "DELL VOSTRO", "Sevkiyat", "SCH"),
    ("Zafer HIDIR (Depo Sorumlusu)", "Laptop", "DELL VOSTRO", "Sevkiyat", "SCH"),
    ("Emin BARAN (Depo Sorumlusu)", "Laptop", "DELL VOSTRO", "Sevkiyat", "SCH"),
    ("Tarık ÇAKMAKÇI (Depo ve Lojistik Operasyon Sorumlusu)", "Laptop", "DELL VOSTRO", "Sevkiyat", "SCH"),
    ("Muhammet Mustafa KILIÇ (Üretim Mühendisi)", "Laptop", "DELL VOSTRO", "Üretim", "SCH"),
    ("Ümit AKIN (Üretim Mühendisi)", "Laptop", "DELL VOSTRO", "Üretim", "SCH"),
    ("Ümit AKIN (Üretim Mühendisi) (Uğur Yemenici)", "Laptop", "DELL VOSTRO", "Üretim", "SCH"),
    ("Giga Üretim 2. Hat", "Laptop", "DELL VOSTRO", "Üretim", "SCH"),
    ("Muhammed İPEK (Üretim Mühendisi)", "Laptop", "DELL VOSTRO", "Üretim", "SCH"),
    ("Mine DAYIOĞLU (Kalite Mühendisi)", "Laptop", "DELL VOSTRO", "Kalite", "SCH"),
    ("Mustafa ÖZDEMİR (Muhasebe Müdürü)", "Laptop", "DELL VOSTRO", "Muhasebe", "SCH"),
    ("Yılmaz ÖLPER (Proje Ve Şantiye Mühendisi)", "Laptop", "LENOVO THINKPAD P15V", "AR-GE", "SCH"),
    ("Naci YILDIZ (Mali Ve İdari İşler Sorumlusu)", "Laptop", "DELL VOSTRO", "İdari İşler", "SCH"),
    ("Cantekin ŞENGÜL (İş Sağlığı Ve Güvenliği Uzmanı (B Sınıfı))", "Laptop", "DELL VOSTRO", "İSG", "SCH"),
    ("Ender ÖZALICI (Kalite Güvence Sorumlusu)", "Laptop", "DELL VOSTRO", "İSG", "SCH"),
    ("Kalite Alanı (Nedim GÜNER)", "Laptop", "DELL VOSTRO", "Kalite", "SCH"),
    ("Nedim GÜNER (Kalite Kontrol Sorumlusu)", "Laptop", "DELL VOSTRO", "Kalite", "SCH"),
    
    # Image 2
    ("Kaan ŞAHİN (Kalite Mühendisi)", "Laptop", "DELL VOSTRO", "Kalite", "ALU"),
    ("Çağatay Şahin ÇİFTÇİ (Kalite Kontrol Mühendisi)", "Laptop", "DELL VOSTRO", "Kalite", "ALU"),
    ("Aslı Sefa ÇEŞME (Kalite Yöneticisi)", "Laptop", "DELL VOSTRO", "Kalite", "ALU"),
    ("Aluform Kalite", "Laptop", "LENOVO Thinkpad", "Kalite", "ALU"),
    ("Ferhat ATAR (Muhasebe Uzmanı)", "Laptop", "DELL VOSTRO", "Muhasebe", "ALU"),
    ("Pınar Belgin YERLİKAYA (Yönetici Asistanı)", "Laptop", "DELL VOSTRO 153510", "Ofis", "ALU"),
    ("Ergün DUMAN (Planlama Sorumlusu)", "Laptop", "DELL VOSTRO", "Planlama", "ALU"),
    ("Aluform Stajyer", "Laptop", "DELL VOSTRO", "Planlama", "ALU"),
    ("Emre AÇAN (Planlama Sorumlusu)", "Laptop", "DELL VOSTRO", "Planlama", "ALU"),
    ("Mustafa Çağrı PAMUK (Planlama Sorumlusu)", "Laptop", "MONSTER ABRA A5", "Planlama", "ALU"),
    ("Uğur KARAYAKA (SATIŞ UZMANI)", "Laptop", "DELL VOSTRO", "Satış", "ALU"),
    ("Anıl GÜMÜŞ (Fabrika Satış Uzmanı)", "Laptop", "DELL VOSTRO", "Satış", "ALU"),
    ("Mert YILDIZ (Üretim Mühendisi)", "Laptop", "DELL VOSTRO", "Üretim", "ALU"),
    ("Mustafa Mert MUTLU (Üretim Mühendisi)", "Laptop", "DELL VOSTRO", "Üretim", "ALU"),
    ("Aluform Üretim", "Laptop", "DELL VOSTRO", "Üretim", "ALU"),
    ("Yaşar Ertuğ GÜNNER (Üretim Mühendisi)", "Laptop", "DELL VOSTRO", "Üretim", "ALU"),
    ("Elif ŞEKER (İdari İşler Uzmanı)", "Laptop", "DELL VOSTRO", "İdari İşler", "ALU"),

    # Image 3
    ("İsmail ÖZTÜRK (Proje Mühendisi)", "Laptop", "MONSTER ABRA A5", "AR-GE", "SCH"),
    ("Muhammed Mustafa UYAR (Yazılım Geliştirme Uzmanı)", "Laptop", "DELL VOSTRO", "Bilgi İşlem", "SCH"),
    ("Eray GÜNNER (Yazılım Destek Uzmanı)", "Laptop", "DELL VOSTRO", "Bilgi İşlem", "SCH"),
    ("Kaan ŞEREFLİOĞLU (Bilgi İşlem Uzmanı)", "Laptop", "LENOVO LOQ", "Bilgi İşlem", "SCH"),
    ("Ön Güvenlik", "Masaüstü", "HP OEM", "Güvenlik", "SCH"),
    ("Nuhfel İN (İdari İşler Uzmanı)", "Laptop", "DELL VOSTRO", "İdari İşler", "SCH"),
    ("Beyzanur DUDAK (İnsan Kaynakları Uzmanı)", "Laptop", "DELL INS 3520", "İnsan Kaynakları", "SCH"),
    ("Selin GÜNHER (İnsan Kaynakları Uzmanı)", "Laptop", "DELL VOSTRO", "İnsan Kaynakları", "SCH"),
    ("Muammer KABAOĞLU (Muhasebe Uzmanı)", "Laptop", "DELL VOSTRO", "İnsan Kaynakları", "SCH"),
    ("Fatma Mürvet KARAOĞLU (İnsan Kaynakları Uzmanı)", "Laptop", "DELL VOSTRO", "İnsan Kaynakları", "SCH"),
    ("Selim SEZGİN (Mali Ve İdari İşler Sorumlusu)", "Laptop", "DELL VOSTRO", "İnsan Kaynakları", "SCH"),
    ("Cihan AKSOY (İSG Uzmanı)", "Laptop", "DELL VOSTRO", "İSG", "SCH"),
    ("Kalite Alanı 17BLN04", "Laptop", "DELL VOSTRO", "Kalite", "SCH"),
    ("Süleyman BAYRAKTAR (Kalite Mühendisi)", "Laptop", "DELL VOSTRO", "Kalite", "SCH"),
    ("Duhan Ferhat ÖZTÜRK (Kalite Mühendisi)", "Laptop", "DELL VOSTRO", "Kalite", "SCH"),
    ("Yağmur ESER (Kalite Mühendisi)", "Laptop", "DELL VOSTRO", "Kalite", "SCH"),
    ("Kalite Alanı F9SDBX3", "Laptop", "DELL VOSTRO", "Kalite", "SCH"),
    ("Elmas BIYIKLI (Kalite Mühendisi)", "Laptop", "DELL VOSTRO", "Kalite", "SCH"),
    ("Tuğcan DEMİRDÖVEN (Kalite Mühendisi)", "Laptop", "DELL VOSTRO", "Kalite", "SCH"),
    ("Oğuzhan GELDİ (Kalite Mühendisi)", "Laptop", "DELL VOSTRO", "Kalite", "SCH"),
    ("Berke BATMAZ (Kalite Mühendisi)", "Laptop", "DELL VOSTRO", "Kalite", "SCH"),
    ("Giga Pvlab", "Laptop", "DELL VOSTRO", "Kalite", "SCH"),
    ("Alihan BOZ (Kalite Mühendisi)", "Laptop", "DELL VOSTRO", "Kalite", "SCH"),
    ("Ladin ASLAN (Kalite Kontrol Sorumlusu)", "Laptop", "LENOVO Thinkbook", "Kalite", "SCH"),
    ("Ahmet Can GENÇ (Muhasebe Uzmanı)", "Laptop", "DELL VOSTRO", "Muhasebe", "SCH"),
    ("Merve BAYRAKTAR (Finans Uzmanı)", "Laptop", "DELL VOSTRO", "Muhasebe", "SCH"),
    ("Fatma CANBULAT (Muhasebe Uzmanı)", "Laptop", "DELL VOSTRO", "Muhasebe", "SCH"),
    ("Şule ÇAKMAK (Muhasebe Uzmanı)", "Laptop", "DELL VOSTRO", "Muhasebe", "SCH"),
    ("Edanur AKDEMİR (Ofis Asistanı)", "Laptop", "DELL VOSTRO", "Ofis", "SCH"),
    ("Nurdagül KIL (Büro Yönetimi ve Yönetici Asistanı)", "Laptop", "DELL VOSTRO", "Ofis", "SCH")
]

records = []
barcode = 101000000

for name, cat, brand, loc, sirket in base_data:
    # 1. Main Computer
    barcode += 1
    ip = rand_ip() if cat in ['Laptop', 'Masaüstü'] else ""
    mac = rand_mac() if cat in ['Laptop', 'Masaüstü'] else ""
    records.append((name, str(barcode), cat, brand, loc, sirket, ip, mac, "Sistem kurulumu tamam."))
    
    # 2. Add a Monitor
    barcode += 1
    records.append((name, str(barcode), "Monitör", random.choice(["DELL 24'' IPS", "ASUS 27''", "ViewSonic 24''"]), loc, sirket, "", "", "24 inç, 144Hz"))
    
    # 3. Add Keyboard/Mouse
    barcode += 1
    records.append((name, str(barcode), "Klavye/Fare", random.choice(["Logitech MK220", "A4 Tech Wireless", "Microsoft Sculpt"]), loc, sirket, "", "", "Kablosuz USB"))

    # 4. Phones for some
    if random.choice([True, False]):
        barcode += 1
        if "Müdür" in name or "Yönetici" in name or "Satış" in name:
            records.append((name, str(barcode), "Cep Telefonu", "Apple iPhone 16", loc, sirket, "", "", f"Tel: 05{random.randint(30, 59)}{random.randint(1000000, 9999999)}"))
        else:
            records.append((name, str(barcode), "Masa Telefonu", "Yealink T21P", loc, sirket, rand_ip(), rand_mac(), rand_phone_ext()))

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute('DELETE FROM cihaz')
conn.commit()

for row in records:
    c.execute('''INSERT INTO cihaz (personel_ad_soyad, barkod_no, kategori, marka_model, lokasyon_ofis, sirket, ip_adresi, mac_adresi, notlar)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', row)

conn.commit()
conn.close()
print("Tüm personeller eklendi!")
