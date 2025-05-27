import os
import xml.etree.ElementTree as ET

# Mapping fine-grained class names → 7 coarse classes
def fine_to_coarse(name):
    if name.startswith('motorcycle'):
        return 0
    elif name.startswith('car'):
        return 1
    elif name.startswith('scooter'):
        return 2
    elif name.startswith('autorickshaw'):
        return 3
    elif name.startswith('truck'):
        return 4
    elif name.startswith('mini-bus'):
        return 5
    elif name.startswith('bus'):
        return 6
    else:
        return None  # Skip unknown

# Get image size from XML or use fallback
def get_image_size(root):
    size_tag = root.find('size')
    if size_tag is not None:
        w = int(size_tag.find('width').text)
        h = int(size_tag.find('height').text)
        return w, h
    return 1280, 720  # fallback if missing

# Convert one XML file
def convert_one(xml_path, txt_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    img_w, img_h = get_image_size(root)

    lines = []
    for obj in root.findall('object'):
        name = obj.find('name').text
        coarse_id = fine_to_coarse(name)
        if coarse_id is None:
            continue

        bbox = obj.find('bndbox')
        xmin = float(bbox.find('xmin').text)
        ymin = float(bbox.find('ymin').text)
        xmax = float(bbox.find('xmax').text)
        ymax = float(bbox.find('ymax').text)

        x_center = ((xmin + xmax) / 2) / img_w
        y_center = ((ymin + ymax) / 2) / img_h
        width = (xmax - xmin) / img_w
        height = (ymax - ymin) / img_h

        lines.append(f"{coarse_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

    with open(txt_path, 'w') as f:
        f.write('\n'.join(lines))

# Convert all .xml files in a folder
def convert_folder(xml_folder):
    for file in os.listdir(xml_folder):
        if not file.endswith('.xml'):
            continue
        xml_path = os.path.join(xml_folder, file)
        txt_path = os.path.join(xml_folder, file.replace('.xml', '.txt'))
        convert_one(xml_path, txt_path)

        # Xoá file .xml sau khi convert (nếu muốn)
        os.remove(xml_path)

# === CHẠY CHUYỂN ĐỔI CHO TẤT CẢ SPLITS ===
splits = ['train', 'val', 'test']
for split in splits:
    label_path = os.path.join('Dataset', 'labels', split)
    convert_folder(label_path)
