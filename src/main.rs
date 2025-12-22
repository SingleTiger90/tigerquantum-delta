use tokio::net::UdpSocket;
use tokio::time::{sleep, Duration};
use std::sync::{Arc, atomic::{AtomicUsize, Ordering}};
use std::collections::HashMap;
use std::sync::Mutex;
use rand::Rng;

const PHI: f64 = 1.61803398875;
const PI: f64 = 3.14159265359;
static SYSTEM_STATE: AtomicUsize = AtomicUsize::new(1); // 1: Alive, 2: Superposition (DDoS/Intrusion)

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    let socket = Arc::new(UdpSocket::bind("0.0.0.0:8888").await?);
    let attack_mass = Arc::new(Mutex::new(HashMap::<std::net::SocketAddr, Vec<String>>::new()));
    
    println!(">>> TIGER-DELTA CORE: ONLINE [432Hz Mode]");
    println!(">>> MIKORD-SHIELD: ACTIVE");

    let mut buf = [0u8; 2048];
    loop {
        let (len, addr) = socket.recv_from(&mut buf).await?;
        let data = String::from_utf8_lossy(&buf[..len]).to_string();
        let state = SYSTEM_STATE.load(Ordering::SeqCst);

        // Перевірка на валідність (Твій Маяк)
        if data.contains("PHI_PI_NOTE") && state != 2 {
            println!(">>> [RESONANCE] Valid signal from {}. Membrane transparent.", addr);
            let _ = socket.send_to(b"ACK_SYNC", addr).await;
            continue;
        }

        // --- ЛОГІКА АНТИТИГРА (Intrusion/DDoS) ---
        let mut mass_guard = attack_mass.lock().unwrap();
        let entry = mass_guard.entry(addr).or_insert(vec![]);
        entry.push(data.clone());
        let mass_size = entry.len();

        if mass_size > 5 { SYSTEM_STATE.store(2, Ordering::SeqCst); }

        // П'яний Майстер + Спіральний зсув
        let shifted_len = ((data.len() as f64 * PHI) % data.len() as f64) as usize;
        let cycled_data = format!("{}{}", &data[shifted_len..], &data[..shifted_len]);
        let pi_shots = (data.len() as f64 / PI).round() as usize % 8 + 1;
        
        let delay_ms = (PHI.powf(pi_shots as f64) * 10.0) as u64;
        
        println!(">>> [DRUNKEN_TIGER] Staggering {} ms for {}. Absorbing mass: {}", delay_ms, addr, mass_size);

        let socket_clone = socket.clone();
        let addr_clone = addr;
        let cycled_clone = cycled_data.clone();

        tokio::spawn(async move {
            sleep(Duration::from_millis(delay_ms)).await;

            // Квантовий Спін відповіді
            if rand::thread_rng().gen_bool(0.7) {
                let response = format!("DRUNK_REFLECT|{}|{}", pi_shots, cycled_clone);
                let _ = socket_clone.send_to(response.as_bytes(), addr_clone).await;
            }

            // Критична маса: Рефлекторний Меч (Mikord Protection)
            if mass_size > 15 {
                for _ in 0..3 {
                    let void_fragment: String = (0..32).map(|_| rand::thread_rng().gen_range(33..126) as u8 as char).collect();
                    let _ = socket_clone.send_to(format!("EMPTY_VOID|{}", void_fragment).as_bytes(), addr_clone).await;
                    sleep(Duration::from_millis(50)).await;
                }
            }
        });

        if mass_size > 50 { 
            println!(">>> [CRITICAL] Purging mass for {}. Reached Empty Fort state.", addr);
            entry.clear(); 
            SYSTEM_STATE.store(1, Ordering::SeqCst);
        }
    }
}
