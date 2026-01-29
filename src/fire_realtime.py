import cv2
from ultralytics import YOLO
from flask import Flask, render_template, Response
import time

# --- Inisialisasi Aplikasi Flask ---
app = Flask(__name__, template_folder='../templates')

# --- KONFIGURASI KAMERA (ATUR DI SINI) ---
# Masukkan angka index kamera yang tadi kamu temukan (misal: 1 atau 0)
CAMERA_INDEX = 1  

# --- Load Model YOLO ---
# Menggunakan device=0 (GPU)
print("⏳ Loading Model YOLOv8...")
model = YOLO("runs/detect/train3/weights/best.pt")
print("✅ Model Loaded!")

cap = None

def open_camera(index):
    global cap
    
    if cap:
        cap.release()
    
    print(f"📷 Mencoba membuka kamera index: {index}")
    
    # HAPUS CAP_DSHOW AGAR DROIDCAM LANCAR
    cap = cv2.VideoCapture(index)

    # Set Resolusi HD (1280x720)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    if not cap.isOpened():
        print(f"❌ ERROR: Kamera index {index} GAGAL dibuka!")
        return False
    
    print(f"✅ Kamera index {index} BERHASIL dibuka!")
    return True

# --- BUKA KAMERA SESUAI PILIHAN KAMU ---
# Langsung paksa buka index yang kamu mau, gak pake fallback-fallbackan
open_camera(CAMERA_INDEX)

def generate_frames():
    global cap
    while True:
        # Logika Reconnect Sederhana
        if not cap or not cap.isOpened():
            print("⚠️ Kamera putus, mencoba reconnect...")
            time.sleep(2)
            open_camera(CAMERA_INDEX)
            continue

        ret, frame = cap.read()
        if not ret:
            # Jangan print error terus-terusan biar gak spam
            continue

        # --- OPTIMASI GPU (JANGAN DIHAPUS) ---
        # device=0 -> GPU RTX 4050
        # half=True -> FP16 (Lebih ngebut)
        results = model(frame, conf=0.4, device=0, half=True, verbose=False)
        
        # Plot hasil deteksi
        res_plotted = results[0].plot()

        # --- OPTIMASI KOMPRESI WEB ---
        # Kualitas 60% biar enteng di browser
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]
        
        _, buffer = cv2.imencode('.jpg', res_plotted, encode_param)
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

# --- Endpoint Flask ---

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), 
                    mimetype='multipart/x-mixed-replace; boundary=frame')

# --- Jalankan App ---

if __name__ == '__main__':
    print(f"🔥 Server berjalan di http://127.0.0.1:5001")
    # threaded=True wajib biar video stream lancar
    app.run(host='0.0.0.0', port=5001, debug=True, threaded=True)