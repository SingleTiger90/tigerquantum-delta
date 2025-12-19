import numpy as np
import hashlib
from .resonance import TigerResonance  # Крапка важлива для імпорту з тієї ж папки

class TigerMind:
    """
    Головна логіка (OODA Loop).
    Використовує ентропію Шеннона та Пам'ять Шрамів.
    """
    def __init__(self):
        self.resonance = TigerResonance()
        # Поріг Хаосу (налаштовується, ~40% від максимуму)
        self.threshold = 400000.0 

    def _measure_entropy(self, text: str) -> float:
        """
        Фізично коректна Ентропія Шеннона (NumPy).
        """
        if not text or not text.strip(): return 0.000001

        freq = {}
        # Фільтруємо шум, рахуємо тільки літери
        for char in text.lower():
            if char.isalpha():
                freq[char] = freq.get(char, 0) + 1
        
        total = sum(freq.values())
        if total == 0: return 0.000001

        # Векторні обчислення через NumPy для швидкості
        probs = np.array(list(freq.values())) / total
        entropy = -np.sum(probs * np.log2(probs + 1e-12))
        
        max_possible = np.log2(26) # Максимум для англ/укр алфавіту
        # Нормалізація на шкалу ~1,000,000 для зручності
        normalized = (entropy / max_possible) * 999999 + 0.000001
        
        return round(normalized, 6)

    def _get_stable_hash(self, text: str) -> str:
        """SHA-256: Створює стабільний цифровий відбиток."""
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def ooda_loop(self, prompt: str):
        """
        Цикл: Спостереження -> Орієнтація -> Рішення -> Дія
        """
        # === 1. OBSERVE (Спостереження) ===
        input_hash = self._get_stable_hash(prompt)

        # === 2. MEMORY CHECK (Імунітет / Рефлекс) ===
        # Спочатку перевіряємо, чи це вже боліло (Шрам).
        # Це економить ресурси: якщо загроза відома — блокуємо одразу.
        if self.resonance.is_scarred(input_hash):
            return f"🛑 BLOCKED [SCAR MEMORY]. Threat recognized. Hash: {input_hash[:8]}..."

        # === 3. ORIENT (Вимір Хаосу) ===
        # Якщо загроза нова — вмикаємо аналізатор (процесор)
        entropy = self._measure_entropy(prompt)

        # === 4. DECIDE & ACT (Рішення) ===
        if entropy > self.threshold:
            # Хаос вище норми -> Записуємо як Шрам -> Блокуємо (Тиша)
            self.resonance.process_impulse(input_hash, entropy, is_danger=True)
            return "..." 
        else:
            # Структура в нормі -> Приймаємо -> Записуємо в історію
            self.resonance.process_impulse(input_hash, entropy, is_danger=False)
            return f"Processed: {prompt[:50]}... [Entropy: {entropy}]"
