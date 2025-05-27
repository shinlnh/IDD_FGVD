import os
import shutil

splits = ['train', 'val', 'test']
base_path = 'Dataset'

for split in splits:
    old_img_dir = os.path.join(base_path, split, 'images')
    old_anno_dir = os.path.join(base_path, split, 'annos')

    new_img_dir = os.path.join(base_path, 'images', split)
    new_lbl_dir = os.path.join(base_path, 'labels', split)

    os.makedirs(new_img_dir, exist_ok=True)
    os.makedirs(new_lbl_dir, exist_ok=True)

    # Di chuyển ảnh
    for file in os.listdir(old_img_dir):
        if file.endswith('.jpg') or file.endswith('.png'):
            shutil.copy2(os.path.join(old_img_dir, file), os.path.join(new_img_dir, file))

    # Di chuyển annotation gốc (xml) sang chỗ riêng để convert
    for file in os.listdir(old_anno_dir):
        if file.endswith('.xml'):
            shutil.copy2(os.path.join(old_anno_dir, file), os.path.join(new_lbl_dir, file))
