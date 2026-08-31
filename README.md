# 🛡️ NetShield IDS

> **Python, Scapy ve FastAPI ile geliştirilmiş gerçek zamanlı Ağ Saldırı Tespit Sistemi (IDS).**

NetShield IDS; yetkili olduğunuz ağ trafiğini gerçek zamanlı olarak izlemek, şüpheli davranışları tespit etmek, risk seviyeleri hesaplamak ve potansiyel olarak zararlı bir etkinlik algılandığında operatörü uyarmak için tasarlanmış açık kaynaklı bir savunma güvenliği aracıdır.

Proje; ağ saldırı tespiti (IDS) kavramlarını öğrenmek ve denemek için hafif ve anlaşılır bir alternatif sunmak amacıyla geliştirilmiştir.

---

## ✨ Özellikler

### 🔍 Ağ İzleme
- Scapy ile gerçek zamanlı paket yakalama
- Ağ arayüzü seçimi
- Canlı paket istatistikleri
- Otomatik ağ geçidi keşfi

### 🚨 Tespit Motoru
NetShield şu anda aşağıdaki şüpheli davranışları izler:

- ARP eşleşme değişiklikleri / olası ARP spoofing
- SYN trafik anomalileri
- UDP trafik anomalileri
- ICMP trafik anomalileri
- TCP port taraması
- Host taraması
- Olağandışı trafik davranışları

### 🧠 Risk Motoru
- IP tabanlı risk puanlama
- Önem seviyeleri: `LOW`, `MEDIUM`, `HIGH`, `CRITICAL`
- Uyarlanabilir trafik tabanı
- Tekrarlanan bildirimleri azaltmak için uyarı bekleme süresi
- Zaman içinde risk puanının azalması

### 🔔 Uyarı Sistemi
- Gerçek zamanlı terminal uyarıları
- İsteğe bağlı Windows bildirim sesi
- İsteğe bağlı Discord webhook uyarıları
- Yapılandırılmış güvenlik olay kayıtları

### 📊 Raporlama
- JSON olay kayıtları
- CSV olay kayıtları
- HTML güvenlik raporları

### 🌐 Web Paneli
Dahili FastAPI web paneli şunları gösterir:

- Paket sayısı
- Uyarı sayısı
- İzlenen host sayısı
- Çalışma süresi
- Son güvenlik olayları
- IP risk puanları

---

## 🖥️ Web Paneli

NetShield çalışırken web paneline yerel makineden erişilebilir.

Default address:

```text
http://127.0.0.1:8080
```

Panel otomatik olarak yenilenir ve IDS tarafından tespit edilen son olayları gösterir.

---

## 📋 Gereksinimler

- Python `3.10+`
- Windows, Linux veya macOS
- Scapy
- FastAPI
- Uvicorn
- PyYAML
- Requests

### Windows

Windows kullanıcılarının paket yakalama için **Npcap** kurması gerekir.

Npcap kurulurken varsayılan kurulum seçenekleri normal paket yakalama kullanımı için genellikle yeterlidir.

### Yetkiler

İşletim sistemine ve kullanılan ağ arayüzüne bağlı olarak paket yakalama için yönetici yetkileri gerekebilir.

Windows'ta paket yakalama çalışmıyorsa PowerShell veya Komut İstemi'ni **Yönetici olarak** çalıştırmayı deneyin.

---

# 🚀 Kurulum

## 1. Repoyu klonlayın

```bash
git clone https://github.com/BiggerSon/NetShield.git
cd NetShield
```

## 2. Sanal ortam oluşturun

### Windows

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3. Bağımlılıkları yükleyin

```bash
pip install -r requirements.txt
```

---

# ▶️ NetShield'ı Çalıştırma

IDS'yi başlatın:

```bash
python main.py
```

NetShield kullanılabilir ağ arayüzlerini gösterecektir.

Example:

```text
========================================================================
                 🛡️ NETSHIELD IDS
                 Network Security Monitor
========================================================================
Version : 2.0.0

[+] Gateway detected: 192.168.1.1

[+] Detection modules:
    ARP Spoofing              : True
    SYN anomaly              : True
    UDP anomaly              : True
    ICMP anomaly             : True
    TCP port scan             : True
    Host scan                 : True
    Adaptive baseline         : True
    Automatic mitigation      : False

[+] Dashboard: http://127.0.0.1:8080

[+] NetShield çalışıyor.
[+] CTRL+C ile durdurabilirsin.
```

