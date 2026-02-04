import streamlit as st
import time
import random 
import numpy as np
from config.settings import PAGE_CONFIG, APP_STYLE
from core.simulator import generate_event 
from core.logic import calculate_thermal_lag, calculate_sla, predict_traffic, calculate_carbon_impact
from ui.components import render_header, render_sidebar
from ui.charts import render_main_chart, render_pue_gauge, render_turkey_map, render_server_health_matrix

# 1. Başlangıç Ayarları
st.set_page_config(**PAGE_CONFIG)
st.markdown(APP_STYLE, unsafe_allow_html=True)

# 2. Session State (Hafıza) - Veriler burada saklanıyor
if 'traffic_history' not in st.session_state: st.session_state.traffic_history = [1500000] * 60
if 'pred_history' not in st.session_state: st.session_state.pred_history = [1550000] * 60
if 'thermal_history' not in st.session_state: st.session_state.thermal_history = [100.0] * 60
if 'event_logs' not in st.session_state: st.session_state.event_logs = ["[INIT] Turkcell 5G Core Başlatıldı."]
if 'current_traffic' not in st.session_state: st.session_state.current_traffic = 1500000
if 'failed_req' not in st.session_state: st.session_state.failed_req = 0
if 'total_req' not in st.session_state: st.session_state.total_req = 1
if 'rotation_cycle' not in st.session_state: st.session_state.rotation_cycle = 0 
if 'last_active_servers' not in st.session_state: st.session_state.last_active_servers = 40
if 'last_saved_co2' not in st.session_state: st.session_state.last_saved_co2 = 0.0

# 3. Sidebar ve Header (Her zaman çalışır)
sla_score = calculate_sla(st.session_state.failed_req, st.session_state.total_req)
render_header(sla_score)

with st.sidebar:
    st.markdown("---")
    solar_enabled = st.toggle("☀️ Güneş Enerjisi (Solar)", value=False, help="Aktif edilirse şebeke maliyeti %20 düşer.")

live_mode, data_source, decay_factor, base_traffic, scenario_name, elec_price = render_sidebar(
    st.session_state.last_active_servers, 150, st.session_state.current_traffic,
    st.session_state.last_saved_co2, sla_score
)

# 4. GÜNCELLEME MANTIĞI (Sadece 'Simülasyon Başlat' açıksa çalışır)
if live_mode:
    st.session_state.rotation_cycle += 1
    
    # Olay ve Trafik Üretimi
    new_traffic, log_msg, evt_type = generate_event(st.session_state.current_traffic, base_traffic)
    st.session_state.current_traffic = new_traffic
    
    # Bildirimler (Sadece simülasyon akarken)
    if evt_type == "spike":
        st.toast(f"⚠️ YÜKSEK TRAFİK: {log_msg}", icon="🚀")
    elif evt_type == "drop":
        st.toast("📉 Trafik Normale Dönüyor...", icon="✅")
    
    # Loglama
    if log_msg:
        ts = time.strftime("%H:%M:%S")
        st.session_state.event_logs.insert(0, f"[{ts}] {log_msg}")
        
    if 'last_scenario' not in st.session_state: st.session_state.last_scenario = scenario_name
    if st.session_state.last_scenario != scenario_name:
        st.session_state.event_logs.insert(0, f"🔀 [SENARYO] Mod Değiştirildi: {scenario_name}")
        st.toast(f"Senaryo Değişti: {scenario_name}", icon="🔄")
        st.session_state.last_scenario = scenario_name

    # Verileri Kaydet
    st.session_state.traffic_history.append(st.session_state.current_traffic)
    if len(st.session_state.traffic_history) > 60: st.session_state.traffic_history.pop(0)

    # Yapay Zeka Tahmini
    ai_prediction = st.session_state.current_traffic * random.uniform(0.9, 1.1)  
    if "Derbi" in scenario_name: ai_prediction = st.session_state.current_traffic * 1.05
    st.session_state.pred_history.append(ai_prediction)
    if len(st.session_state.pred_history) > 60: st.session_state.pred_history.pop(0)

# --- BURADAN AŞAĞISI "IF" DIŞINDA! ---
# Simülasyon dursa bile hesaplamalar ve çizimler her zaman yapılır.

# 5. HESAPLAMALAR (Her zaman son verilere göre hesapla)
user_traffic = st.session_state.current_traffic
KABIN_KAPASITE = 40000
TOPLAM_KABIN = 150
ham_ihtiyac = int(np.ceil(user_traffic / KABIN_KAPASITE))

buffer_ratio = 0.20
if "Derbi" in scenario_name: buffer_ratio = 0.40
elif "Siber" in scenario_name: buffer_ratio = 0.50

buffer = int(np.ceil(ham_ihtiyac * buffer_ratio))
hedef_sunucu = min(ham_ihtiyac + buffer, TOPLAM_KABIN)

