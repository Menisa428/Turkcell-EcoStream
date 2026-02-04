# core/report.py
from fpdf import FPDF
from datetime import datetime

# Türkçe karakterleri İngilizceye çeviren ve Emojileri temizleyen fonksiyon
def clean_text(text):
    if not isinstance(text, str):
        return str(text)
    
    # Türkçe Harf Dönüşümü
    replacements = {
        'ş': 's', 'Ş': 'S',
        'ı': 'i', 'İ': 'I',
        'ğ': 'g', 'Ğ': 'G',
        'ü': 'u', 'Ü': 'U',
        'ö': 'o', 'Ö': 'O',
        'ç': 'c', 'Ç': 'C',
        'â': 'a'
    }
    for tr, en in replacements.items():
        text = text.replace(tr, en)
    
    # Emojileri ve ASCII dışı karakterleri silmek için
    return text.encode('latin-1', 'ignore').decode('latin-1')

class PDFReport(FPDF):
    def header(self):
        self.set_fill_color(255, 201, 0)
        self.rect(0, 0, 210, 20, 'F')
        self.set_font('Arial', 'B', 15)
        self.set_text_color(0, 21, 41)
        self.cell(0, 10, 'TURKCELL PLATINUM - ECO STREAM RAPORU', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Sayfa {self.page_no()}', 0, 0, 'C')

def generate_pdf(scenario, active_servers, total_servers, traffic, saved_co2, sla):
    pdf = PDFReport()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    pdf.set_font("Arial", size=12)
    date_str = datetime.now().strftime('%Y-%m-%d %H:%M')
    pdf.cell(0, 10, f"Rapor Tarihi: {date_str}", ln=True, align='R')
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 10, "1. SEBEKE DURUM OZETI", ln=True, fill=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", size=11)
    clean_scenario = clean_text(scenario)
    pdf.cell(0, 8, f"- Aktif Senaryo Modu: {clean_scenario}", ln=True)
    pdf.cell(0, 8, f"- Anlik Veri Trafigi: {traffic/1000:.2f} Gbps", ln=True)
    pdf.cell(0, 8, f"- SLA (Hizmet Kalitesi): %{sla:.4f}", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.set_fill_color(230, 230, 230)
    pdf.cell(0, 10, "2. KAYNAK OPTIMIZASYONU", ln=True, fill=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", size=11)
    pdf.cell(0, 8, f"- Toplam Sunucu Kapasitesi: {total_servers} Adet", ln=True)
    pdf.cell(0, 8, f"- Aktif Kullanilan Sunucu: {active_servers} Adet", ln=True)
    pdf.cell(0, 8, f"- Dinamik Olarak Kapatilan (Uyku): {total_servers - active_servers} Adet", ln=True)
    pdf.ln(10)
    
    pdf.set_font("Arial", 'B', 14)
    pdf.set_fill_color(255, 201, 0)
    pdf.cell(0, 10, "3. YESIL ENERJI VE KARBON ETKISI", ln=True, fill=True)
    pdf.ln(5)
    
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, f"Bu saat diliminde engellenen karbon salinimi:", ln=True)
    
    pdf.set_font("Arial", 'B', 20)
    pdf.set_text_color(0, 100, 0)
    pdf.cell(0, 15, f"{saved_co2:.2f} kg CO2", ln=True, align='C')
    pdf.set_text_color(0)
    
    pdf.set_font("Arial", size=10)
    pdf.ln(5)
    desc = clean_text("Eco-Stream yapay zekasi sayesinde atil kapasite kapatilmis ve gereksiz enerji tuketiminin onune gecilmistir.")
    pdf.multi_cell(0, 5, desc)
    
    return pdf.output(dest='S').encode('latin-1', 'replace')