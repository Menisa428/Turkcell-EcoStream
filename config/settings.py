# config/settings.py

PAGE_CONFIG = {
    "page_title": "Turkcell Platinum Operations",
    "page_icon": "📶",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# TURKCELL PLATINUM - SADECE SARI VE LACİVERT
APP_STYLE = """
<style>
    /* Ana Arka Plan: Koyu Gece Mavisi */
    .stApp { background-color: #000B14; color: #FFFFFF; }
    
    /* Header: Koyu Mavi Gradient ve Sarı Çizgi */
    .header-box {
        background: linear-gradient(90deg, #001529 0%, #000000 100%);
        padding: 20px; border-radius: 12px; 
        border-bottom: 4px solid #FFC900; 
        margin-bottom: 20px;
        box-shadow: 0 0 25px rgba(255, 201, 0, 0.15);
    }
    
    /* Kartlar */
    div[data-testid="stMetric"] {
        background-color: #001222; 
        border: 1px solid #1c2e4a;
        border-left: 5px solid #FFC900;
        padding: 15px; border-radius: 8px;
    }
    label[data-testid="stMetricLabel"] { color: #A0C4E8 !important; font-weight: bold; }
    div[data-testid="stMetricValue"] { color: #FFFFFF !important; font-family: 'Consolas', monospace; }
    
    /* Sidebar */
    section[data-testid="stSidebar"] { background-color: #00080F; border-right: 1px solid #1c2e4a; }
    
    /* Log Ekranı */
    .log-window {
        font-family: 'Consolas', monospace; font-size: 11px;
        background-color: #000000; color: #FFC900;
        padding: 10px; border: 1px solid #333; height: 300px; overflow-y: auto;
    }
    
    /* SLA Kutusu (Artık Kırmızı Yok, Gri var) */
    .uptime-box {
        font-family: 'Arial', sans-serif;
        color: #FFC900; font-weight: bold; font-size: 18px;
        border: 1px solid #FFC900; padding: 5px 15px; border-radius: 20px;
        background: rgba(255, 201, 0, 0.05);
        display: inline-block;
    }
    .fail-box { color: #888; border-color: #888; } /* Hata durumunda Gri olur */
    
    .map-container { border: 1px solid #333; padding: 5px; border-radius: 10px; }
</style>
"""