NetShield'ın izlemesini istediğiniz ağ arayüzünü seçin.

---

# 🎯 Ağ Arayüzü Seçimi

Kullanılabilir arayüzleri NetShield'a listeletebilirsiniz:

```bash
python main.py
```

Veya arayüzü doğrudan belirtebilirsiniz:

```bash
python main.py --interface "YOUR_INTERFACE"
```

`YOUR_INTERFACE` değerini sisteminizde Scapy tarafından gösterilen gerçek arayüz adıyla değiştirin.

Hangi arayüzü kullanacağınızdan emin değilseniz NetShield'ı `--interface` parametresi olmadan başlatın ve listeden doğru adaptörü seçin.

---

# ⚙️ Yapılandırma

Temel ayarlar şu dosyada tutulur:

```text
config.yaml
```

Tek tek tespit modüllerini etkinleştirebilir/devre dışı bırakabilir ve eşik değerlerini değiştirebilirsiniz.

Example:

```yaml
detection:
  window_seconds: 10

  syn:
    enabled: true
    threshold: 100

  udp:
    enabled: true
    threshold: 250

  icmp:
    enabled: true
    threshold: 100

  port_scan:
    enabled: true
    unique_ports: 20

  host_scan:
    enabled: true
    unique_hosts: 25

  arp:
    enabled: true
```

---

# 🧠 Uyarlanabilir Tespit

NetShield yalnızca sabit eşiklere bağlı kalmak yerine uyarlanabilir bir trafik tabanı kullanabilir.

Configuration:

```yaml
adaptive:
  enabled: true
  multiplier: 3.0
  minimum_baseline: 10
```

Bu özellik, tespit motorunun daha önce gözlemlenen trafik davranışlarını dikkate almasını sağlar.

Uyarlanabilir tespit, yalnızca sabit eşikler kullanmaya kıyasla yanlış pozitifleri azaltmayı amaçlar.

---

# 🚨 Uyarı Sistemi

Terminal uyarıları varsayılan olarak etkindir:

```yaml
alerts:
  console: true
```

Example:

```text
========================================================================
🚨 NETSHIELD SECURITY ALERT
========================================================================
Time       : 2026-08-31T17:02:31
Type       : TCP Port Scan
Severity   : HIGH
Risk       : 81/100
Source     : 192.168.1.25
Destination: 192.168.1.1
Message    : Multiple destination ports observed from one source.
========================================================================
```

NetShield ayrıca aynı tespitin konsolu veya bildirim servisini art arda uyarılarla doldurmasını önlemek için bir uyarı bekleme süresi kullanır.

---

# 🔔 Discord Bildirimleri

Discord bildirimleri isteğe bağlıdır.

In `config.yaml`:

```yaml
alerts:
  console: true

  discord:
    enabled: true
    webhook_url: "YOUR_WEBHOOK_URL"
```

Yer tutucuyu kendi Discord webhook adresinizle değiştirin.

## ⚠️ Önemli

**Gerçek webhook adreslerini, API anahtarlarını, token'ları, şifreleri veya diğer gizli bilgileri GitHub'a kesinlikle yüklemeyin.**

Hassas değerleri mümkün olduğunca public repodan ayrı tutun.

---

# 📊 Kayıtlar ve Raporlar

Güvenlik olayları şu dosyalarda saklanır:

```text
logs/security_events.json
logs/security_events.csv
```

JSON formatı uygulamalar ve otomasyon için kullanışlıdır.

CSV formatı elektronik tablolar ve veri analizi için kullanışlıdır.

---

# 📄 HTML Güvenlik Raporu

Kaydedilen olaylardan HTML raporu oluşturun:

```bash
python main.py --report
```

Rapor şu konumda oluşturulur:

```text
reports/security_report.html
```

---

# 🧪 Testler

Projede risk motoru için temel testler bulunmaktadır.

Kurulu değilse pytest'i yükleyin:

```bash
pip install pytest
```

Testleri çalıştırın:

```bash
pytest
```

---

# 📁 Proje Yapısı

