import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import numpy as np
import math
import urllib.request
import os
import time

# 1. Yüz modeli yoksa otomatik indir 
model_path = 'face_landmarker.task'
if not os.path.exists(model_path):
    print("MediaPipe güncel yapay zeka modeli indiriliyor...")
    url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task"
    urllib.request.urlretrieve(url, model_path)

# 2. EAR (Göz Kırpma Oranı) Hesaplama Fonksiyonu
def calculate_ear(eye_points):
    v1 = math.dist(eye_points[1], eye_points[5])
    v2 = math.dist(eye_points[2], eye_points[4])
    h = math.dist(eye_points[0], eye_points[3])
    return (v1 + v2) / (2.0 * h) if h != 0 else 0

# Standart göz koordinat indeksleri
RIGHT_EYE = [33, 160, 158, 133, 153, 144]
LEFT_EYE = [362, 385, 387, 263, 373, 380]

# 3. Yeni Nesil MediaPipe API Ayarları
base_options = python.BaseOptions(model_asset_path=model_path)
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    output_face_blendshapes=False,
    output_facial_transformation_matrixes=False,
    num_faces=1
)
detector = vision.FaceLandmarker.create_from_options(options)

# --- Kalibrasyon ve Üst Gövde Değişkenleri ---
calibration_duration = 4  # 4 saniye dik oturuş kalibrasyonu
calibration_heights = []
ref_height = None
is_calibrated = False
start_time = time.time()
# ----------------------------------------------

# 4. Kamerayı Başlat
cap = cv2.VideoCapture(0)
print("Sistem başlatıldı. Lütfen ilk 4 saniye dik oturun...")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
    detection_result = detector.detect(mp_image)

    status_text = "Kullanici Masa Basinda Degil!"
    posture_text = ""
    color = (0, 255, 0)
    posture_color = (0, 255, 255)
    upper_body_color = (0, 255, 0)

    if detection_result.face_landmarks:
        for face_landmarks in detection_result.face_landmarks:
            landmarks = [(int(pt.x * w), int(pt.y * h)) for pt in face_landmarks]

            # --- ÜST GÖVDE ÇERÇEVESİ OLUŞTURMA (Yeni API ile) ---
            # Yüz noktalarının sınırlarını buluyoruz
            x_coords = [pt[0] for pt in landmarks]
            y_coords = [pt[1] for pt in landmarks]
            
            face_x_min, face_x_max = min(x_coords), max(x_coords)
            face_y_min, face_y_max = min(y_coords), max(y_coords)
            
            # Yüz genişliğini baz alarak omuz ve üst gövde için dinamik bir çerçeve hesaplıyoruz
            face_width = face_x_max - face_x_min
            face_height = face_y_max - face_y_min
            
            # Üst gövdeyi (Omuzlar ve göğüs dahil) kaplayacak genişletilmiş çerçeve sınırları
            body_x_min = max(0, face_x_min - int(face_width * 1.5))
            body_x_max = min(w, face_x_max + int(face_width * 1.5))
            body_y_min = max(0, face_y_min - int(face_height * 0.5))
            body_y_max = min(h, face_y_max + int(face_height * 3.0)) # Göğüs/bel hizasına kadar indirir

            # Kamburluk tespiti için yüzün çene altı ile tepe noktası arasındaki dikey merkezi izliyoruz
            current_center_y = (face_y_min + face_y_max) / 2

            # --- KALİBRASYON ---
            elapsed_time = time.time() - start_time
            if not is_calibrated:
                if elapsed_time < calibration_duration:
                    calibration_heights.append(current_center_y)
                    posture_text = f"Kalibrasyon Yapiliyor... Kalan: {int(calibration_duration - elapsed_time)}s"
                    posture_color = (0, 165, 255)
                else:
                    if len(calibration_heights) > 0:
                        ref_height = sum(calibration_heights) / len(calibration_heights)
                        is_calibrated = True
                        print("Kalibrasyon tamamlandı!")
            
            # --- KAMBURLUK KONTROLÜ ---
            else:
                # Kullanıcı öne eğilip kamburlaştığında kafası (yüz merkezi) aşağı düşer (yani Y piksel değeri büyür)
                # Buradaki hassasiyet eşiği: face_height * 0.25 (Yüz boyunun çeyreği kadar aşağı düşerse uyarır)
                if current_center_y > (ref_height + (face_height * 0.25)):
                    posture_text = "UYARI: Kambur Oturuyorsunuz!"
                    posture_color = (0, 0, 255)
                    upper_body_color = (0, 0, 255) # Üst gövde çerçevesini kırmızı yap
                else:
                    posture_text = "Durus: Dik / Ideal"
                    posture_color = (0, 255, 0)
                    upper_body_color = (0, 255, 0) # Üst gövde çerçevesini yeşil yap

            # Üst Gövde Çerçevesini Çiz
            cv2.rectangle(frame, (body_x_min, body_y_min), (body_x_max, body_y_max), upper_body_color, 2)

            # --- GÖZ VE ODAK TAKİBİ ---
            right_eye_pts = [landmarks[i] for i in RIGHT_EYE]
            left_eye_pts = [landmarks[i] for i in LEFT_EYE]

            right_ear = calculate_ear(right_eye_pts)
            left_ear = calculate_ear(left_eye_pts)
            avg_ear = (right_ear + left_ear) / 2.0

            for pt in right_eye_pts + left_eye_pts:
                cv2.circle(frame, pt, 1, (255, 0, 0), -1)

            if avg_ear < 0.21:
                status_text = "DIKKAT: Gozler Kapali / Yorgun!"
                color = (0, 0, 255)
            else:
                status_text = "Derse Odakli"
                color = (0, 255, 0)

    # Yazıları Ekrana Bas
    cv2.putText(frame, status_text, (30, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.75, color, 2)
    cv2.putText(frame, posture_text, (30, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.75, posture_color, 2)
    
    cv2.imshow("VisionDesk - Ust Govde ve Odak Takibi", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()