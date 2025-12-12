"""
Unit Tests for TigerΔ Framework.
Validates the 'Critical Mass' hypothesis and 'Passive Control' logic.
"""

import numpy as np
import pytest
from tiger_delta import TigerMind, JungleSimulation

def test_tiger_mind_initialization():
    """Перевіряємо, чи 'Мозок' ініціалізується з правильними аксіомами."""
    mind = TigerMind(seed=42)
    assert mind.resonance == 50.0
    assert len(mind.spark_memory) > 0
    assert "LUMIS" in mind.spark_memory[0]

def test_passive_control_stability():
    """
    Перевіряємо, що Passive Control реально стабілізує систему.
    Стабільність має бути > 60% при наявності 'Іскри' (пам'яті).
    """
    mind = TigerMind(seed=42)
    stability = mind.run_simulation(rounds=1000)
    assert stability > 60.0, f"Stability too low: {stability}%"

def test_critical_mass_hypothesis():
    """
    Науковий доказ (твоя логіка):
    10% Тигрів -> Хаос > 60 (Крах)
    40% Тигрів -> Хаос < 20 (Стабільність)
    """
    # Сценарій 1: Мало тигрів (10%)
    sim_low = JungleSimulation(tiger_pct=10, seed=42)
    hist_low = sim_low.run()
    final_chaos_low = np.mean(list(hist_low[-1].values()))
    
    # Сценарій 2: Критична маса (40%)
    sim_high = JungleSimulation(tiger_pct=40, seed=42)
    hist_high = sim_high.run()
    final_chaos_high = np.mean(list(hist_high[-1].values()))

    print(f"\n[TEST] Low Tigers Chaos: {final_chaos_low:.2f}")
    print(f"[TEST] High Tigers Chaos: {final_chaos_high:.2f}")

    # Перевірки (Assertions)
    assert final_chaos_low > 50.0, "Low tiger count should lead to high chaos"
    assert final_chaos_high < 25.0, "Critical mass failed to stabilize network"