```text
NetShield/
│
├── main.py
├── config.yaml
├── requirements.txt
├── README.md
├── .gitignore
├── LICENSE
│
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
│   ├── state.py
│   ├── alerts.py
│   ├── risk.py
│   ├── detector.py
│   ├── capture.py
│   ├── reporter.py
│   └── discovery.py
│
├── web/
│   ├── __init__.py
│   ├── server.py
│   │
│   ├── templates/
│   │   └── index.html
│   │
│   └── static/
│       ├── style.css
│       └── app.js
│
├── logs/
│   └── .gitkeep
│
├── reports/
│   └── .gitkeep
│
└── tests/
    └── test_risk.py
```

---

# 🛡️ Güvenlik Modeli

NetShield bir **IDS (Intrusion Detection System / Saldırı Tespit Sistemi)**'dir.

Temel çalışma amacı:

```text
Capture
   ↓
Analyze
   ↓
Detect
   ↓
Score
   ↓
Alert
   ↓
Log
   ↓
Report
```

Otomatik müdahale varsayılan olarak devre dışıdır:

```yaml
mitigation:
  enabled: false
```

Bu bilinçli bir tercihtir.

Bir tespit sistemi, dikkatlice tasarlanmış bir müdahale politikası olmadan tek bir potansiyel yanlış tespide dayanarak trafiği otomatik olarak engellememelidir.

---

# ⚠️ Yanlış Pozitifler

Ağ davranışı aşağıdaki etkenlere göre önemli ölçüde değişebilir:

- Cihaz sayısı
- Ağ hızı
- Uygulamalar
- Bulut servisleri
- DNS etkinliği
- Oyunlar
- Yayın/streaming
- Yazılım güncellemeleri
- Ağ topolojisi

Bu nedenle bir tespit olayı, **otomatik olarak bir saldırı gerçekleştiği anlamına gelmez**.

Eşik değerleri izlenen ortama göre ayarlanmalıdır.

---

# 🔐 Sorumlu Kullanım

NetShield şu amaçlarla kullanılmak üzere tasarlanmıştır:

- Kendi cihazlarınız
- Kendi ağlarınız
- Laboratuvar ortamları
- Yetkili güvenlik testleri
- Savunma amaçlı ağ izleme
- Siber güvenlik eğitimi ve araştırması

**Yalnızca inceleme yetkinizin bulunduğu ağ trafiğini izleyin.**

Uygun yetki olmadan NetShield'ı ağları, cihazları veya trafiği izlemek için kullanmayın.

---

# 🤝 Katkıda Bulunma

Katkılarınızı bekliyoruz.

Pull request göndermeden önce:

1. Değişikliklerinizi test edin.
2. Gizli bilgiler veya kimlik doğrulama bilgileri eklemeyin.
3. Güvenlik açısından hassas yapılandırmaları commit'lerin dışında tutun.
4. Gerektiğinde dokümantasyonu güncelleyin.
5. Değişiklikleri odaklı tutun ve yapılan değişikliğin amacını açıklayın.

Gelecekte geliştirilebilecek özellikler:

- Daha fazla protokol tespit modülü
- Daha gelişmiş trafik tabanı öğrenimi
- PCAP içe aktarma ve analiz
- Gelişmiş olay korelasyonu
- Web paneli için kimlik doğrulama
- Veritabanı destekli olay depolama
- Ek bildirim sağlayıcıları
- Geliştirilmiş görselleştirme
- İsteğe bağlı savunma amaçlı müdahale mekanizmaları

---

# 📜 Lisans

NetShield IDS MIT Lisansı ile yayımlanmaktadır.

Lisansın tamamı için `LICENSE` dosyasına bakın.

---

# ⭐ Proje Durumu

**Mevcut sürüm:** `2.0.0`

NetShield, aktif olarak geliştirilen savunma amaçlı bir ağ izleme projesidir.

Mevcut sürüm; gerçek zamanlı tespit, uyarı, risk puanlama, kayıt, raporlama ve hafif bir web paneline odaklanmaktadır.

---

## 🛡️ NetShield IDS

**İzle. Tespit Et. Uyar.**

Kullanılan teknolojiler:

- Python
- Scapy
- FastAPI
- Uvicorn
- PyYAML
- Requests
