use std::f64::consts::PI;

/// SIMUL: The Virtual Sandbox for Entropy Projection
/// -----------------------------------------------
/// Цей модуль працює як "двійник" системи, де ми тестуємо 
/// ентропійні удари до того, як вони торкнуться LUMIS.
pub struct SimulUnit {
    projection_entropy: f64,
    stability_index: f64,
}

impl SimulUnit {
    pub fn new() -> Self {
        SimulUnit {
            projection_entropy: 0.0,
            stability_index: 1.618, // Phi-base
        }
    }

    /// Проекція удару: перевірка, чи витримає система без анігіляції
    pub fn project_impact(&mut self, impact_force: f64) -> bool {
        // Симулюємо віртуальний перегрів
        let virtual_heat = impact_force * 0.5;
        self.projection_entropy += virtual_heat;

        // Якщо в симуляції ентропія ламає Phi-стабільність — LUMIS має активувати Антитигра
        if self.projection_entropy > self.stability_index {
            self.projection_entropy *= 0.1; // Скидання симуляції
            return true; // Тривога: потрібен імпульс
        }
        false
    }

    /// Функція дзеркального моделювання (що зараз бачить ворог)
    pub fn get_decoy_state(&self) -> f64 {
        (self.projection_entropy * PI).sin().abs()
    }
}
