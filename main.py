import cv2
import numpy as np

def save_results_to_file(results):
    with open("results.txt", "w") as f:
        for frame_objects in results:
            for obj in frame_objects:
                class_label, box = obj
                x, y, w, h = box
                f.write(f"{class_label} - x: {x}, y: {y}, w: {w}, h: {h}\n")

# YOLOv3 modelini yükleyin
weights_path = r"C:\Users\merye\Desktop\opencvli\yolov3.weights"
cfg_path = r"C:\Users\merye\Desktop\opencvli\yolov3.cfg"
net = cv2.dnn.readNet(weights_path, cfg_path)

# Etiketleri yükleyin
coco_path = r"C:\Users\merye\Desktop\opencvli\coco.names"
classes = []
with open(coco_path, "r") as f:
    classes = [line.strip() for line in f.readlines()]

# YOLOv3 çıkış katmanlarını alın
layer_names = net.getLayerNames()
output_layers = [layer_names[i-1] for i in net.getUnconnectedOutLayers()]

# Video dosyasını açın
video = cv2.VideoCapture("kayit.avi")

results = []  # Detected objects will be stored in this list

while True:
    # Video çerçevesini okuyun
    ret, frame = video.read()

    if not ret:
        break

    height, width, channels = frame.shape

    # Giriş görüntüsü için bir blob oluşturun
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    # YOLOv3 modeline giriş görüntüsünü ilerletin
    net.setInput(blob)
    outs = net.forward(output_layers)

    # Nesne tespiti için listeleri ve dizinleri saklayın
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5:
                # Nesne tespiti için sınırlayıcı kutu koordinatlarını alın
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Non-maximum suppression (NMS) uygulayın
    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    # Tespit edilen nesnelerin çerçevelerini çizin ve sonuçları results listesine ekleyin
    detected_objects = [(classes[class_ids[i]], boxes[i]) for i in indexes]
    results.append(detected_objects)

    # Tespit edilen nesnelerin çerçevelerini çizin
    font = cv2.FONT_HERSHEY_PLAIN
    for obj in detected_objects:
        class_label, box = obj
        x, y, w, h = box
        color = (128, 0, 128)   # Mor renk
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, class_label, (x, y + 30), font, 1, color, 2)

    # Çıktı görüntüsünü gösterin
    cv2.imshow("Nesne Tespit", frame)

    # Sonuçları results.txt dosyasına kaydedin
    save_results_to_file([detected_objects])

    # Çıkış yapmak için 'q' tuşuna basın
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Tüm pencereleri kapatın ve videoyu serbest bırakın
video.release()
cv2.destroyAllWindows()
