from ultralytics import YOLO
import cv2
import numpy as np
import torch
import sys
import logging
import time

# =========================================================================================
# Config
# =========================================================================================
logging.basicConfig(level=logging.INFO)
device = "cuda" if torch.cuda.is_available() else "cpu"

# Load YOLO model
try:
    model = YOLO("yolov8n.pt")  # Load model YOLOv8 nano (nhẹ, nhanh)
    logging.info(f"YOLO model loaded on {device}")
except Exception as e:
    logging.error(f"Failed to load YOLO model: {e}")
    sys.exit(1)  # Lỗi -> thoát chương trình luôn


# =========================================================================================
# (Optional) Preprocessing - resize giữ tỉ lệ + letterbox
# =========================================================================================
def preprocess_frame(frame, img_size=640):
    """
    Resize ảnh để vừa kích thước img_size của YOLO, giữ tỉ lệ gốc và thêm letterbox padding.
    Args:
        frame: ảnh BGR từ OpenCV
        img_size: kích thước đầu vào YOLO (thường là 640)
    Returns:
        letterbox_img: ảnh đã resize + padding
    """
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Chuyển sang RGB
    h, w = img.shape[:2]
    scale = min(img_size / h, img_size / w)  # Tính tỉ lệ scale
    new_w, new_h = int(w * scale), int(h * scale)

    # Resize ảnh theo tỉ lệ
    resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LINEAR)

    # Tạo ảnh nền xám để đặt ảnh resized vào giữa
    letterbox_img = np.full((img_size, img_size, 3), 114, dtype=np.uint8)
    top = (img_size - new_h) // 2
    left = (img_size - new_w) // 2
    letterbox_img[top:top+new_h, left:left+new_w] = resized

    return letterbox_img


# =========================================================================================
# Video detection loop
# =========================================================================================
def detect_video(video_path, save_output=False, output_path="output.mp4"):
    """
    Nhận diện đối tượng trong video theo từng frame.
    Args:
        video_path: đường dẫn file video
        save_output: True nếu muốn lưu video kết quả
        output_path: đường dẫn lưu video đầu ra
    """
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        logging.error(f"Không thể mở video: {video_path}")
        return
    
    # Cấu hình writer nếu cần lưu output
    out = None
    if save_output:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Định dạng MP4
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0
    start_time = time.time()

    # Đọc từng frame -> detect -> hiển thị
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Hết video
        
        # (Optional) Tiền xử lý nếu muốn tự resize trước
        # frame_input = preprocess_frame(frame)  
        frame_input = frame  # YOLOv8 tự resize được nếu bỏ qua bước trên

        # Chạy YOLO detect
        results = model(frame_input, device=device, verbose=False)

        # Vẽ bounding box và label lên frame
        annotated_frame = results[0].plot()

        # Lưu video nếu cần
        if save_output:
            out.write(annotated_frame)

        # Hiển thị real-time
        cv2.imshow("YOLO Detection", annotated_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Bấm 'q' để thoát sớm
            break

        frame_count += 1

    # Tính FPS thực tế
    end_time = time.time()
    elapsed = end_time - start_time
    fps_actual = frame_count / elapsed
    logging.info(f"Processed {frame_count} frames in {elapsed:.2f}s ({fps_actual:.2f} FPS)")

    # Giải phóng tài nguyên
    cap.release()
    if out:
        out.release()
    cv2.destroyAllWindows()


# =========================================================================================
# Run main
# =========================================================================================
if __name__ == "__main__":
    detect_video(r"database\data\6907708323293.mp4", save_output=False)
