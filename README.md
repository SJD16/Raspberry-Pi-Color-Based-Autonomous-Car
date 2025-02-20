# Raspberry-Pi-Color-Based-Autonomous-Car

# 🚗 Raspberry Pi Color-Based Autonomous Car  

## 📌 Overview  
This project is a **Raspberry Pi-powered autonomous car** that uses **computer vision** to detect colors and make driving decisions based on road rules. The system:  
- **Starts moving when a green signal appears** in the camera's top view.  
- **Stops when a red signal appears** in the same area.  
- **Maintains its position on the track** using a white line on a black road.  
- **Turns left or right** if it detects the white line drifting to the edges, adjusting its position to stay centered.  

This behavior simulates an **intelligent vehicle** following basic driving rules, similar to a real-world traffic light system.  

## How It Works
📸 Camera Input: Captures real-time video of the track.
🎨 Color Detection:
    
    - 🟢 Green at the top → Move forward
    - 🔴 Red at the top → Stop
    - ⚪ White line detected at left → Turn left
    - ⚪ White line detected at right → Turn right
    ⚡ Motor Control: The Raspberry Pi processes this information and sends commands to the L293D motor driver to control the car’s movement.

## 🛠️ Features  
- ✅ **Color-based decision-making** (Green = Go, Red = Stop)  
- ✅ **Real-time image processing** with OpenCV  
- ✅ **Lane-following logic** to stay on track  
- ✅ **Motor control** via Raspberry Pi and L293D driver  

## 🏗️ Hardware Requirements  
To build this project, you need:  
- 🖥️ Raspberry Pi (any model with camera support)  
- 📷 Raspberry Pi Camera Module  
- ⚙️ L293D Motor Driver  
- 🚗 Motors & Wheels  
- 🔩 Chassis (for mounting components)  
- 🔋 Power source (battery pack)  

## 🖥️ Software Requirements  
- Raspberry Pi OS  
- Python 3  
- OpenCV  
- NumPy  
- RPi.GPIO  

## 🚀 Setup & Installation  

### 1️⃣ Install Required Libraries  
Run the following commands on your Raspberry Pi:  

```bash
sudo apt update && sudo apt upgrade
sudo apt install python3-opencv python3-numpy
pip install RPi.GPIO

```
## 2️⃣ Connect Hardware
🛠️ Follow these steps to connect the hardware correctly:
- 🖼️ Attach the camera module to the Raspberry Pi.
- 🖧 Connect the L293D motor driver to the Raspberry Pi's GPIO pins.
- ⚙️ Wire the motors to the L293D for movement control.

## 3️⃣ Run the Code

Clone the repository and execute the script:

```bash
git clone https://github.com/your-username/autonomous-car.git
cd autonomous-car
python3 main.py
```
