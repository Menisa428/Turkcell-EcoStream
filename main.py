# main.py
import streamlit as st
import time
import numpy as np
from config.settings import PAGE_CONFIG, APP_STYLE
from core.data import get_traffic_data
from core.logic import calculate_thermal_lag, calculate_sla, predict_traffic, calculate_carbon_impact
from ui.components import render_header, render_sidebar
from ui.charts import render_main_chart, render_pue_gauge, render_turkey_map, render_server_health_matrix

# 1. Başlangıç
st.set_page_config(**PAGE_CONFIG)
st.markdown(APP_STYLE, unsafe_allow_html=True)

# 2. Session State
if 'traffic_history' not in st.session_state: st.session_state.traffic_history = [1500000] * 60
if 'thermal_history' not in st.session_state: st.session_state.thermal_history = [100.0] * 60
if 'event_logs' not in st.session_state: st.session_state.event_logs = ["[INIT] Turkcell 5G Core Başlatıldı."]
if 'current_traffic' not in st.session_state: st.session_state.current_traffic = 1500000
if 'failed_req' not in st.session_state: st.session_state.failed_req = 0
if 'total_req' not in st.session_state: st.session_state.total_req = 1
if 'rotation_cycle' not in st.session_state: st.session_state.rotation_cycle = 0 
if 'last_active_servers' not in st.session_state: st.session_state.last_active_servers = 40
if 'last_saved_co2' not in st.session_state: st.session_state.last_saved_co2 = 0.0

sla_score = calculate_sla(st.session_state.failed_req, st.session_state.total_req)
render_header(sla_score)

# SIDEBAR (Artık 6 değer dönüyor: elec_price eklendi)
live_mode, data_source, decay_factor, base_traffic, scenario_name, elec_price = render_sidebar(
    st.session_state.last_active_servers, 150, st.session_state.current_traffic,
    st.session_state.last_saved_co2, sla_score
)

if live_mode:
    st.session_state.rotation_cycle += 1
    new_traffic = get_traffic_data(data_source, base_traffic)
    if "Derbi" in scenario_name: new_traffic += np.random.randint(-200000, 200000)
    st.session_state.current_traffic = new_traffic
    
    if 'last_scenario' not in st.session_state: st.session_state.last_scenario = scenario_name
    if st.session_state.last_scenario != scenario_name:
        st.session_state.event_logs.insert(0, f"🔀 [SENARYO] Mod Değiştirildi: {scenario_name}")
        st.session_state.last_scenario = scenario_name

user_traffic = st.session_state.current_traffic
pred_traffic = predict_traffic(st.session_state.traffic_history)
st.session_state.traffic_history.append(user_traffic)
if len(st.session_state.traffic_history) > 60: st.session_state.traffic_history.pop(0)

# Kapasite Hesapları
KABIN_KAPASITE = 40000
TOPLAM_KABIN = 150
ham_ihtiyac = int(np.ceil(user_traffic / KABIN_KAPASITE))
buffer_ratio = 0.20
if "Derbi" in scenario_name: buffer_ratio = 0.40
buffer = int(np.ceil(ham_ihtiyac * buffer_ratio))
hedef_sunucu = min(ham_ihtiyac + buffer, TOPLAM_KABIN)

# Termal ve Maliyet
SERVER_KW = 0.8
ELEC_RATE = elec_price # Sidebar'dan gelen dinamik fiyatı kullanıyoruz
it_load_kw = hedef_sunucu * SERVER_KW
prev_cooling = st.session_state.thermal_history[-1]
actual_cooling_kw = calculate_thermal_lag(it_load_kw, prev_cooling, decay_factor)
st.session_state.thermal_history.append(actual_cooling_kw)
if len(st.session_state.thermal_history) > 60: st.session_state.thermal_history.pop(0)

dynamic_pue = (it_load_kw + actual_cooling_kw) / it_load_kw if it_load_kw > 0 else 1.0
total_cost = (it_load_kw + actual_cooling_kw) * ELEC_RATE

