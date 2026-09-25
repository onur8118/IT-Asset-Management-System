# IT Asset Management & Helpdesk System

Bu proje, bir IT departmanýnýn tüm donaným, lisans, personel (Active Directory), sarf malzeme ve destek (Ticket) süreçlerini tek bir platformda toplamak amacýyla geliþtirilmiþ web tabanlý bir otomasyon sistemidir.

## ?? Teknolojiler (Tech Stack)
* **Backend:** Python, Flask
* **Veritabaný:** SQLite
* **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
* **Kütüphaneler:** jQuery, DataTables, SweetAlert2, Chart.js, jsPDF

## ?? Özellikler
* **Donaným Envanteri:** Cihaz ekleme, düzenleme ve dinamik QR kod üretimi.
* **Personel Yönetimi:** Active Directory simülasyonu, þifre sýfýrlama, hesabý kilitleme ve cihaza zimmetleme.
* **Að (NAC) Kontrolü:** Ortak Wi-Fi ana þalteri ve personel bazlý VPN yetkilendirmesi.
* **Satýn Alma ve Finans:** jsPDF kullanýlarak GÝB formatýna uygun PDF E-Fatura üretimi.
* **Þifre Kasasý (Vault):** Kritik sunucu ve cihaz þifrelerinin maskelenmiþ olarak güvenle saklanmasý.
* **Sarf Malzeme:** Stok kritik seviye uyarý (Progress bar) sistemi.
* **Sistem Loglarý:** Uygulama üzerinde yapýlan iþlemlerin IP ve yetkili detaylarýyla kaydedilmesi.

## ?? Kurulum (Installation)
1. Repoyu klonlayýn: \git clone <repo-url>\
2. Gerekli kütüphaneleri yükleyin: \pip install -r requirements.txt\
3. Veritabanýný oluþturun: \python seed_db.py\
4. Uygulamayý çalýþtýrýn: \python app.py\

Proje \http://127.0.0.1:5000\ adresinde çalýþacaktýr.

---
*Bu proje, staj kapsamýnda geliþtirilmiþ bir prototiptir.*
