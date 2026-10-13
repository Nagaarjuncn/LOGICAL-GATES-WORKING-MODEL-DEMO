# LogicGate Studio 2D

A high-fidelity, interactive **2D Logic Gate Simulator & Schematic Diagram Studio** featuring animated circuit diagrams, electromechanical switch models, digital timing waveforms, and a dual-engine **Python & C++** calculation backend.

![Status](https://img.shields.io/badge/Status-Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.x-blue?logo=python)
![C++](https://img.shields.io/badge/C++-11%2B-00599C?logo=c%2B%2B)
![Frontend](https://img.shields.io/badge/Frontend-HTML5%20%2F%20SVG%20%2F%20Canvas-orange)

---

## 🌟 Key Features

### 1. Complete IEEE 315 Logic Gate Library
Supports all 7 fundamental digital logic gates with standard IEEE 315 vector glyphs:
- **AND** (`A · B`)
- **OR** (`A + B`)
- **XOR** (`A ⊕ B`)
- **NOT** (`¬A`) — *Automatically adapts UI for single-input operation*
- **NAND** (`¬(A · B)`)
- **NOR** (`¬(A + B)`)
- **XNOR** (`¬(A ⊕ B)`)

### 2. Multi-Mode 2D Circuit Visualizations
Switch between three dedicated visual diagnostic perspectives:
- **2D Logic Schematic**: Vector SVG schematic featuring signal glow effects, color-coded voltage states (LOW: 0V vs. HIGH: 5V), an animated LED dome with realistic glow and ray bursts, and a Canvas particle system simulating electron flow through active signal paths.
- **2D Switch Circuit**: Physical electromechanical/transistor switch model rendered on HTML5 Canvas showing series, parallel, and inverted circuit loops with real-time open/closed loop detection.
- **2D Timing Waveform**: Real-time oscilloscope-style digital logic timing diagram scanning inputs `A`, `B`, and output `Q` across time with clock-synchronized transitions.

### 3. Interactive Inputs & Dynamic Truth Table
- Clickable toggle switches for Input Terminals A and B with instant logic level & voltage readouts.
- Real-time truth table generation highlighting the active state row.
- **Click-to-Test**: Click any row in the truth table to immediately set input states.

### 4. Calculation Pipeline & Audio Feedback
- Visual dataflow diagram breaking down inputs, boolean formulas, and results.
- Optional Web Audio API synthetic feedback clicks upon signal toggling.
- Simulation speed adjustments (0.5x Slow-Mo, 1.0x Normal, 2.0x Fast).

### 5. Dual-Engine Hybrid Architecture (C++ & Python)
- **C++ Native Engine**: Bitwise boolean logic exported with C linkage (`extern "C"`) in a compiled shared library (`.dll` on Windows / `.so` on Linux/macOS).
- **Python HTTP Middleware**: Lightweight server using Python's standard library (`http.server`, `socketserver`, `ctypes`) that loads the compiled C++ library with zero external pip dependencies.
- **Resilient Fallback**: Automatically falls back to Python's internal logic engine if the compiled C++ library is not found.

---

## 📁 Project Architecture

```
2d mini pro log gate/
├── app.py          # HTTP server, REST API (/calculate), and ctypes C++ loader
├── logic.cpp       # Portable C++ logic implementation (AND, OR, XOR, NOT, NAND, NOR, XNOR)
├── index.html      # Comprehensive single-page UI with SVG schematic, Canvas rendering & controls
└── README.md       # Project documentation
```

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.8+** (uses only standard library modules: `http.server`, `ctypes`, `json`, `os`, `socketserver`)
- *(Optional)* A C++ compiler (such as **g++**, **clang++**, or **MSVC**) if you want to compile the native C++ library.

---

### Step 1: (Optional) Compile the C++ Library

The Python server will run immediately even without compiling C++ by using its built-in fallback. To leverage native C++ performance:

#### Windows (MinGW / GCC):
```powershell
g++ -O3 -shared -o logic.dll logic.cpp
```

#### Windows (MSVC Developer Command Prompt):
```cmd
cl /O2 /LD logic.cpp /Fe:logic.dll
```

#### Linux / macOS (GCC / Clang):
```bash
g++ -O3 -shared -fPIC -o logic.so logic.cpp
```

---

### Step 2: Start the Web Server

Run the Python backend:

```bash
python app.py
```

The server will initialize on port **8000**:
```
Server running at http://localhost:8000
```

---

### Step 3: Launch the Studio

Open your browser and navigate to:
```
http://localhost:8000
```

> **Note**: You can also open [index.html](file:///c:/Users/admin/Documents/2d%20mini%20pro%20log%20gate/index.html) directly in any modern web browser. The frontend gracefully detects whether the backend server is reachable.

---

## 🔌 API Reference

The backend exposes a lightweight REST endpoint:

### `POST /calculate`

#### Request Payload:
```json
{
  "gate": "AND",
  "a": 1,
  "b": 1
}
```

#### Response:
```json
{
  "result": 1,
  "gate": "AND",
  "a": 1,
  "b": 1,
  "expression": "1 · 1 = 1",
  "explanation": "Outputs 1 only when both inputs are 1: 1 AND 1 = 1",
  "backend": "C++ Library (logic.dll)"
}
```

---

## 🎨 Technologies Used

- **Frontend**: HTML5, Vanilla CSS3 (Custom Properties, Flexbox/Grid, Glassmorphism), SVG (IEEE 315 gate geometry & filters), HTML5 Canvas 2D (electron particles, switch loops, waveforms), Web Audio API.
- **Backend**: Python 3 standard library (`ctypes`, `http.server`).
- **Core Engine**: C++ (`extern "C"` bitwise primitives).

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
