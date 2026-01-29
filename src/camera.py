import cv2

def list_ports():
    print("Mencari kamera aktif (Mode Default)...")
    # Cek index 0 sampai 10 (kadang DroidCam suka ngumpet di index gede)
    for i in range(10):
        # HAPUS cv2.CAP_DSHOW, biarkan default (CAP_ANY)
        cap = cv2.VideoCapture(i) 
        
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"✅ Kamera DITEMUKAN di Index: {i}")
                w = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
                h = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
                print(f"   Resolusi: {int(w)}x{int(h)}")
            else:
                print(f"⚠️  Kamera terdeteksi di Index {i}, tapi gagal baca frame (Mungkin lagi dipake apps lain?)")
            cap.release()
        else:
            pass # Gak usah diprint biar gak nyepam console

if __name__ == '__main__':
    list_ports()