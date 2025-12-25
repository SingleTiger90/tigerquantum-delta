use getrandom::getrandom;
use std::time::{Duration, Instant};

// Fixed-point constants (Q32.32 format — 32 bits integer part, 32 bits fractional)
// Scale: 1 << 32 = 4_294_967_296
const FIXED_SCALE: i64 = 1i64 << 32;
const PI_FIXED: i64 = 3373259426i64;     // ≈ π * 2^32
const PHI_FIXED: i64 = 6941587532i64;    // ≈ φ * 2^32 (golden ratio)
const ONE_FIXED: i64 = FIXED_SCALE;      // 1.0 in fixed-point

// Nonce refresh period (e.g., every 5 seconds — balance between security and performance)
const NONCE_EPOCH: Duration = Duration::from_secs(5);

pub struct StringState {
    nonce: u64,
    last_update: Instant,
}

impl StringState {
    pub fn new() -> Self {
        let mut state = Self {
            nonce: 0,
            last_update: Instant::now().checked_sub(Duration::from_secs(100)).unwrap(),
        };
        state.refresh_nonce();
        state
    }

    /// Updates nonce if the epoch has passed
    pub fn ensure_fresh_nonce(&mut self) {
        if self.last_update.elapsed() >= NONCE_EPOCH {
            self.refresh_nonce();
        }
    }

    /// Refresh nonce using hardware RNG
    fn refresh_nonce(&mut self) {
        let mut buf = [0u8; 8];
        // getrandom works in user-space; in eBPF, replace with rdtsc + ktime + per-cpu counter
        if getrandom(&mut buf).is_ok() {
            self.nonce = u64::from_le_bytes(buf);
        } else {
            // Fallback (rarely used)
            self.nonce = self.nonce.wrapping_add(1);
        }
        self.last_update = Instant::now();
    }

    /// Fixed-point sin approximation using Taylor series (up to 7th order) — accurate enough and fast
    /// Input: angle in fixed-point [0, 2π) → [0, 2^33)
    fn sin_fixed(mut x: i64) -> i64 {
        // Reduce to [-π, π]
        x %= 2 * PI_FIXED;
        if x > PI_FIXED {
            x -= 2 * PI_FIXED;
        }
        if x < -PI_FIXED {
            x += 2 * PI_FIXED;
        }

        // Taylor: sin(x) ≈ x - x^3/6 + x^5/120 - x^7/5040
        let x2 = (x * x) >> 32;
        let x3 = (x2 * x) >> 32;
        let x5 = (x3 * x2) >> 32;
        let x7 = (x5 * x2) >> 32;

        let term1 = x;
        let term3 = (x3 * 716861901) >> 32;     // 1/6 ≈ 0.1666666667 * 2^32
        let term5 = (x5 * 35791394) >> 32;      // 1/120 ≈ 0.0083333333 * 2^32
        let term7 = (x7 * 1429388) >> 32;        // 1/5040 ≈ 0.0001984127 * 2^32

        term1 - term3 + term5 - term7
    }

    /// Main compactification function (data folding) in fixed-point
    /// Input: array of 10 normalized attributes as i64 in [0, ONE_FIXED)
    pub fn compactify(&mut self, attributes: &[i64; 10]) -> i64 {
        self.ensure_fresh_nonce();

        let mut sum: i64 = 0;

        for (i, &a_i) in attributes.iter().enumerate() {
            // a_i + nonce (extend nonce to i64)
            let a_nonce = a_i.wrapping_add(self.nonce as i64);

            // (a_i + nonce) * π
            let scaled = (a_nonce * PI_FIXED) >> 32;

            // sin(scaled)
            let sin_val = Self::sin_fixed(scaled);

            // sin_val * φ
            let contrib = (sin_val * PHI_FIXED) >> 32;

            // Add with index for additional diffusion
            let idx_offset = ((i as i64) * 123456789i64) << 16; // scaled shift
            sum = sum.wrapping_add(contrib.wrapping_add(idx_offset));
        }

        // Final mod 1 → return fractional part
        sum.rem_euclid(ONE_FIXED)
    }
}

// Example usage in main
fn main() {
    let mut state = StringState::new();

    // Normalized packet attributes (e.g., IP, port, size etc. → [0, 1.0))
    let attrs: [i64; 10] = [
        ((0.1 * FIXED_SCALE as f64) as i64),
        ((0.23 * FIXED_SCALE as f64) as i64),
        ((0.45 * FIXED_SCALE as f64) as i64),
        ((0.67 * FIXED_SCALE as f64) as i64),
        ((0.89 * FIXED_SCALE as f64) as i64),
        ((0.12 * FIXED_SCALE as f64) as i64),
        ((0.34 * FIXED_SCALE as f64) as i64),
        ((0.56 * FIXED_SCALE as f64) as i64),
        ((0.78 * FIXED_SCALE as f64) as i64),
        ((0.90 * FIXED_SCALE as f64) as i64),
    ];

    let compact = state.compactify(&attrs);
    println!("Compact scalar (fixed-point): {}", compact);
    println!("As float: {:.10}", compact as f64 / FIXED_SCALE as f64);
}
