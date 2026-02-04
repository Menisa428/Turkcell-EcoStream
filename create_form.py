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
        self.set_text_color(100, 100, 100)
        self.cell(0, 10, clean_text('Eco-Stream: Teknik Simulasyon Kilavuzu'), 0, 1, 'R')
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Sayfa {self.page_no()}', 0, 0, 'C')

# --- TEKNİK ADIMLAR ---
data = {
    "ADIM 1: BASLATMA VE SESSION STATE (Initialization)": """
Simulasyon baslatildiginda, sistem once Streamlit'in 'Session State' hafizasini kontrol eder.
- Trafik Gecmisi (Traffic History): Son 60 saniyenin verisi hafizaya yuklenir.
- Termal Gecmis (Thermal History): Sunucularin sicaklik verileri baslatilir.
- Varsayilan Degerler: Baslangic trafigi 1.5 Tbps, aktif sunucu sayisi 40 olarak atanir.
""",
    "ADIM 2: VERI URETIMI VE GIRIS (Input Generation)": """
Kullanicinin sectigi 'Veri Kaynagi'na gore trafik uretilir:
A) Algoritmik Mod: Anlik saate gore (Sabah dusuk, Aksam yuksek) baz trafik hesaplanir.
B) Replay Modu: Sinus dalgasi kullanilarak duzenli ve tahmin edilebilir bir veri akisi saglanir.

Bu asama, core/simulator.py dosyasindaki fonksiyonlar tarafindan yonetilir.
""",
    "ADIM 3: OLAY ENJEKSIYONU (Event Injection)": """
Sistemin dayanikliligini test etmek icin normal trafigin uzerine 'Kaos' eklenir:
- Game+ Event: Rastgele zamanlarda ani trafik sicramalari (Spike) olusturulur.
- Senaryo Modlari: Kullanici 'Derbi Maci' veya 'Siber Saldiri' sectiginde, trafik carpanlari (Multiplier) devreye girer ve veri manipule edilir.
""",
    "ADIM 4: AI TAHMINLEME (Predictive Analysis)": """
Gelen veri, 'core/logic.py' icindeki tahmin motoruna gonderilir.
- Sistem, gecmis veriye bakarak gelecek 10 dakikalik yuk tahmini yapar.
- Bu tahmin, grafikte 'Mavi Kesik Cizgi' olarak gorsellestirilir ve operatorun onleyici aksiyon almasini saglar.
""",
    "ADIM 5: KAPASITE PLANLAMA (Capacity Planning)": """
Endustri Muhendisligi hesaplamalari burada devreye girer:
1. Ham Ihtiyac: Anlik Trafik / Kabin Kapasitesi (40Gbps).
2. Guvenlik Stogu (Buffer): Senaryoya gore %20, %40 veya %50 yedek sunucu eklenir.
3. Hedef Sunucu Sayisi: (Ham Ihtiyac + Buffer) formuluyle kesinlesir.
""",
    "ADIM 6: FIZIK MOTORU VE MALIYET (Physics Engine)": """
Sunucular kapansa bile sogutma maliyeti aninda dusmez.
- Newton'un Soguma Yasasi (Thermal Inertia) kullanilarak, sogutma enerjisinin zamanla azalmasi simule edilir.
- Enerji Tuketimi = (IT Yuku + Sogutma Yuku) * Elektrik Birim Fiyati.
- Eger 'Solar Mod' aktifse, toplam maliyete %20 indirim uygulanir.
""",
    "ADIM 7: CIKTI VE RAPORLAMA (Output & Dashboard)": """
Tum bu hesaplamalar milisaniyeler icinde tamamlanir ve arayuze yansitilir:
- Server Rack Gorseli: Hangi sunucunun aktif, hangisinin uykuda oldugunu gosterir.
- Canli Grafikler: Plotly kutuphanesi ile anlik cizilir.
- Toast Bildirimleri: Kritik degisimlerde sag altta uyari penceresi acilir.
"""
}

# --- PDF OLUŞTURMA ---
pdf = PDFForm()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# Başlık Kısmı
pdf.set_font('Arial', 'B', 16)
pdf.set_text_color(0, 51, 102) # Koyu Mavi
pdf.cell(0, 10, clean_text("ECO-STREAM SIMULASYON AKISI"), 0, 1, 'C')
pdf.set_font('Arial', '', 11)
pdf.set_text_color(50, 50, 50)
pdf.cell(0, 10, clean_text("Algorithm Workflow & Technical Steps"), 0, 1, 'C')
pdf.ln(10)

# İçeriği Döngüyle Yaz
for step, content in data.items():
    # Adım Başlığı
    pdf.set_font('Arial', 'B', 11)
    pdf.set_fill_color(230, 240, 255) # Açık Mavi Arkaplan
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 8, clean_text(step), 0, 1, 'L', fill=True)
    
    # İçerik Metni
    pdf.set_font('Arial', '', 10)
    pdf.multi_cell(0, 6, clean_text(content.strip()))
    pdf.ln(6)

# İmza Bölümü
pdf.ln(10)
pdf.set_draw_color(200, 200, 200)
pdf.line(10, pdf.get_y(), 200, pdf.get_y()) # Çizgi çek
pdf.ln(5)

pdf.set_font('Arial', 'B', 10)
pdf.cell(60, 10, clean_text("Nisa Nur Arslan"), 0, 0, 'C')
pdf.cell(60, 10, clean_text("Nisa Yanik"), 0, 0, 'C')
pdf.cell(60, 10, clean_text("Seviye Nur Gonulolmez"), 0, 1, 'C')

# Dosyayı Kaydet (İsmi değiştirdik: Teknik Doküman yaptık)
file_name = "EcoStream_Teknik_Simulasyon_Dokumani.pdf"
pdf.output(file_name)

print(f"✅ Teknik Kılavuz Başarıyla Oluşturuldu: {file_name}")