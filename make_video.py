import os
import cv2
import re

# Thư mục chứa script
script_dir = os.path.dirname(os.path.abspath(__file__))
detect_root = os.path.join(script_dir, "yolov5", "runs", "detect")
output_dir = os.path.join(script_dir, "output_video")

# Tạo thư mục output_video nếu chưa có
os.makedirs(output_dir, exist_ok=True)

# --- Tìm thư mục fgvd_detect hoặc fgvd_detectN lớn nhất ---
pattern = re.compile(r"fgvd_detect(\d*)")
latest_folder = None
max_index = -1

for folder in os.listdir(detect_root):
    match = pattern.fullmatch(folder)
    if match:
        idx_str = match.group(1)
        idx = int(idx_str) if idx_str.isdigit() else 0
        if idx > max_index:
            max_index = idx
            latest_folder = folder

if latest_folder is None:
    raise FileNotFoundError("❌ Không tìm thấy thư mục fgvd_detect(N) trong runs/detect")

image_folder = os.path.join(detect_root, latest_folder)

# --- Tìm tên file output_videoN.mp4 chưa tồn tại ---
video_index = 1
while True:
    video_name = os.path.join(output_dir, f"output_video{video_index}.mp4")
    if not os.path.exists(video_name):
        break
    video_index += 1

fps = 30  # Frame per second

# Lấy danh sách ảnh
images = sorted(
    [img for img in os.listdir(image_folder) if img.endswith(".jpg") or img.endswith(".png")]
)

if not images:
    raise FileNotFoundError(f"❌ Không tìm thấy ảnh .jpg hoặc .png trong {image_folder}")

# Lấy kích thước ảnh đầu tiên
first_image = cv2.imread(os.path.join(image_folder, images[0]))
height, width, _ = first_image.shape

# Tạo video writer
out = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))

# Ghi từng ảnh
for image in images:
    frame = cv2.imread(os.path.join(image_folder, image))
    out.write(frame)

out.release()
print(f"✅ Video đã được lưu tại: {video_name}")
