import time
import numpy as np
import hashlib
from .resonance import TigerResonance

class TigerMind:
    """
    Головна логіка (OODA Loop).
    Використовує ентропію Шеннона для визначення хаосу.
    """
    def __init__(self):
        self.resonance = TigerResonance()
        # Поріг 40% на шкалі 0-999999 (400,000 одиниць)
        self.threshold = 400000.0 

    def _measure_entropy(self, text: str) -> float:
        """
        Фізично коректна Ентропія Шеннона з високою точністю.
        """
        if not text or not text.strip():
            return 0.000001

        freq = {}
        # Фільтруємо шум, рахуємо тільки структуру (літери)
        for char in text.lower():
            if char.isalpha():
                freq[char] = freq.get(char, 0) + 1
        
        total = sum(freq.values())
        if total == 0:
            return 0.000001

        # Векторизація
        probs = np.array(list(freq.values())) / total
        
        # Захист від log(0) через epsilon (1e-12)
        entropy = -np.sum(probs * np.log2(probs + 1e-12))
        
        max_possible = np.log2(26)
        # Нормалізація на шкалу ~1,000,000
        normalized = (entropy / max_possible) * 999999 + 0.000001
        
        return round(normalized, 6)

    def _get_stable_hash(self, text: str) -> str:
        """Створює стабільний відбиток (SHA-256)"""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def ooda_loop(self, prompt: str):
        # 1. OBSERVE
        entropy = self._measure_entropy(prompt)
        input_hash = self._get_stable_hash(prompt)

        # 2. ORIENT & DECIDE
        if entropy > self.threshold:
            # Хаос вище норми -> Пасивний контроль (Тиша)
            self.resonance.process_impulse(input_hash, entropy)
            return "..." 
        else:
            # Структура в нормі -> Дія
            self.resonance.process_impulse(input_hash, entropy)
            return f"Processed: {prompt[:50]}... [Entropy: {entropy}]"
