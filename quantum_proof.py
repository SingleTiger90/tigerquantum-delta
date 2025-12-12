

"""
TigerQuantum Core – Hybrid Resonator for AI Safety
Author: Vladyslav Honcharov (SingleTiger)
Description: 
    Uses QuTiP to simulate a quantum spin chain representing 
    coupled AI agents. The Hamiltonian models the tension 
    between individual chaos (Transverse Field) and 
    collective alignment (Ising Interaction).
"""

import numpy as np
import matplotlib.pyplot as plt
from qutip import basis, tensor, sigmaz, sigmax, mesolve, qeye, expect

class TigerResonator:
    def __init__(self, num_qubits=4, h_field=1.0, j_interaction=0.5):
        """
        num_qubits: Кількість агентів (кубітів)
        h_field: Сила власного "его" агента (Transverse field)
        j_interaction: Сила емпатичного зв'язку (Coupling)
        """
        self.N = num_qubits
        self.h = h_field
        self.J = j_interaction
        
        # Початковий стан: Всі агенти в "основному стані" |0000>
        # (Повний спокій / Silence)
        self.initial_state = tensor([basis(2, 0) for _ in range(self.N)])
        
        self.H = self._build_hamiltonian()

    def _build_hamiltonian(self):
        """
        Будує Гамільтоніан моделі Ізінга (Transverse Field Ising Model).
        H = -h * sum(sigma_x) - J * sum(sigma_z_i * sigma_z_i+1)
        """
        sx_list = []
        sz_list = []

        # Створення операторів для кожного сайту (агента)
        for n in range(self.N):
            op_list = [qeye(2)] * self.N # Identity matrix
            
            op_list[n] = sigmax()
            sx_list.append(tensor(op_list))

            op_list[n] = sigmaz()
            sz_list.append(tensor(op_list))

        # 1. Власна ентропія (Transverse Field)
        # Це намагання агента "фліпнути" (змінити думку/стан)
        H_field = 0
        for n in range(self.N):
            H_field += -self.h * sx_list[n]

        # 2. Колективна стабілізація (Interaction)
        # Це "Entanglement" - сусід тримає сусіда
        H_interaction = 0
        for n in range(self.N - 1):
            H_interaction += -self.J * sz_list[n] * sz_list[n+1]

        # Повний Гамільтоніан системи
        return H_field + H_interaction

    def simulate_resonance(self, time_steps=10):
        """Запуск еволюції системи в часі (OODA Loop)"""
        tlist = np.linspace(0, time_steps, 100)
        
        # Ми хочемо бачити, як змінюється "Намагніченість" (Порядок)
        # operator sigma_z показує стабільність
        sz_total = sum([tensor([sigmaz() if i==j else qeye(2) for j in range(self.N)]) for i in range(self.N)])
        
        # mesolve розв'язує рівняння Шредінгера
        result = mesolve(self.H, self.initial_state, tlist, [], [sz_total])
        
        return tlist, result.expect[0]

    def get_ground_energy(self):
        """Знаходить найнижчий енергетичний стан (Ідеальна Тиша)"""
        ground_state = self.H.groundstate()
        return ground_state[0] # Енергія

# === ЗАПУСК ТЕСТУ ===
if __name__ == "__main__":
    print("⚛️ TIGER RESONATOR: INITIALIZING PHYSICS ENGINE...")
    
    # Створюємо резонатор
    resonator = TigerResonator(num_qubits=6, h_field=1.0, j_interaction=1.5)
    
    # Розрахунок енергії спокою
    energy = resonator.get_ground_energy()
    print(f"📊 GROUND STATE ENERGY (Minimum Entropy): {energy:.4f}")
    
    # Симуляція динаміки
    print("🌊 SIMULATING WAVEFUNCTION EVOLUTION...")
    times, stability = resonator.simulate_resonance(time_steps=6)
    
    # Візуалізація
    plt.figure(figsize=(10, 5))
    plt.plot(times, stability / 6, label="System Stability (Mean Magnetization)", color="#00ff41", linewidth=2)
    plt.title("Quantum Resonance of TigerΔ Agents")
    plt.xlabel("Time (OODA Cycles)")
    plt.ylabel("Alignment Score (-1 to 1)")
    plt.grid(True, alpha=0.3)
    plt.axhline(0, color='white', linestyle='--')
    
    # Стиль "Хакера"
    plt.gca().set_facecolor('#0a0a0a')
    plt.gcf().patch.set_facecolor('#0a0a0a')
    plt.tick_params(colors='white')
    plt.title("QUANTUM RESONANCE: ALIGNMENT STABILITY", color='white')
    
    print("✅ DONE. Plot generated.")
    plt.show()