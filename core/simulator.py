# core/simulator.py
import random
from core.logic import format_bandwidth

def generate_event(current, base):
    """Rastgele olaylar ve trafik dalgalanmaları üretir."""
    chance = random.random()
    change, msg, evt_type = 0, "", "normal"
    
    if chance < 0.05:
        change = random.randint(400000, 900000)
        msg = f"🚀 [YÜKSEK TRAFİK] Game+ Sunucu Talebi Arttı! (+{format_bandwidth(change)})"
        evt_type = "spike"
    elif chance < 0.10:
        change = random.randint(-600000, -200000)
        msg = f"📉 [NORMALİZASYON] Trafik dengeleniyor."
        evt_type = "drop"
    else:
        change = random.randint(-40000, 40000)
        
    new_val = current + change
    # Merkeze dönüş (Stabilizasyon) sağlar
    new_val += (base - new_val) * 0.15 
    if new_val < 0: new_val = 0
    
    return int(new_val), msg, evt_type