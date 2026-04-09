# 🕷️ SpiderRobot

A four-legged spider robot controlled by a **Raspberry Pi 5** (high-level logic & inverse kinematics) and a **Raspberry Pi Pico 2W** (real-time servo control). The robot walks, stands up, and sits down using pre-computed gait sequences and analytical 3-DoF inverse kinematics per leg.

---

![Walking Demo](data/walking.gif)

---

## 🏗️ Hardware Overview

| Component | Role |
|---|---|
| Raspberry Pi 5 | High-level logic, inverse kinematics, web GUI, serial communication |
| Raspberry Pi Pico 2W | Real-time servo driver, IMU reading, serial command interpreter |
| 12 × Servo motors | 3 per leg (Coxa, Femur, Tibia joints) |
| MPU-6500 IMU | Onboard accelerometer + gyroscope on the Pico |

### Leg Geometry

Each of the **4 legs** has **3 degrees of freedom**:

```
Body
 │
 ├── Coxa  (60.5 mm)   — horizontal rotation at body attachment
 │    └── Femur (96.3 mm)  — vertical swing
 │         └── Tibia (113.5 mm) — knee extension to foot
```

---

## 📁 Project Structure

```
src/
├── board_py/                  # ── Raspberry Pi Pico 2W (MicroPython)
│   ├── main.py                #    Entry point: serial command loop
│   ├── servo.py               #    PWM servo abstraction
│   ├── mpu6500.py             #    IMU driver (accelerometer + gyro)
│   └── config.json            #    Servo pin & calibration config
│
└── ext/                       # ── Raspberry Pi 5 (Python 3)
    ├── main.py                #    Main control loop + web GUI server
    ├── sequences.py           #    Pre-computed gait animations (walk, stand, sit)
    ├── utils.py               #    Serial client, offsetting helpers, utilities
    └── inverse_kinematics/    #    IK library
        ├── spider_leg.py      #    Analytical 3-DoF IK solver per leg
        ├── leg_plotter.py     #    Matplotlib visualizer for leg geometry
        └── __init__.py
```

---

## ⚙️ How It Works

```
┌─────────────────────────────────────────┐
│           Raspberry Pi 5                │
│                                         │
│  sequences.py  →  IK solver  →  angles  │
│                                    │    │
│  Web GUI (browser) ←── live plot   │    │
└────────────────────────────────────┼────┘
                                     │ Serial (USB)
                              set_angles XX:XX:...:XX
                                     │
┌────────────────────────────────────▼────┐
│           Raspberry Pi Pico 2W          │
│                                         │
│  12 × Servo PWM  ←── servo[i].set_deg   │
│  MPU-6500 IMU    ──► accel / gyro data  │
└─────────────────────────────────────────┘
```

1. **Sequences** (`ext/sequences.py`) define foot-tip trajectories as lists of 4-leg positions.
2. **Inverse Kinematics** (`ext/inverse_kinematics/spider_leg.py`) converts each 3-D foot position into Coxa / Femur / Tibia joint angles.
3. **Serial protocol** — the Pi 5 sends `set_angles A0:A1:…:A11\n` over USB; the Pico replies with a JSON status including IMU data.
4. **Web GUI** streams a live matplotlib visualisation of the robot pose to any browser on the local network.

---

## 🚀 Getting Started

### Pico 2W (MicroPython)

1. Flash **MicroPython** onto the Pico 2W.
2. Copy the contents of `board_py/` to the Pico root using [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) or Thonny.
3. Edit `config.json` to match your servo GPIO pins and calibration values.
4. The Pico boots automatically and listens for serial commands.

### Raspberry Pi 5

```bash
cd src/ext
uv sync          # install dependencies from uv.lock
python main.py   # start the control loop + web server
```

Open your browser at `http://<pi5-ip>:5000` to access the Web GUI.

#### Available Commands (Web GUI)

| Command | Action |
|---|---|
| `stand_up` | Execute stand-up sequence |
| `sit_down` | Execute sit-down sequence |
| `walk` | Execute walking gait |
| `pause` | Halt current animation & hot-reload sequences |

---

## 🔌 Serial Protocol (Pico ↔ Pi 5)

**Pi 5 → Pico:**
```
set_angles A0:A1:A2:A3:A4:A5:A6:A7:A8:A9:A10:A11
reset
help
```

**Pico → Pi 5 (JSON):**
```json
{
  "angles": "set_angles 90:45:...",
  "accelerometer": [0.01, 0.02, 9.81],
  "gyroscope": [0.0, 0.1, 0.0]
}
```

---

## 🧮 Inverse Kinematics

The IK solver in `ext/inverse_kinematics/spider_leg.py` uses **analytical geometry** to solve a 3-link planar chain (Coxa → Femur → Tibia) in the leg's local frame.

Each `SpiderLeg` is instantiated with the physical link lengths:

```python
SpiderLeg("Leg1", COXA=60.5, FEMUR=96.3, TIBIA=113.5)
```

The `compute_angles(foot_position)` method returns the three joint angles ready to be sent to the Pico.

---

## 🖥️ Simulator

A [PyBullet](https://pybullet.org/) simulation is available in `simulator/` using the provided URDF model, letting you test gait sequences without physical hardware.

```bash
cd src/simulator
python hello_bullet.py
```

---

## 📦 Dependencies

### Raspberry Pi 5 (`ext/`)
- `numpy`
- `opencv-python`
- `matplotlib`
- `flask` (web GUI)

Managed via `uv` — see `ext/pyproject.toml` and `ext/uv.lock`.

### Raspberry Pi Pico 2W (`board_py/`)
- MicroPython standard libraries (`ujson`, `machine`, `select`)
- Bundled drivers: `servo.py`, `mpu6500.py`

---

## 📄 License

This project is open-source. Feel free to use, modify, and share it.
