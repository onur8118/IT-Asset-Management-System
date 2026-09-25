IT Asset Management & Helpdesk System
Bu proje, bir IT departmanının tüm donanım, lisans, personel (Active Directory), sarf malzeme ve destek (Ticket) süreçlerini tek bir platformda toplamak amacıyla geliştirilmiş web tabanlı bir otomasyon sistemidir.

?? Teknolojiler (Tech Stack)
Backend: Python, Flask
Veritabanı: SQLite
Frontend: HTML5, CSS3, Bootstrap 5, JavaScript
Kütüphaneler: jQuery, DataTables, SweetAlert2, Chart.js, jsPDF
?? Özellikler
Donanım Envanteri: Cihaz ekleme, düzenleme ve dinamik QR kod üretimi.
Personel Yönetimi: Active Directory simülasyonu, şifre sıfırlama, hesabı kilitleme ve cihaza zimmetleme.
Ağ (NAC) Kontrolü: Ortak Wi-Fi ana şalteri ve personel bazlı VPN yetkilendirmesi.
Satın Alma ve Finans: jsPDF kullanılarak GİB formatına uygun PDF E-Fatura üretimi.
Şifre Kasası (Vault): Kritik sunucu ve cihaz şifrelerinin maskelenmiş olarak güvenle saklanması.
Sarf Malzeme: Stok kritik seviye uyarı (Progress bar) sistemi.
Sistem Logları: Uygulama üzerinde yapılan işlemlerin IP ve yetkili detaylarıyla kaydedilmesi.
?? Kurulum (Installation)
Repoyu klonlayın: \git clone \
Gerekli kütüphaneleri yükleyin: \pip install -r requirements.txt\
Veritabanını oluşturun: \python seed_db.py\
Uygulamayı çalıştırın: \python app.py\
Proje \http://127.0.0.1:5000\ adresinde çalışacaktır.
