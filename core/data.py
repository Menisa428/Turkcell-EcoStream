# core/data.py
import random
import time
import numpy as np
from datetime import datetime

def get_traffic_data(mode, base_traffic):
    """
    Seçilen moda göre (Canlı Mock veya Replay) trafik verisi üretir.
    """
    noise = random.uniform(0.98, 1.02)
    
    if mode == "Canlı API (Mock)":
        # Güncel saate göre yoğunluk (Gamer Pattern)
        now = datetime.now()
        hour_factor = {
            0: 0.8, 1: 0.6, 2: 0.4, 3: 0.3, 4: 0.25, 5: 0.3, 
            6: 0.4, 7: 0.6, 8: 0.9, 9: 1.0, 10: 1.1, 11: 1.2,
            12: 1.3, 13: 1.4, 14: 1.4, 15: 1.5, 16: 1.7, 17: 1.9,
            18: 2.1, 19: 2.4, 20: 2.6, 21: 2.5, 22: 2.2, 23: 1.8
        }
        val = base_traffic * hour_factor.get(now.hour, 1.0) * noise
        return int(val)
        
    elif mode == "Geçmiş Veri Tekrarı (Replay)":
        # Sinus dalgası simülasyonu
        t = time.time()
        val = base_traffic + (base_traffic * 0.4 * np.sin(t / 5)) 
        return int(val * noise)
    
    return base_traffic