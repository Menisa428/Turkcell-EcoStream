# core/logic.py
import math

def format_bandwidth(mbps):
    if mbps >= 1000000: return f"{mbps/1000000:.2f} Tbps"
    elif mbps >= 1000: return f"{mbps/1000:.1f} Gbps"
    else: return f"{mbps} Mbps"

def calculate_thermal_lag(current_load_kw, prev_cooling_load, decay_factor=0.9):
    target_cooling = current_load_kw * 0.5 
    if target_cooling > prev_cooling_load:
        actual_cooling = target_cooling 
    else:
        actual_cooling = target_cooling + (prev_cooling_load - target_cooling) * decay_factor
    return actual_cooling

def calculate_sla(failed, total):
    if total == 0: return 100.0
    uptime = 100.0 - ((failed / total) * 100.0)
    return max(0.0, uptime)

def predict_traffic(history):
    if len(history) < 5: return history[-1]
    recent = history[-5:]
    weights = [0.05, 0.1, 0.2, 0.25, 0.4] 
    pred = sum([r*w for r,w in zip(recent, weights)])
    return pred * 1.05 

def calculate_carbon_impact(active_servers, total_servers, server_kw, pue):
    # Türkiye Şebeke Elektriği Karbon Çarpanı (kg CO2 / kWh)
    CO2_FACTOR_KG = 0.44 
    
    # Geleneksel (Hepsi Açık) Tüketim
    traditional_kw = total_servers * server_kw * 1.5 
    
    # Bizim (Optimize) Tüketim
    eco_kw = active_servers * server_kw * pue
    
    # Tasarruf Edilen Güç
    saved_kw = traditional_kw - eco_kw
    
    # Engellenen Karbon (kg)
    saved_co2 = saved_kw * CO2_FACTOR_KG
    
    return saved_kw, saved_co2