# Karbon Hesabı
saved_kw, saved_co2 = calculate_carbon_impact(hedef_sunucu, TOPLAM_KABIN, SERVER_KW, dynamic_pue)
st.session_state.last_active_servers = hedef_sunucu
st.session_state.last_saved_co2 = saved_co2

# --- SİBER SALDIRI MANTIĞI & PROJEKSİYON ---
# Geleneksel sistemin maliyeti (Baseline)
traditional_cost = TOPLAM_KABIN * SERVER_KW * 1.5 * ELEC_RATE 
hourly_savings = traditional_cost - total_cost
yearly_projection = hourly_savings * 24 * 365

# Eğer Siber Saldırı varsa, Tasarruf yoktur, Güvenlik vardır.
savings_display = f"{yearly_projection/1000000:.1f} Milyon TL"
savings_sub = "2026 Projeksiyonu"
ai_confidence = 98.5

if "Siber" in scenario_name:
    savings_display = "⚠️ GÜVENLİK MODU"
    savings_sub = "Tasarruf Devre Dışı"
    ai_confidence = 74.0 # Saldırıda güven düşer
    st.session_state.event_logs.insert(0, f"🛡️ [DDOS KORUMA] Kapasite artırıldı, tasarruf önemsenmiyor.")
elif "Derbi" in scenario_name:
    ai_confidence = 85.2

# 5. DASHBOARD (YENİ DÜZEN)
c1, c2, c3, c4 = st.columns(4)

def render_yellow_metric(col, label, value, subval):
    col.markdown(f"""
    <div style="background-color:#001529; border-left:4px solid #FFC900; padding:10px; border-radius:5px; height:120px;">
        <div style="color:#A0C4E8; font-size:12px; font-weight:bold;">{label}</div>
        <div style="color:#FFFFFF; font-size:22px; font-weight:bold; margin-top:5px;">{value}</div>
        <div style="color:#FFC900; font-size:11px; margin-top:5px;">{subval}</div>
    </div>
    """, unsafe_allow_html=True)

render_yellow_metric(c1, "📡 TRAFİK & GÜVEN", f"{user_traffic/1000000:.2f} Tbps", f"🤖 AI Güven: %{ai_confidence}")
render_yellow_metric(c2, "🖥️ AKTİF KAPASİTE", f"{hedef_sunucu} / {TOPLAM_KABIN}", f"Buffer: {buffer} Sunucu")
render_yellow_metric(c3, "💰 SAATLİK GİDER", f"{total_cost:,.0f} TL", f"Geleneksel: {traditional_cost:,.0f} TL")
render_yellow_metric(c4, "🚀 YILLIK HEDEF", savings_display, savings_sub)

# YENİ ORTA BÖLÜM: HARİTA VE GRAFİK YAN YANA
col_map, col_chart = st.columns([1, 2])

with col_map:
    render_turkey_map(scenario_name)

with col_chart:
    # Baseline için Toplam Kapasite Enerjisini gönderiyoruz (Grafik referansı için)
    total_capacity_visual = TOPLAM_KABIN * SERVER_KW * 1.5 * 20000 
    render_main_chart(st.session_state.traffic_history, st.session_state.thermal_history, total_capacity_visual)

# ALT BÖLÜM: PUE, LOG, MATRIX
c_pue, c_log = st.columns([1, 2])
with c_pue:
    render_pue_gauge(dynamic_pue)
with c_log:
    with st.expander("📟 Sistem Olay Günlüğü", expanded=True):
        st.text_area("", "\n".join(st.session_state.event_logs[:15]), height=150)

# EN ALT: MATRIX
st.markdown("---")
render_server_health_matrix(TOPLAM_KABIN, ham_ihtiyac, buffer, st.session_state.rotation_cycle)

if live_mode:
    time.sleep(1)
    st.rerun()