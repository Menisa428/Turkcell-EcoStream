# ui/components.py
import streamlit as st
from core.report import generate_pdf 

def render_header(sla_score):
    sla_color = "#FFC900" if sla_score > 99.9 else "#888888"
    border_style = f"1px solid {sla_color}"
    
    st.markdown(f"""
    <div class="header-box">
        <div style="display:flex; align-items:center; justify-content:space-between;">
            <div style="display:flex; align-items:center;">
                <div style="font-size: 38px; margin-right: 15px;">📶</div>
                <div>
                    <h2 style="color:#FFFFFF; margin:0; font-weight:900; letter-spacing:1px;" translate="no">TURKCELL <span style="font-weight:300; color:#FFC900;">ECO-STREAM</span></h2>
                    <div style="color:#AAA; font-size:12px; font-family:'Arial';" translate="no">PLATINUM DIGITAL TWIN v19.0 (Audit Approved)</div>
                </div>
            </div>
            <div style="text-align:right;">
                 <div class="uptime-box" style="color:{sla_color}; border:{border_style};">SLA: %{sla_score:.4f}</div>
                 <div style="color:#666; font-size:11px; margin-top:5px;">System Reliability Monitor</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_sidebar(active_servers, total_servers, current_traffic, saved_co2, sla_score):
    with st.sidebar:
        st.header("🎛️ KONTROL PANELİ")
        
        st.subheader("📍 Senaryo Seçimi")
        scenario = st.selectbox(
            "Trafik Durumu",
            ["Normal Akış (Günlük)", "⚽ Derbi Maçı (High Traffic)", "🌙 Gece Modu (Low Traffic)", "🔥 Siber Saldırı (Load Test)"],
            index=0
        )
        
        st.markdown("---")
        live_mode = st.toggle("🔴 SİMÜLASYONU BAŞLAT", value=True)
        
        with st.expander("⚙️ Mühendislik & Maliyet"):
            data_source = st.radio("Veri Kaynağı", ["Algoritmik", "Replay"])
            decay = st.slider("Termal Gecikme (Inertia)", 0.1, 0.99, 0.90)
            # YENİ: ELEKTRİK FİYATI DEĞİŞTİRME
            elec_price = st.number_input("Elektrik Birim Fiyatı (TL/kWh)", value=4.5, step=0.1)
        
        base_traffic = 1500000 
        if "Derbi" in scenario: base_traffic = 4500000
        elif "Gece" in scenario: base_traffic = 400000
        elif "Siber" in scenario: base_traffic = 8000000 
        
        st.markdown("---")
        st.subheader("📂 Yönetici İşlemleri")
        
        pdf_bytes = generate_pdf(scenario, active_servers, total_servers, current_traffic, saved_co2, sla_score)
        
        st.download_button(
            label="📄 Günlük Raporu İndir (PDF)",
            data=pdf_bytes,
            file_name="Turkcell_EcoStream_Rapor.pdf",
            mime="application/pdf",
        )
        
        # YENİ: TAKIM İMZASI
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 11px;">
            Developed by<br>
            <strong style="color: #FFC900; font-size: 13px;">Nisa Nur Arslan</strong><br>
            <strong style="color: #FFC900; font-size: 13px;">Nisa Yanık</strong><br>
            <strong style="color: #FFC900; font-size: 13px;">Seviye Nur Gönülölmez</strong><br>
            <span style="color: #AAA; margin-top:5px; display:block;">Industrial Engineering Team</span>
            © 2026 Eco-Stream Project
        </div>
        """, unsafe_allow_html=True)
            
        return live_mode, data_source, decay, base_traffic, scenario, elec_price