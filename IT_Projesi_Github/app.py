from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'gizli_anahtar_staj_projesi'
basedir = os.path.abspath(os.path.dirname(__name__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'envanter.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Cihaz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    personel_ad_soyad = db.Column(db.String(100), nullable=False)
    barkod_no = db.Column(db.String(50), unique=True, nullable=False)
    kategori = db.Column(db.String(50), nullable=False)
    marka_model = db.Column(db.String(100), nullable=False)
    lokasyon_ofis = db.Column(db.String(100), nullable=True)
    sirket = db.Column(db.String(50), nullable=True)
    ip_adresi = db.Column(db.String(50), nullable=True)
    mac_adresi = db.Column(db.String(50), nullable=True)
    notlar = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Cihaz {self.barkod_no}>'

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    personeller = db.session.query(
        Cihaz.personel_ad_soyad, 
        Cihaz.sirket, 
        Cihaz.lokasyon_ofis, 
        db.func.count(Cihaz.id).label('cihaz_sayisi')
    ).group_by(Cihaz.personel_ad_soyad, Cihaz.sirket, Cihaz.lokasyon_ofis).all()
    
    toplam_cihaz = sum(p.cihaz_sayisi for p in personeller)
    
    return render_template('index.html', personeller=personeller, toplam_cihaz=toplam_cihaz)

@app.route('/personel/<path:ad_soyad>')
def personel_detay(ad_soyad):
    cihazlar = Cihaz.query.filter_by(personel_ad_soyad=ad_soyad).all()
    if not cihazlar:
        flash('Personel bulunamadı.', 'danger')
        return redirect(url_for('index'))
    sirket = cihazlar[0].sirket
    lokasyon = cihazlar[0].lokasyon_ofis
    return render_template('detay.html', ad_soyad=ad_soyad, cihazlar=cihazlar, sirket=sirket, lokasyon=lokasyon)

@app.route('/ekle', methods=['GET', 'POST'])
def ekle():
    if request.method == 'POST':
        yeni_cihaz = Cihaz(
            personel_ad_soyad=request.form['personel_ad_soyad'],
            barkod_no=request.form['barkod_no'],
            kategori=request.form['kategori'],
            marka_model=request.form['marka_model'],
            lokasyon_ofis=request.form['lokasyon_ofis'],
            sirket=request.form['sirket'],
            ip_adresi=request.form['ip_adresi'],
            mac_adresi=request.form['mac_adresi'],
            notlar=request.form['notlar']
        )
        db.session.add(yeni_cihaz)
        db.session.commit()
        flash('Cihaz başarıyla eklendi!', 'success')
        return redirect(url_for('index'))
    return render_template('ekle.html')

@app.route('/sil/<int:id>')
def sil(id):
    cihaz = Cihaz.query.get_or_404(id)
    db.session.delete(cihaz)
    db.session.commit()
    flash('Cihaz silindi.', 'danger')
    return redirect(url_for('index'))

fake_tickets = [
    {'id': '#TCK-1042', 'kullanici': 'İsmail ÖZTÜRK', 'departman': 'Bilgi İşlem', 'konu': 'Monitör güç kablosu temassızlığı', 'durum': 'Açık', 'oncelik': 'Yüksek', 'tarih': '10.09.2026 09:15'},
    {'id': '#TCK-1041', 'kullanici': 'Kaan ŞEREFLİOĞLU', 'departman': 'Kalite', 'konu': 'AutoCAD lisans yenileme', 'durum': 'İşlemde', 'oncelik': 'Orta', 'tarih': '09.09.2026 14:20'},
    {'id': '#TCK-1040', 'kullanici': 'Ferhat ATAR', 'departman': 'Üretim', 'konu': 'Klavye tuşları basmıyor', 'durum': 'Çözüldü', 'oncelik': 'Düşük', 'tarih': '08.09.2026 11:10'},
    {'id': '#TCK-1039', 'kullanici': 'Tuğba AYDIN', 'departman': 'Muhasebe', 'konu': 'Yazıcıya bağlanamıyorum', 'durum': 'Açık', 'oncelik': 'Yüksek', 'tarih': '10.09.2026 10:05'},
    {'id': '#TCK-1038', 'kullanici': 'Ahmet YILMAZ', 'departman': 'İnsan Kaynakları', 'konu': 'Masaüstü bilgisayar çok yavaş', 'durum': 'İşlemde', 'oncelik': 'Orta', 'tarih': '07.09.2026 16:45'},
    {'id': '#TCK-1037', 'kullanici': 'Merve KAYA', 'departman': 'Pazarlama', 'konu': 'Adobe Photoshop lisans hatası', 'durum': 'Çözüldü', 'oncelik': 'Düşük', 'tarih': '06.09.2026 09:30'},
    {'id': '#TCK-1036', 'kullanici': 'Caner ŞAHİN', 'departman': 'Satış', 'konu': 'VPN bağlantısı kopuyor', 'durum': 'Açık', 'oncelik': 'Yüksek', 'tarih': '05.09.2026 13:15'},
    {'id': '#TCK-1035', 'kullanici': 'Ayşe ÇELİK', 'departman': 'Üretim', 'konu': 'Barkod okuyucu bozuldu', 'durum': 'İşlemde', 'oncelik': 'Yüksek', 'tarih': '04.09.2026 10:20'},
    {'id': '#TCK-1034', 'kullanici': 'Burak DEMİR', 'departman': 'Lojistik', 'konu': 'E-posta şifre sıfırlama', 'durum': 'Çözüldü', 'oncelik': 'Düşük', 'tarih': '03.09.2026 15:00'},
    {'id': '#TCK-1033', 'kullanici': 'Selin YILDIZ', 'departman': 'AR-GE', 'konu': 'Yeni monitör talebi', 'durum': 'İşlemde', 'oncelik': 'Orta', 'tarih': '02.09.2026 11:45'},
    {'id': '#TCK-1032', 'kullanici': 'Gökhan KURT', 'departman': 'Sistem', 'konu': 'Sunucu disk alanı uyarısı', 'durum': 'Çözüldü', 'oncelik': 'Yüksek', 'tarih': '01.09.2026 08:10'},
    {'id': '#TCK-1031', 'kullanici': 'Elif ŞEN', 'departman': 'Muhasebe', 'konu': 'Excel makro güvenlik hatası', 'durum': 'Açık', 'oncelik': 'Orta', 'tarih': '31.08.2026 14:30'}
]

@app.route('/tickets')
def tickets():
    return render_template('tickets.html', tickets=fake_tickets)

from flask import jsonify, request
import random
from datetime import datetime

@app.route('/resolve_ticket/<ticket_id>', methods=['POST'])
def resolve_ticket(ticket_id):
    for t in fake_tickets:
        if t['id'] == ticket_id:
            t['durum'] = 'Çözüldü'
            return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/create_random_ticket', methods=['POST'])
def create_random_ticket():
    k = request.form.get('kullanici')
    d = request.form.get('departman')
    i = request.form.get('konu')
    
    max_id = 1042
    for t in fake_tickets:
        try:
            num = int(t['id'].replace('#TCK-', ''))
            if num > max_id: max_id = num
        except: pass
    
    now = datetime.now().strftime("%d.%m.%Y %H:%M")
    new_t = {
        'id': f"#TCK-{max_id + 1}", 'kullanici': k, 'departman': d, 'konu': i, 
        'durum': 'Açık', 'oncelik': random.choice(['Yüksek', 'Orta', 'Düşük']), 'tarih': now
    }
    fake_tickets.insert(0, new_t)
    return jsonify({'success': True})

fake_lisanslar = [
    {'id': 1, 'yazilim': 'Microsoft Office 365', 'anahtar': 'O365-CORP-***', 'kullanici': 'Tüm Şirket', 'adet': '150', 'kalan': '12', 'bitis': '15.08.2027', 'durum': 'Aktif'},
    {'id': 2, 'yazilim': 'AutoCAD 2024', 'anahtar': 'ACAD-2024-***', 'kullanici': 'AR-GE Departmanı', 'adet': '5', 'kalan': '0', 'bitis': '01.01.2027', 'durum': 'Kritik'},
    {'id': 3, 'yazilim': 'Kaspersky Endpoint Security', 'anahtar': 'KASP-ENT-***', 'kullanici': 'Tüm Şirket', 'adet': '200', 'kalan': '45', 'bitis': '10.11.2028', 'durum': 'Aktif'},
    {'id': 4, 'yazilim': 'Adobe Creative Cloud', 'anahtar': 'ADOB-CC-***', 'kullanici': 'Pazarlama', 'adet': '2', 'kalan': '1', 'bitis': '20.09.2026', 'durum': 'Süresi Yaklaşıyor'},
    {'id': 5, 'yazilim': 'Windows 11 Pro', 'anahtar': 'WIN11-PRO-***', 'kullanici': 'Tüm Şirket', 'adet': '100', 'kalan': '25', 'bitis': 'Süresiz', 'durum': 'Aktif'},
    {'id': 6, 'yazilim': 'SolidWorks 2023', 'anahtar': 'SLDW-2023-***', 'kullanici': 'Tasarım', 'adet': '3', 'kalan': '0', 'bitis': '15.05.2027', 'durum': 'Kritik'},
    {'id': 7, 'yazilim': 'JetBrains PyCharm', 'anahtar': 'JB-PYCH-***', 'kullanici': 'Yazılım', 'adet': '10', 'kalan': '8', 'bitis': '01.12.2026', 'durum': 'Aktif'},
    {'id': 8, 'yazilim': 'FortiClient VPN', 'anahtar': 'FRTI-VPN-***', 'kullanici': 'Uzaktan Çalışanlar', 'adet': '50', 'kalan': '15', 'bitis': '30.10.2027', 'durum': 'Aktif'},
    {'id': 9, 'yazilim': 'VMware Workstation', 'anahtar': 'VMW-WRK-***', 'kullanici': 'Sistem Yönetimi', 'adet': '5', 'kalan': '2', 'bitis': '22.04.2026', 'durum': 'Süresi Yaklaşıyor'},
    {'id': 10, 'yazilim': 'Zoom Pro', 'anahtar': 'ZOOM-PRO-***', 'kullanici': 'Yönetim', 'adet': '20', 'kalan': '5', 'bitis': '10.01.2027', 'durum': 'Aktif'},
    {'id': 11, 'yazilim': 'Slack Enterprise', 'anahtar': 'SLCK-ENT-***', 'kullanici': 'Tüm Şirket', 'adet': '150', 'kalan': '10', 'bitis': '05.08.2028', 'durum': 'Aktif'}
]

@app.route('/lisanslar')
def lisanslar():
    return render_template('lisanslar.html', lisanslar=fake_lisanslar)

@app.route('/add_license', methods=['POST'])
def add_license():
    yazilim = request.form.get('yazilim')
    anahtar = request.form.get('anahtar')
    adet = request.form.get('adet')
    new_id = len(fake_lisanslar) + 1
    fake_lisanslar.insert(0, {
        'id': new_id, 'yazilim': yazilim, 'anahtar': anahtar, 'kullanici': 'Atanmadı', 
        'adet': adet, 'kalan': adet, 'bitis': 'Süresiz', 'durum': 'Aktif'
    })
    return jsonify({'success': True})

# --- GLOBAL FAKE DATA ---
import random
isimler = ["Ali", "Mehmet", "Fatma", "Zeynep", "Mustafa", "Elif", "Emre", "Esra", "Burak", "Hasan", "Cansu", "Hüseyin", "Büşra", "Can", "Gamze", "Volkan", "Gizem", "Oğuz", "Selin"]
soyisimler = ["YILMAZ", "KAYA", "DEMİR", "ÇELİK", "ŞAHİN", "YILDIZ", "AYDIN", "ÖZDEMİR", "ARSLAN", "DOĞAN", "KILIÇ", "ÇETİN", "KARA", "KOÇ", "ÖZKAN", "ŞİMŞEK", "POLAT"]
departmanlar = ["Üretim", "Kalite", "Lojistik", "Satış", "Pazarlama", "Ar-Ge", "Muhasebe", "İnsan Kaynakları"]

fake_personel = [
    {'id': 101, 'isim': 'İsmail ÖZTÜRK', 'departman': 'Bilgi İşlem', 'unvan': 'IT Yöneticisi', 'cihaz_sayisi': 3, 'durum': 'Aktif', 'mail': 'iozturk@schmid.com.tr'},
    {'id': 102, 'isim': 'Ahmet YILMAZ', 'departman': 'İnsan Kaynakları', 'unvan': 'İK Uzmanı', 'cihaz_sayisi': 1, 'durum': 'Aktif', 'mail': 'ayilmaz@schmid.com.tr'},
    {'id': 103, 'isim': 'Kaan ŞEREFLİOĞLU', 'departman': 'Kalite', 'unvan': 'Kalite Mühendisi', 'cihaz_sayisi': 2, 'durum': 'Aktif', 'mail': 'kseref@schmid.com.tr'},
    {'id': 104, 'isim': 'Merve KAYA', 'departman': 'Pazarlama', 'unvan': 'Pazarlama Uzmanı', 'cihaz_sayisi': 1, 'durum': 'İzinde', 'mail': 'mkaya@schmid.com.tr'},
    {'id': 105, 'isim': 'Ferhat ATAR', 'departman': 'Üretim', 'unvan': 'Vardiya Amiri', 'cihaz_sayisi': 1, 'durum': 'Aktif', 'mail': 'fatar@schmid.com.tr'},
    {'id': 106, 'isim': 'Tuğba AYDIN', 'departman': 'Muhasebe', 'unvan': 'Muhasebe Uzmanı', 'cihaz_sayisi': 2, 'durum': 'Aktif', 'mail': 'taydin@schmid.com.tr'}
]
for i in range(45):
    ad = random.choice(isimler)
    soyad = random.choice(soyisimler)
    mail = f"{ad.lower()}.{soyad.lower()}@schmid.com.tr".replace('ş','s').replace('ç','c').replace('ğ','g').replace('ü','u').replace('ö','o').replace('ı','i')
    fake_personel.append({
        'id': 107 + i, 'isim': f"{ad} {soyad}", 'departman': random.choice(departmanlar),
        'unvan': 'Personel', 'cihaz_sayisi': random.randint(0, 3), 'durum': random.choice(['Aktif', 'Aktif', 'Aktif', 'Aktif', 'İzinde']), 'mail': mail
    })

fake_sarf = [
    {'kod': 'STK-001', 'isim': 'HP 85A Siyah Toner (Yazıcı)', 'kategori': 'Yazıcı', 'adet': 3, 'kritik': 5, 'durum': 'Kritik'},
    {'kod': 'STK-002', 'isim': 'CAT6 Ethernet Kablosu (Kutu 305m)', 'kategori': 'Kablo', 'adet': 2, 'kritik': 1, 'durum': 'Yeterli'},
    {'kod': 'STK-003', 'isim': 'Logitech M171 Kablosuz Mouse', 'kategori': 'Aksesuar', 'adet': 15, 'kritik': 5, 'durum': 'Yeterli'},
    {'kod': 'STK-004', 'isim': 'Kingston 16GB USB 3.0 Bellek', 'kategori': 'Depolama', 'adet': 7, 'kritik': 10, 'durum': 'Azalıyor'},
    {'kod': 'STK-005', 'isim': 'A4 Fotokopi Kağıdı (Koli)', 'kategori': 'Kırtasiye', 'adet': 1, 'kritik': 3, 'durum': 'Kritik'},
    {'kod': 'STK-006', 'isim': 'Dell KM117 Kablosuz Klavye/Mouse Set', 'kategori': 'Aksesuar', 'adet': 8, 'kritik': 10, 'durum': 'Azalıyor'},
    {'kod': 'STK-007', 'isim': 'Paugge HDMI 2.1 Kablo (2 Metre)', 'kategori': 'Kablo', 'adet': 24, 'kritik': 5, 'durum': 'Yeterli'},
    {'kod': 'STK-008', 'isim': 'Samsung 870 EVO 500GB SSD', 'kategori': 'Donanım/Parça', 'adet': 4, 'kritik': 5, 'durum': 'Kritik'},
    {'kod': 'STK-009', 'isim': 'Ugreen Type-C to HDMI/USB Hub', 'kategori': 'Adaptör', 'adet': 12, 'kritik': 5, 'durum': 'Yeterli'},
    {'kod': 'STK-010', 'isim': 'Epson 103 EkoTank Siyah Mürekkep', 'kategori': 'Yazıcı', 'adet': 6, 'kritik': 5, 'durum': 'Yeterli'},
    {'kod': 'STK-011', 'isim': 'Epson 103 EkoTank Renkli Mürekkep Seti', 'kategori': 'Yazıcı', 'adet': 2, 'kritik': 3, 'durum': 'Kritik'},
    {'kod': 'STK-012', 'isim': 'RJ45 Network Ucu (100\'lü Paket)', 'kategori': 'Ağ Donanımı', 'adet': 5, 'kritik': 2, 'durum': 'Yeterli'},
    {'kod': 'STK-013', 'isim': '1m Patch Kablo (Sarı)', 'kategori': 'Kablo', 'adet': 45, 'kritik': 20, 'durum': 'Yeterli'},
    {'kod': 'STK-014', 'isim': 'Arctic MX-4 Termal Macun (4g)', 'kategori': 'Donanım/Parça', 'adet': 3, 'kritik': 2, 'durum': 'Yeterli'},
    {'kod': 'STK-015', 'isim': 'CR2032 BIOS Pili (5\'li Paket)', 'kategori': 'Donanım/Parça', 'adet': 1, 'kritik': 3, 'durum': 'Kritik'},
    {'kod': 'STK-016', 'isim': 'WD Blue 1TB 2.5" Harici Disk', 'kategori': 'Depolama', 'adet': 5, 'kritik': 5, 'durum': 'Yeterli'},
    {'kod': 'STK-017', 'isim': 'Logitech H390 USB Kulaklık', 'kategori': 'Aksesuar', 'adet': 9, 'kritik': 10, 'durum': 'Azalıyor'},
    {'kod': 'STK-018', 'isim': 'DisplayPort to VGA Dönüştürücü', 'kategori': 'Adaptör', 'adet': 18, 'kritik': 5, 'durum': 'Yeterli'},
    {'kod': 'STK-019', 'isim': '220V PC Güç Kablosu (Power Cord)', 'kategori': 'Kablo', 'adet': 35, 'kritik': 15, 'durum': 'Yeterli'},
    {'kod': 'STK-020', 'isim': 'Cisco 1G SFP Fiber Modül', 'kategori': 'Ağ Donanımı', 'adet': 2, 'kritik': 4, 'durum': 'Kritik'},
    {'kod': 'STK-021', 'isim': 'Notebook Standı (Alüminyum)', 'kategori': 'Aksesuar', 'adet': 6, 'kritik': 10, 'durum': 'Azalıyor'},
    {'kod': 'STK-022', 'isim': 'Sprey Ekran Temizleyici (500ml)', 'kategori': 'Kırtasiye/Temizlik', 'adet': 11, 'kritik': 5, 'durum': 'Yeterli'}
]

fake_fatura = [
    {'tarih': '10.08.2026', 'tedarikci': 'Vatan Bilgisayar', 'aciklama': '5 Adet Dell Vostro Laptop', 'tutar': '125.000 TL'},
    {'tarih': '01.09.2026', 'tedarikci': 'İtopya', 'aciklama': '10 Adet Logitech Klavye/Mouse Seti', 'tutar': '8.500 TL'},
    {'tarih': '05.09.2026', 'tedarikci': 'Microsoft Türkiye', 'aciklama': 'Office 365 Yıllık Yenileme', 'tutar': '45.000 TL'},
    {'tarih': '12.09.2026', 'tedarikci': 'Sinerji', 'aciklama': '3 Adet Asus 27" Monitör', 'tutar': '15.000 TL'},
    {'tarih': '15.09.2026', 'tedarikci': 'Hepsiburada', 'aciklama': '2 Adet TP-Link Access Point', 'tutar': '6.200 TL'},
    {'tarih': '18.09.2026', 'tedarikci': 'Amazon TR', 'aciklama': '5 Adet Samsung 1TB SSD', 'tutar': '12.500 TL'},
    {'tarih': '20.09.2026', 'tedarikci': 'Teknosa', 'aciklama': 'Toplantı Odası TV (LG 65")', 'tutar': '32.000 TL'},
    {'tarih': '22.09.2026', 'tedarikci': 'N11', 'aciklama': 'Kablo Düzenleyici ve Patch Cord', 'tutar': '2.100 TL'},
    {'tarih': '25.09.2026', 'tedarikci': 'Cisco', 'aciklama': 'Catalyst 2960 Switch Lisansı', 'tutar': '55.000 TL'},
    {'tarih': '27.09.2026', 'tedarikci': 'Vatan Bilgisayar', 'aciklama': '2 Adet HP Lazer Yazıcı', 'tutar': '18.000 TL'},
    {'tarih': '28.09.2026', 'tedarikci': 'İtopya', 'aciklama': 'UPS Akü Değişimi (10 Adet)', 'tutar': '9.500 TL'},
    {'tarih': '01.10.2026', 'tedarikci': 'Fortinet', 'aciklama': 'FortiGate Yıllık Güvenlik Lisansı', 'tutar': '110.000 TL'},
    {'tarih': '02.10.2026', 'tedarikci': 'Amazon TR', 'aciklama': 'IT Departmanı Araç Gereçleri', 'tutar': '4.300 TL'},
    {'tarih': '03.10.2026', 'tedarikci': 'Sinerji', 'aciklama': 'Server RAM Takviyesi (64GB)', 'tutar': '22.000 TL'},
    {'tarih': '05.10.2026', 'tedarikci': 'Vatan Bilgisayar', 'aciklama': 'Yönetici Laptop (MacBook Pro)', 'tutar': '85.000 TL'}
]

@app.route('/personel')
def personel():
    return render_template('personel.html', personel=fake_personel)

@app.route('/add_personel', methods=['POST'])
def add_personel():
    isim = request.form.get('isim')
    departman = request.form.get('departman')
    mail = request.form.get('mail')
    fake_personel.insert(0, {
        'id': len(fake_personel)+101, 'isim': isim, 'departman': departman, 'mail': mail,
        'unvan': 'Yeni Personel', 'cihaz_sayisi': 0, 'durum': 'Aktif'
    })
    return jsonify({'success': True})

@app.route('/add_ticket', methods=['POST'])
def add_ticket():
    konu = request.form.get('konu')
    kullanici = request.form.get('kullanici')
    from datetime import datetime
    fake_tickets.insert(0, {
        'id': f'INC-{random.randint(1000, 9999)}', 'kullanici': kullanici, 'konu': konu,
        'tarih': datetime.now().strftime("%d.%m.%Y %H:%M"), 'durum': 'Açık', 'oncelik': 'Yüksek'
    })
    return jsonify({'success': True})

@app.route('/add_stock', methods=['POST'])
def add_stock():
    isim = request.form.get('isim')
    adet = int(request.form.get('adet', 0))
    fake_sarf.insert(0, {
        'kod': f'STK-{random.randint(100, 999)}', 'isim': isim, 'kategori': 'Yeni Ürün',
        'adet': adet, 'kritik': max(1, int(adet/3)), 'durum': 'Yeterli'
    })
    return jsonify({'success': True})

@app.route('/sarf-malzeme')
def sarf_malzeme():
    return render_template('sarf_malzeme.html', sarf=fake_sarf)

@app.route('/ag-cihazlari')
def ag_cihazlari():
    fake_ag = [
        {'isim': 'Core Switch - Sistem Odası', 'ip': '192.168.1.1', 'marka': 'Cisco Catalyst 9300', 'lokasyon': 'Merkez Bina (SCH)', 'uptime': '45 Gün, 12 Saat', 'durum': 'Online'},
        {'isim': 'Edge Switch - Üretim', 'ip': '192.168.2.1', 'marka': 'HP Aruba 2930F', 'lokasyon': 'Üretim Bandı 1', 'uptime': '12 Gün, 5 Saat', 'durum': 'Online'},
        {'isim': 'Access Point - AR-GE', 'ip': '192.168.3.15', 'marka': 'Ubiquiti UniFi U6-Pro', 'lokasyon': 'AR-GE Ofisi', 'uptime': '5 Gün, 1 Saat', 'durum': 'Online'},
        {'isim': 'Güvenlik Duvarı (Firewall)', 'ip': '192.168.1.254', 'marka': 'Fortinet FortiGate 100F', 'lokasyon': 'Merkez Bina (SCH)', 'uptime': '120 Gün, 8 Saat', 'durum': 'Online'},
        {'isim': 'Edge Switch - Depo', 'ip': '192.168.4.1', 'marka': 'Cisco Catalyst 2960', 'lokasyon': 'Hammadde Deposu', 'uptime': '-', 'durum': 'Offline'},
        {'isim': 'Access Point - Yönetim', 'ip': '192.168.3.16', 'marka': 'Ubiquiti UniFi U6-Pro', 'lokasyon': 'Yönetim Katı', 'uptime': '30 Gün, 2 Saat', 'durum': 'Online'},
        {'isim': 'Edge Switch - İK', 'ip': '192.168.5.1', 'marka': 'HP Aruba 2530', 'lokasyon': 'İnsan Kaynakları', 'uptime': '80 Gün, 15 Saat', 'durum': 'Online'},
        {'isim': 'VPN Gateway', 'ip': '192.168.1.253', 'marka': 'Cisco ASA 5500', 'lokasyon': 'Sistem Odası', 'uptime': '200 Gün, 10 Saat', 'durum': 'Online'},
        {'isim': 'Storage (NAS)', 'ip': '192.168.1.100', 'marka': 'Synology RS3621xs+', 'lokasyon': 'Sistem Odası', 'uptime': '55 Gün, 20 Saat', 'durum': 'Online'},
        {'isim': 'Access Point - Kafeterya', 'ip': '192.168.3.20', 'marka': 'TP-Link Omada EAP660', 'lokasyon': 'Kafeterya', 'uptime': '-', 'durum': 'Offline'},
        {'isim': 'Yazıcı Sunucusu', 'ip': '192.168.1.50', 'marka': 'Windows Server 2022', 'lokasyon': 'Sistem Odası', 'uptime': '15 Gün, 6 Saat', 'durum': 'Online'}
    ]
    return render_template('ag_cihazlari.html', cihazlar=fake_ag)

@app.route('/raporlar')
def raporlar():
    toplam_cihaz = Cihaz.query.count()
    return render_template('raporlar.html', toplam_cihaz=toplam_cihaz)

fake_logs = [
    {'tarih': '10.09.2026 10:15:22', 'islem': 'YENİ ZİMMET', 'kullanici': 'Stajyer Admin', 'detay': 'DELL Vostro Laptop, İsmail ÖZTÜRK adlı personele zimmetlendi.', 'ip': '192.168.1.55'},
    {'tarih': '10.09.2026 09:45:10', 'islem': 'SİSTEM AYARI', 'kullanici': 'Stajyer Admin', 'detay': 'Karanlık mod ve E-posta bildirim ayarları güncellendi.', 'ip': '192.168.1.55'},
    {'tarih': '09.09.2026 16:30:00', 'islem': 'SİLME', 'kullanici': 'Sistem Yöneticisi', 'detay': 'Eski Model Monitör envanterden düşüldü.', 'ip': '192.168.1.10'},
    {'tarih': '09.09.2026 14:20:15', 'islem': 'YENİ ZİMMET', 'kullanici': 'Sistem Yöneticisi', 'detay': 'iPhone 16 Pro, Genel Müdür\'e zimmetlendi.', 'ip': '192.168.1.10'},
    {'tarih': '08.09.2026 08:30:00', 'islem': 'GİRİŞ', 'kullanici': 'Sistem Yöneticisi', 'detay': 'Sisteme başarılı giriş yapıldı.', 'ip': '192.168.1.10'},
    {'tarih': '07.09.2026 11:15:00', 'islem': 'YAZILIM GÜNCELLEME', 'kullanici': 'Stajyer Admin', 'detay': 'Windows 11 toplu güncelleştirmeleri onaylandı.', 'ip': '192.168.1.55'},
    {'tarih': '06.09.2026 14:45:22', 'islem': 'AĞ TARAMASI', 'kullanici': 'Sistem Yöneticisi', 'detay': '192.168.2.0/24 IP bloğu tarandı. 3 yeni cihaz bulundu.', 'ip': '192.168.1.10'},
    {'tarih': '05.09.2026 09:20:10', 'islem': 'YENİ ZİMMET', 'kullanici': 'Stajyer Admin', 'detay': 'Logitech MX Master 3, Tasarım Departmanına eklendi.', 'ip': '192.168.1.55'},
    {'tarih': '04.09.2026 17:00:00', 'islem': 'YEDEKLEME', 'kullanici': 'Sistem', 'detay': 'Otomatik haftalık veritabanı yedeği başarıyla alındı.', 'ip': 'localhost'},
    {'tarih': '03.09.2026 10:05:30', 'islem': 'SİLME', 'kullanici': 'Sistem Yöneticisi', 'detay': 'Bozuk HP Yazıcı envanterden düşüldü.', 'ip': '192.168.1.10'},
    {'tarih': '02.09.2026 15:40:15', 'islem': 'LİSANS YENİLEME', 'kullanici': 'Sistem Yöneticisi', 'detay': 'AutoCAD 2024 lisansları 1 yıl uzatıldı.', 'ip': '192.168.1.10'},
    {'tarih': '01.09.2026 08:00:00', 'islem': 'RAPOR OLUŞTURMA', 'kullanici': 'Sistem', 'detay': 'Aylık envanter PDF raporu oluşturuldu ve e-posta ile gönderildi.', 'ip': 'localhost'}
]

log_islemler = ["GİRİŞ", "YENİ ZİMMET", "SİLME", "YEDEKLEME", "ŞİFRE SIFIRLAMA", "HESAP KİLİTLEME", "STOK GİRİŞİ", "VPN BAĞLANTISI", "LİSANS EKLEME"]
log_kullanicilar = ["Sistem Yöneticisi", "Stajyer Admin", "Network Uzmanı", "Sistem", "Güvenlik Duvarı"]
log_detaylar = [
    "Sisteme IP üzerinden başarılı giriş yapıldı.", 
    "Active Directory kullanıcı parolası resetlendi.", 
    "Yeni bir Access Point ağa dahil edildi.", 
    "Depodan 5 adet sarf malzeme çıkışı yapıldı.",
    "Zabbix sunucusu üzerinden SNMP alarmı alındı.",
    "Kullanıcı hesabı çoklu başarısız giriş sebebiyle kilitlendi.",
    "Firewall kuralı güncellendi (Port 443 İzni).",
    "Yeni lisans anahtarı sisteme girildi.",
    "Tüm switch konfigürasyonları yedeklendi."
]

for i in range(85):
    gun = random.randint(1, 30)
    ay = 8
    saat = random.randint(8, 18)
    dk = random.randint(10, 59)
    fake_logs.append({
        'tarih': f'{gun:02d}.{ay:02d}.2026 {saat:02d}:{dk:02d}:00',
        'islem': random.choice(log_islemler),
        'kullanici': random.choice(log_kullanicilar),
        'detay': random.choice(log_detaylar),
        'ip': f'192.168.{random.randint(1,5)}.{random.randint(10, 250)}'
    })

# Tarihe göre sırala
fake_logs.sort(key=lambda x: datetime.strptime(x['tarih'], "%d.%m.%Y %H:%M:%S"), reverse=True)

@app.route('/log')
def log():
    return render_template('log.html', logs=fake_logs)

import csv
from io import StringIO
from flask import Response

@app.route('/export/excel')
def export_excel():
    cihazlar = Cihaz.query.all()
    si = StringIO()
    # BOM for Excel to read Turkish chars correctly
    si.write('\ufeff')
    writer = csv.writer(si, delimiter=';')
    writer.writerow(['Personel', 'Departman', 'Cihaz Kategorisi', 'Marka & Model', 'Barkod No', 'IP Adresi'])
    
    for c in cihazlar:
        writer.writerow([c.personel_ad_soyad, c.lokasyon_ofis, c.kategori, c.marka_model, c.barkod_no, c.ip_adresi])
    
    output = si.getvalue()
    si.close()
    
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment;filename=it_envanter_raporu.csv"}
    )

@app.route('/export/pdf')
def export_pdf():
    cihazlar = Cihaz.query.all()
    return render_template('pdf_report.html', cihazlar=cihazlar)

@app.route('/ag-kontrol')
def ag_kontrol(): return render_template('ag_kontrol.html')

@app.route('/sifre-kasasi')
def sifre_kasasi(): return render_template('sifre_kasasi.html')

@app.route('/add_fatura', methods=['POST'])
def add_fatura():
    tedarikci = request.form.get('tedarikci')
    aciklama = request.form.get('aciklama')
    tutar = request.form.get('tutar')
    from datetime import datetime
    fake_fatura.insert(0, {
        'tarih': datetime.now().strftime("%d.%m.%Y"),
        'tedarikci': tedarikci,
        'aciklama': aciklama,
        'tutar': tutar + ' TL'
    })
    return jsonify({'success': True})

@app.route('/satin-alma')
def satin_alma(): return render_template('satin_alma.html', faturalar=fake_fatura)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    flash('Sistemden başarıyla çıkış yaptınız.', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
