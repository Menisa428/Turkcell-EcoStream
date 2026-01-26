# ui/charts.py
import plotly.graph_objects as go
import streamlit as st
import pandas as pd

def render_main_chart(traffic_hist, thermal_hist, total_capacity_kw):
    st.markdown("##### 📈 Enerji Verimliliği Karşılaştırması")
    fig = go.Figure()
    
    baseline = [total_capacity_kw] * len(traffic_hist)
    fig.add_trace(go.Scatter(y=baseline, mode='lines', name='Geleneksel Tüketim (Eski)', 
                             line=dict(color='#444444', width=2, dash='dash')))

    thermal_vis = [x * 20000 for x in thermal_hist]
    fig.add_trace(go.Scatter(y=thermal_vis, mode='lines', name='Eco-Stream Tüketim (Bizim)', 
                             line=dict(color='#E1E1E1', width=2), fill='tonexty', fillcolor='rgba(255, 255, 255, 0.05)'))
    
    fig.add_trace(go.Scatter(y=traffic_hist, mode='lines', name='Veri Trafiği', 
                             line=dict(color='#FFC900', width=3)))
    
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
    st.markdown("##### 🧱 Kabin Durumu (Wear Leveling)")
    grid_html = """
    <style>
        .rack-container {
            display: grid; grid-template-columns: repeat(20, 1fr);
            gap: 3px; padding: 10px;
            background-color: #00080F; 
            border-radius: 8px; border: 1px solid #1c2e4a;
        }
        .server-box {
            height: 10px; width: 100%; border-radius: 2px;
            transition: all 0.5s ease;
        }
        .active-load { background-color: #FFC900; box-shadow: 0 0 6px #FFC900; } 
        .active-buffer { background-color: #FFFFFF; box-shadow: 0 0 4px #FFFFFF; } 
        .idle { background-color: #0d1b2a; opacity: 0.6; }
        .maintenance { background-color: #333333; border: 1px solid #555; } 
    </style>
    <div class="rack-container">
    """
    total_active = load_count + buffer_count
    for i in range(total_servers):
        effective_pos = (i - rotation_index) % total_servers
        class_name = "idle"
        tooltip = f"ID: {i+1} | KAPALI"
        if 0 <= effective_pos < load_count:
            class_name = "active-load"
            tooltip = f"ID: {i+1} | AKTİF"
        elif load_count <= effective_pos < total_active:
            class_name = "active-buffer"
            tooltip = f"ID: {i+1} | BUFFER"
        if class_name == "idle" and (i * 7 + rotation_index) % 97 == 0:
            class_name = "maintenance"
        grid_html += f'<div class="server-box {class_name}" title="{tooltip}"></div>'
    grid_html += "</div>"
    st.markdown(grid_html, unsafe_allow_html=True)