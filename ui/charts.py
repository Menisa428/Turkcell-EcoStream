# ui/charts.py
import plotly.graph_objects as go
import streamlit as st
import pandas as pd



def render_main_chart(traffic_hist, thermal_hist, pred_hist, total_capacity_kw):
    st.markdown("##### 📈 Enerji ve AI Tahmin Analizi")
    fig = go.Figure()
    
    # 1. Geleneksel Tüketim (Sabit Gri Çizgi)
    baseline = [total_capacity_kw] * len(traffic_hist)
    fig.add_trace(go.Scatter(y=baseline, mode='lines', name='Geleneksel (Eski)', 
                             line=dict(color='#444444', width=2, dash='dash')))

    # 2. Bizim Eco-Stream Tüketimi (Dolu Beyaz Alan)
    thermal_vis = [x * 20000 for x in thermal_hist]
    fig.add_trace(go.Scatter(y=thermal_vis, mode='lines', name='Eco-Stream (Bizim)', 
                             line=dict(color='#E1E1E1', width=2), fill='tonexty', fillcolor='rgba(255, 255, 255, 0.05)'))
    
    # 3. Gerçekleşen Trafik (Sarı Çizgi)
    fig.add_trace(go.Scatter(y=traffic_hist, mode='lines', name='Gerçekleşen Trafik', 
                             line=dict(color='#FFC900', width=3)))

    # 4. [YENİ] Yapay Zeka Tahmini (Kesik Mavi Çizgi)
    # Tahmin verisi bazen eksik olabilir, uzunluğu eşitleyelim
    if len(pred_hist) > 0:
        fig.add_trace(go.Scatter(y=pred_hist, mode='lines', name='AI Gelecek Tahmini', 
                                 line=dict(color='#00FFFF', width=2, dash='dot')))
    
    fig.update_layout(height=380, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor="rgba(0,0,0,0)", 
                      plot_bgcolor="rgba(255,255,255,0.05)", xaxis=dict(showgrid=False, visible=False), 
                      yaxis=dict(showgrid=True, gridcolor='#333'),
                      font=dict(color="#ddd"), legend=dict(orientation="h", y=1.1, x=0))
    st.plotly_chart(fig, use_container_width=True)

