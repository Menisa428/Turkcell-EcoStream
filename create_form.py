# create_form.py
from fpdf import FPDF

# Türkçe karakterleri düzelten fonksiyon
def clean_text(text):
    if not isinstance(text, str): return str(text)
    replacements = {
        'ş': 's', 'Ş': 'S', 'ı': 'i', 'İ': 'I', 'ğ': 'g', 'Ğ': 'G',
        'ü': 'u', 'Ü': 'U', 'ö': 'o', 'Ö': 'O', 'ç': 'c', 'Ç': 'C', 'â': 'a'
    }
    for tr, en in replacements.items():
        text = text.replace(tr, en)
    return text.encode('latin-1', 'ignore').decode('latin-1')

class PDFForm(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 10)
        self.cell(0, 10, clean_text('Eco-Stream Proje Ekibi'), 0, 1, 'R')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Sayfa {self.page_no()}', 0, 0, 'C')

# --- BAŞVURU İÇERİĞİ (TAKIM BİLGİLERİ DAHİL) ---
data = {
    "1. PROJE KUNYESI": """
Proje Adi: Turkcell Eco-Stream: 5G AI-Powered Digital Twin
Proje Teknoloji Alani: Yapay Zeka, Enerji Verimliligi, Telekomunikasyon, Dijital Ikiz
Proje Sahiplerinin Adi Soyadi:
- Nisa Nur Arslan
- Nisa Yanik
- Seviye Nur Gonulolmez
""",
    "2. PROJE AMACI": """
Bu projenin temel amaci, telekomunikasyon sektorundeki en buyuk operasyonel gider (OPEX) kalemi olan enerji maliyetlerini minimize etmek ve karbon ayak izini azaltmaktir.

Turkcell Eco-Stream, 150 kabinlik bir veri merkezini simule eden bir 'Dijital Ikiz' cozumudur. Proje, sebeke trafigini anlik olarak izleyerek ve yapay zeka ile gelecek yuku tahmin ederek, sunuculari dinamik bir sekilde acip kapatmayi hedefler. Amacimiz, hizmet kalitesinden (SLA) odun vermeden, sadece ihtiyac duyulan kapasiteyi aktif tutarak enerji tuketimini optimize etmektir.
""",
    "3. PROJE ACIKLAMASI": """
HEDEF KITLE:
Projenin birincil hedef kitlesi Turkcell, Vodafone gibi buyuk telekomunikasyon operatorleri ve veri merkezi isletmecileridir.

SORUN VE IHTIYAC:
Geleneksel sistemler 'Reaktif' degil 'Statik' calisir. Trafik olsa da olmasa da sunucular tam kapasite calisir. Bu da yuksek enerji maliyeti, karbon salinimi ve donanim yipranmasi yaratir.

COZUM VE FAYDA:
Eco-Stream, Python tabanli simulasyon motoru sayesinde, veri trafigindeki dalgalanmalari milisaniyeler icinde analiz eder. 'Tahminleme Algoritmasi' (Predictive AI) kullanarak trafigin artacagini onceden sezer ve sunuculari devreye alir.
Yillik projeksiyonda tek bir veri merkezi icin yaklasik 15-20 Milyon TL tasarruf ongorulmektedir.

ERISILEBILIRLIK:
Yoneticiler icin gelistirilen 'Turkcell Platinum Dashboard' arayuzu ile kullanim kolayligi sunar.
""",
    "4. OZGUNLUK": """
Eco-Stream, sadece bir otomasyon degil; fizik kurallarini ve donanim sagligini gozeten butunlesik bir muhendislik cozumudur.

FIZIK MOTORU (Physics Engine): Newton'un Soguma Yasasi simule edilerek, termal sonumlenme (Thermal Inertia) hesaplanir.
WEAR LEVELING (Asinma Dengeleme): 'Rotational Scheduling' algoritmasi ile yuk surekli farkli sunuculara dagitilir, donanim omru uzatilir.
SIBER SALDIRI MODU: Guvenlik tehdidi algilandiginda tasarrufu devre disi birakip hizmet surekliligini one alan 'Fail-Safe' mekanizmasi vardir.
""",
    "5. ETKI VE SURDURULEBILIRLIK": """
EKONOMIK DEGER: Enerji tuketimini (PUE degerini) optimize ederek operasyonel maliyetleri dusurur.
SOSYAL DEGER: Ulkenin enerji disa bagimliligini azaltmaya ve karbon emisyonlarini dusurmeye yardimci olur.
VERI GIZLILIGI: Kullanilan veriler tamamen anonim 'Sebeke Trafik Yogunlugu' verileridir. KVKK ve GDPR uyumlulugu tamdir.
""",
    "6. PAZAR ARASTIRMASI": """
PAZAR BUYUKLUGU: Global Yesil Veri Merkezi pazarinin hizla buyumesiyle proje genis bir pazara sahiptir.
REKABET ANALIZI: Rakipler genellikle 'Vendor-Lock' (Marka Bagimliligi) yaratir. Eco-Stream ise 'Vendor-Agnostic' (Markadan Bagimsiz) bir yazilim katmanidir.
FARKLILASMA: Rakipler sadece enerjiyi kisarken, Eco-Stream yoneticilere finansal projeksiyon sunar ve bunu resmi PDF raporuyla belgeler.
""",
    "7. TICARI POTANSIYEL": """
GELIR MODELI: Veri merkezi basina yillik lisanslama ve saglanan enerji tasarrufu uzerinden basari bazli komisyon (%10-%20).
BUYUME ONGORUSU: MVP asamasindaki proje, once pilot uygulama, ardindan tum cekirdek sebekeye yayginlastirilabilir.
""",
    "8. TEKNIK YONTEM VE UYGULANABILIRLIK": """
YONTEM: Yoneylem Arastirmasi (OR) teknikleri ve Agirlikli Hareketli Ortalama tahminleme modelleri kullanilmistir. %99.9 SLA basarisina ulasilmistir.
TEKNOLOJI: Python, Streamlit, Plotly, FPDF.
UYGULANABILIRLIK: Proje, donanima mudahale etmeden, mevcut yonetim yazilimlarinin uzerine bir 'Orkestrasyon Katmani' olarak (Overlay) kurulabilir.
""",
    "9. PROJE YONETIMI": """
RISK YONETIMI: Yapay zeka hatasina karsi 'Buffer' sunucu mantigi ve siber saldirilara karsi 'Guvenlik Modu' gelistirilmistir.
YONETIM STRATEJISI: Cevik (Agile) yontemle iteratif olarak gelistirilmistir (V14.0 -> V19.0).
ADAPTASYON: Modular mimarisi sayesinde farkli donanimlara kolayca adapte olabilir.
""",
    "10. PILOT UYGULAMALAR": """
Proje su an 'Simule Edilmis Pilot Ortamda' (Digital Twin) basariyla calismaktadir. Gercek dunya senaryolari (Derbi Maci, Gece Modu, Saldiri) test edilmis ve yillik tasarruf projeksiyonlari dogrulanmistir.
"""
}

# --- PDF OLUŞTURMA ---
pdf = PDFForm()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# Başlık
pdf.set_font('Arial', 'B', 16)
pdf.set_text_color(0, 0, 128) # Lacivert
pdf.cell(0, 10, clean_text("TURKCELL ECO-STREAM"), 0, 1, 'C')
pdf.set_font('Arial', '', 12)
pdf.cell(0, 10, clean_text("5G AI-POWERED DIGITAL TWIN - TAKIM BASVURU FORMU"), 0, 1, 'C')
pdf.ln(10)

# İçeriği Döngüyle Yaz
for title, content in data.items():
    # Başlık
    pdf.set_font('Arial', 'B', 12)
    pdf.set_fill_color(240, 240, 240) # Açık Gri
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, clean_text(title), 0, 1, 'L', fill=True)
    
    # Metin
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 6, clean_text(content.strip()))
    pdf.ln(5)

# Dosyayı Kaydet
file_name = "EcoStream_Takim_Basvuru_Dokumani.pdf"
pdf.output(file_name)

print(f"✅ Takım PDF'i Başarıyla Oluşturuldu: {file_name}")