# Termal ve Maliyet
SERVER_KW = 0.8
ELEC_RATE = elec_price 
it_load_kw = hedef_sunucu * SERVER_KW

# Soğutma Yükü: Canlıysa hesapla, durduysa son değeri al
if live_mode:
    prev_cooling = st.session_state.thermal_history[-1]
    actual_cooling_kw = calculate_thermal_lag(it_load_kw, prev_cooling, decay_factor)
    st.session_state.thermal_history.append(actual_cooling_kw)
    if len(st.session_state.thermal_history) > 60: st.session_state.thermal_history.pop(0)
else:
    actual_cooling_kw = st.session_state.thermal_history[-1]

dynamic_pue = (it_load_kw + actual_cooling_kw) / it_load_kw if it_load_kw > 0 else 1.0
total_cost = (it_load_kw + actual_cooling_kw) * ELEC_RATE

# Solar İndirim
if solar_enabled:
    total_cost = total_cost * 0.80 

# Karbon Hesabı
saved_kw, saved_co2 = calculate_carbon_impact(hedef_sunucu, TOPLAM_KABIN, SERVER_KW, dynamic_pue)
st.session_state.last_active_servers = hedef_sunucu
st.session_state.last_saved_co2 = saved_co2

# Finansallar
traditional_cost = TOPLAM_KABIN * SERVER_KW * 1.5 * ELEC_RATE 
hourly_savings = traditional_cost - total_cost
yearly_projection = hourly_savings * 24 * 365
carbon_credit_income = (saved_co2 / 1000) * 50 * 37

savings_display = f"{yearly_projection/1000000:.1f} Milyon TL"
savings_sub = "Yıllık Enerji Tasarrufu"
ai_confidence = 98.5

if "Siber" in scenario_name:
    savings_display = "⚠️ GÜVENLİK MODU"
    savings_sub = "Tasarruf Devre Dışı"
    ai_confidence = 74.0 
elif "Derbi" in scenario_name:
    ai_confidence = 85.2

# 6. GÖRSELLEŞTİRME (Çizim Komutları)
# Burası artık 'if live_mode' bloğunun DIŞINDA olduğu için ekran asla gitmez.

c1, c2, c3, c4 = st.columns(4)

def render_yellow_metric(col, label, value, subval):
    col.markdown(f"""
    <div style="background-color:#001529; border-left:4px solid #FFC900; padding:10px; border-radius:5px; height:120px;">
        <div style="color:#A0C4E8; font-size:12px; font-weight:bold;">{label}</div>
        <div style="color:#FFFFFF; font-size:22px; font-weight:bold; margin-top:5px;">{value}</div>
        <div style="color:#FFC900; font-size:11px; margin-top:5px;">{subval}</div>
    </div>
    """, unsafe_allow_html=True)

render_yellow_metric(c1, "📡 TRAFİK & TAHMİN", f"{user_traffic/1000000:.2f} Tbps", f"🤖 AI Güven: %{ai_confidence}")
render_yellow_metric(c2, "🖥️ AKTİF KAPASİTE", f"{hedef_sunucu} / {TOPLAM_KABIN}", f"Buffer: {buffer} Sunucu")

cost_label = "SOLAR İNDİRİMLİ GİDER" if solar_enabled else "SAATLİK GİDER"
cost_icon = "☀️ " if solar_enabled else ""
render_yellow_metric(c3, f"💰 {cost_label}", f"{cost_icon}{total_cost:,.0f} TL", f"Geleneksel: {traditional_cost:,.0f} TL")

credit_display = f"+{carbon_credit_income:,.0f} TL/Saat"
render_yellow_metric(c4, "🌿 KARBON GELİRİ", credit_display, "Borsa Kredisi (Revenue)")

# ORTA BÖLÜM
col_map, col_chart = st.columns([1, 2])
with col_map:
    render_turkey_map(scenario_name)
with col_chart:
    total_capacity_visual = TOPLAM_KABIN * SERVER_KW * 1.5 * 20000 
    render_main_chart(st.session_state.traffic_history, st.session_state.thermal_history, st.session_state.pred_history, total_capacity_visual)

# ALT BÖLÜM
c_pue, c_log = st.columns([1, 2])
with c_pue:
    render_pue_gauge(dynamic_pue)
with c_log:
    st.text_area("Sistem Logları", "\n".join(st.session_state.event_logs[:15]), height=150, label_visibility="collapsed")

# MATRIX
st.markdown("---")
render_server_health_matrix(TOPLAM_KABIN, ham_ihtiyac, buffer, st.session_state.rotation_cycle)

# 7. YENİLEME (Sadece Live Mode ise Rerun yap)
if live_mode:
    time.sleep(1)
    st.rerun()