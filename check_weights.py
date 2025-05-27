import torch

model_path = r"E:\SourceCode\Python\AI_Edge\IDD_FGVD\yolov5\runs\train\exp\weights\best.pt"
model = torch.load(model_path, map_location="cpu", weights_only=False)

# Trích xuất state_dict
if isinstance(model, dict):
    if 'model' in model:
        state_dict = model['model'].state_dict()
    elif 'state_dict' in model:
        state_dict = model['state_dict']
    else:
        state_dict = model
else:
    state_dict = model.state_dict()

# Kiểm tra kiểu dữ liệu
dtypes = set(p.dtype for p in state_dict.values())
print("Kiểu dữ liệu của trọng số:", dtypes)