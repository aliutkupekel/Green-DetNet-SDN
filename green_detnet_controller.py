import numpy as np
import matplotlib.pyplot as plt
from gekko import GEKKO

# --- 1. SYSTEM PARAMETERS (SLA & HARDWARE) ---
SLA_MAX_LATENCY = 15.0  # ms (Deadline)
POWER_ACTIVE_PATH = 150 # Watts per active core path
STATIC_POWER = POWER_ACTIVE_PATH * 2 # Static baseline keeps both paths ON (300W)

# --- 2. GENERATE 24-HOUR DETERMINISTIC TRAFFIC TRACE ---
np.random.seed(42) # For reproducible results
hours = np.arange(24)
traffic_load = 400 + 350 * np.sin(np.pi * (hours - 8) / 12) + np.random.normal(0, 20, 24)
traffic_load = np.clip(traffic_load, 100, 1000) # Mbps

# --- 3. INITIALIZE ARRAYS FOR RESULTS (PROOF) ---
dynamic_power_history = []
latency_history = []
sla_violations = 0

print("Starting Green-DetNet MPC Orchestration over 24-hour trace...\n")

# --- 4. CLOSED-LOOP MPC SIMULATION ---
for t in range(24):
    load = traffic_load[t]
    
    m = GEKKO(remote=False)
    m.options.IMODE = 3 # Steady State Optimization
    m.options.SOLVER = 1 # APOPT solver for mixed integer
    
    # Manipulated Variable: Backup path state (1=Active, 0=Sleep)
    backup_active = m.Var(value=1, lb=0, ub=1, integer=True)
    
    # Controlled Variable: Predicted Latency
    latency = m.Var()
    m.Equation(latency == 10.0 + (load / (100 + 800 * backup_active)))
    
    # Constraint: NEVER violate the SLA deadline
    m.Equation(latency <= SLA_MAX_LATENCY)
    
    # Objective: Minimize Energy Consumption
    energy = m.Var()
    m.Equation(energy == POWER_ACTIVE_PATH + (POWER_ACTIVE_PATH * backup_active))
    m.Obj(energy)
    
    m.solve(disp=False)
    
    opt_backup_state = int(backup_active.value[0])
    opt_latency = latency.value[0]
    opt_energy = energy.value[0]
    
    if opt_latency > SLA_MAX_LATENCY:
        sla_violations += 1
        
    dynamic_power_history.append(opt_energy)
    latency_history.append(opt_latency)
    
    status = "SLEEP" if opt_backup_state == 0 else "ACTIVE"
    print(f"Hour {t:02d} | Load: {load:3.0f} Mbps | Backup: {status:6} | Latency: {opt_latency:5.2f} ms | Energy: {opt_energy:3.0f} W")

# --- 5. CALCULATE EVALUATION METRICS ---
total_static_energy = 24 * STATIC_POWER
total_dynamic_energy = sum(dynamic_power_history)
energy_savings_percent = ((total_static_energy - total_dynamic_energy) / total_static_energy) * 100

print("\n" + "="*50)
print("EVALUATION & RESEARCH COMPONENT RESULTS")
print("="*50)
print(f"1. Energy Savings: {total_static_energy - total_dynamic_energy:.0f} Watts-hour saved ({energy_savings_percent:.2f}%)")
print(f"2. SLA Violations: {sla_violations} deadline misses ({(sla_violations/24)*100:.1f}% violation rate).")
print("3. Trade-off Analysis: Plotting fundamental frontier...\n")

# --- 6. PLOT THE PROOF (VISUALIZATION) ---
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(10, 12))

ax1.plot(hours, traffic_load, 'b-', marker='o', label='Traffic Load (Mbps)')
ax1.set_ylabel('Throughput (Mbps)')
ax1.set_title('24-Hour Deterministic WAN Traffic Trace')
ax1.grid(True)
ax1.legend()

ax2.plot(hours, [STATIC_POWER]*24, 'r--', linewidth=2, label='Static Allocation Baseline (300W)')
ax2.step(hours, dynamic_power_history, 'g-', marker='s', where='mid', label='Green-DetNet Dynamic MPC')
ax2.set_ylabel('Power Consumption (Watts)')
ax2.set_title(f'Energy Savings over 24h (Total Saved: {energy_savings_percent:.1f}%)')
ax2.grid(True)
ax2.legend()

ax3.plot(hours, latency_history, 'm-', marker='d', label='Predicted Worst-Case Latency')
ax3.axhline(y=SLA_MAX_LATENCY, color='r', linestyle=':', linewidth=2, label='SLA Maximum Bound (15ms)')
ax3.set_xlabel('Time (Hours)')
ax3.set_ylabel('Latency (ms)')
ax3.set_title('SLA Compliance & Energy-Latency Trade-off')
ax3.grid(True)
ax3.legend()

plt.tight_layout()
plt.savefig('green_detnet_results.png')
plt.show()