def render_pue_gauge(pue_val):
    st.markdown("##### ⚡ PUE Skor")
    fig = go.Figure(go.Indicator(
        mode = "gauge+number",
        value = pue_val,
        title = {'text': "Hedef: <1.5", 'font': {'size': 12, 'color': '#888'}},
        gauge = {
            'axis': {'range': [1.0, 2.5], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': "#FFC900"}, 
            'steps': [
                {'range': [1.0, 1.5], 'color': '#001529'}, 
                {'range': [1.5, 2.0], 'color': '#1c2e4a'}, 
                {'range': [2.0, 2.5], 'color': '#333333'}], 
            'threshold': {'line': {'color': "white", 'width': 4}, 'thickness': 0.75, 'value': 2.0}
        }
    ))
    fig.update_layout(height=250, margin=dict(l=20,r=20,t=0,b=0), paper_bgcolor="rgba(0,0,0,0)", font={'color': "white"})
    st.plotly_chart(fig, use_container_width=True)

def render_turkey_map(scenario):
    st.markdown("##### 📍 Komuta Merkezi Haritası")
    cities = ['İstanbul', 'Ankara', 'İzmir', 'Gaziantep', 'Antalya', 'Trabzon', 'Diyarbakır', 'Erzurum']
    lats = [41.0082, 39.9334, 38.4192, 37.0662, 36.8841, 41.0015, 37.9144, 39.9043]
    lons = [28.9784, 32.8597, 27.1287, 37.3833, 30.7056, 39.7178, 40.2306, 41.2679]
    sizes = [40, 25, 25, 15, 20, 15, 15, 12] 
    color_hex = "#FFC900"
    opacity_val = 0.7
    
    if "Derbi" in scenario:
        sizes = [100, 20, 20, 10, 15, 10, 10, 10]
        color_hex = "#FFFFFF" 
        opacity_val = 0.9
    elif "Gece" in scenario:
        sizes = [15, 10, 10, 5, 5, 5, 5, 5]
        color_hex = "#004488"
        opacity_val = 0.5
    elif "Siber" in scenario:
        sizes = [60, 60, 60, 60, 60, 60, 60, 60]
        color_hex = "#FFC900" 
        opacity_val = 0.8

    fig = go.Figure(go.Scattermapbox(
        lat=lats, lon=lons, mode='markers+text',
        marker=go.scattermapbox.Marker(size=sizes, color=color_hex, opacity=opacity_val, allowoverlap=True),
        text=cities, textposition="bottom center",
        textfont=dict(size=10, color="white"),
        hoverinfo='text', hovertext=[f"{c}: {s*10} Gbps" for c, s in zip(cities, sizes)]
    ))
    
    # HATA BURADAYDI, DÜZELTİLDİ:
    fig.update_layout(
        height=380, 
        margin={"r":0,"t":0,"l":0,"b":0},
        mapbox=dict(style="carto-darkmatter", center=dict(lat=39.0, lon=35.0), zoom=4.5),
        paper_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True)

def render_server_health_matrix(total_servers, load_count, buffer_count, rotation_index):
    st.markdown("##### 🧱 Veri Merkezi Dijital İkizi (Digital Twin View)")
    
    # CSS: Modern, Cyberpunk ve Profesyonel Rack Görünümü
    st.markdown("""
    <style>
        .datacenter-container {
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            justify-content: center;
            padding: 10px;
            background-color: #050505;
            border-radius: 10px;
            border: 1px solid #1c2e4a;
        }

        /* Her bir Kabin (Rack) */
        .server-rack {
            width: 45px; /* İnce uzun kabinler */
            background-color: #0e1117;
            border: 1px solid #333;
            border-top: 3px solid #FFC900; /* Platinum Sarı Şerit */
            border-radius: 4px;
            padding: 4px;
            display: flex;
            flex-direction: column;
            gap: 2px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.5);
        }
        
        /* Sunucu Ünitesi (Unit) */
        .server-unit {
            height: 6px;
            width: 100%;
            border-radius: 1px;
            position: relative;
            transition: all 0.3s ease;
        }

        /* Durum Renkleri ve Animasyonlar */
        .status-active {
            background-color: #FFC900; /* Turkcell Sarısı */
            box-shadow: 0 0 5px rgba(255, 201, 0, 0.4);
            animation: pulse-yellow 2s infinite;
        }
        
        .status-buffer {
            background-color: #FFFFFF;
            box-shadow: 0 0 4px rgba(255, 255, 255, 0.3);
            opacity: 0.8;
        }
        
        .status-idle {
            background-color: #1a1a1a;
            border: 1px solid #222;
        }

        .status-maintenance {
            background-color: #333;
            background-image: linear-gradient(45deg, #222 25%, transparent 25%, transparent 50%, #222 50%, #222 75%, transparent 75%, transparent);
            background-size: 4px 4px;
        }

        /* Nefes Alma Animasyonu (Canlı hissi verir) */
        @keyframes pulse-yellow {
            0% { opacity: 1; box-shadow: 0 0 2px #FFC900; }
            50% { opacity: 0.6; box-shadow: 0 0 8px #FFC900; }
            100% { opacity: 1; box-shadow: 0 0 2px #FFC900; }
        }

        .rack-label {
            font-size: 8px;
            color: #555;
            text-align: center;
            margin-top: 2px;
            font-family: monospace;
        }
    </style>
    """, unsafe_allow_html=True)

    # HTML Oluşturucu
    html_content = '<div class="datacenter-container">'
    
    # 150 Sunucuyu 15 Kabine (Her birinde 10 sunucu) bölüyoruz
    servers_per_rack = 10
    total_racks = total_servers // servers_per_rack
    
    total_active = load_count + buffer_count

    for rack_id in range(total_racks):
        html_content += f'<div class="server-rack" title="Rack #{rack_id+1}">'
        
        for u in range(servers_per_rack):
            # Sunucunun gerçek ID'sini hesapla
            server_global_id = (rack_id * servers_per_rack) + u
            
            # Rotasyon mantığı (Wear Leveling)
            effective_pos = (server_global_id - rotation_index) % total_servers
            
            # Durum Belirleme
            state_class = "status-idle"
            tooltip = f"Srv-{server_global_id+1}: UYKUDA"
            
            if 0 <= effective_pos < load_count:
                state_class = "status-active"
                tooltip = f"Srv-{server_global_id+1}: YÜK ALTINDA (Active)"
            elif load_count <= effective_pos < total_active:
                state_class = "status-buffer"
                tooltip = f"Srv-{server_global_id+1}: GÜVENLİK (Buffer)"
            
            # Bakım Modu (Görsel zenginlik için arada bir kapalı göster)
            if state_class == "status-idle" and (server_global_id * 7 + rotation_index) % 97 == 0:
                state_class = "status-maintenance"
                tooltip = f"Srv-{server_global_id+1}: BAKIMDA"

            html_content += f'<div class="server-unit {state_class}" title="{tooltip}"></div>'
        
        html_content += f'<div class="rack-label">R-{rack_id+1:02d}</div>'
        html_content += '</div>' # Rack bitti

    html_content += '</div>' # Container bitti
    
    st.markdown(html_content, unsafe_allow_html=True)

    # Altına Açıklama (Legend)
    st.markdown("""
    <div style="display:flex; gap:20px; justify-content:center; margin-top:10px; font-size:12px; color:#888;">
        <div style="display:flex; align-items:center; gap:5px;"><div style="width:10px; height:10px; background:#FFC900; border-radius:50%;"></div> Aktif Yük</div>
        <div style="display:flex; align-items:center; gap:5px;"><div style="width:10px; height:10px; background:#FFF; border-radius:50%; opacity:0.8;"></div> Buffer (Hazır Kıta)</div>
        <div style="display:flex; align-items:center; gap:5px;"><div style="width:10px; height:10px; background:#1a1a1a; border:1px solid #333; border-radius:50%;"></div> Uyku Modu (Eco)</div>
    </div>
    """, unsafe_allow_html=True)