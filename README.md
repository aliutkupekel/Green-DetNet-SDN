# 🌿 Green-DetNet-SDN

> An SDN-based, energy-aware orchestrator for end-to-end deterministic WAN slices utilizing in-band network telemetry (INT) and Model Predictive Control (MPC).

![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)
![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![SDN](https://img.shields.io/badge/SDN-ONOS-orange.svg)
![Status](https://img.shields.io/badge/Status-Completed-success.svg)

## 📖 Overview
As 6G networks target deep sustainability, the inherent energy inefficiency of "always-on" deterministic networks (IEEE 802.1 TSN / IETF DetNet) presents a critical bottleneck. **Green-DetNet** solves this fundamental challenge by dynamically making deterministic WAN slices energy-proportional without violating strict Service Level Agreements (SLAs).

By leveraging In-band Network Telemetry and a closed-loop Model Predictive Control (MPC) algorithm, the orchestrator models the energy-versus-latency trade-off in real-time. During periods of low traffic load, it selectively transitions redundant backup paths to a sleep state, while mathematically guaranteeing that the worst-case latency budget is never exceeded.

## ✨ Key Features
- **Proactive Energy Optimization:** Dynamically toggles active network hardware based on real-time traffic loads.
- **Zero SLA Violations:** Strict mathematical constraints ensure ultra-reliable low-latency communication (URLLC) is maintained at all times.
- **MPC Engine:** Utilizes the GEKKO Optimization Suite to solve continuous non-linear trajectories and mixed-integer routing decisions.
- **Proven Efficiency:** Emulation results demonstrate a **31.25% reduction** in total daily energy consumption compared to static baselines.

## 🏗️ Architecture & Tech Stack
* **Data Plane:** Emulated multi-hop WAN using `Mininet` and `BMv2` (P4) programmable switches.
* **Control Plane:** `ONOS` / `OpenDaylight` architecture (conceptualized for dynamic rule deployment).
* **Application Plane (Orchestrator):** `Python` + `GEKKO` (MPC Optimization Engine).

## 🚀 Getting Started

### Prerequisites
- Python 3.11 or 3.12
- Windows / Linux / macOS

### Installation
1. Clone the repository:
   ```bash
   git clone [https://github.com/aliutkupekel/Green-DetNet-SDN.git](https://github.com/aliutkupekel/Green-DetNet-SDN.git)
   cd Green-DetNet-SDN

   Ali Utku Pekel
   Alperen Atalay