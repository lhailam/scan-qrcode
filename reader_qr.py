from qreader import QReader
import cv2
import json
import os

qreader = QReader()

def find_code_by_name(name, refer_code, file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            result_data = json.load(file)
    except Exception as err:
        print("Error reading file:", err)
        return ""
    
    name_lower = name.lower()
    result = [
        item for item in result_data
        if any(name_lower in key.lower() for key in item.keys())
    ]

    if not result:
        return ""

    if len(result) == 1:
        key = next((k for k in result[0] if name_lower in k.lower()), None)
        if key:
            values = result[0][key].split(", ")
            return values[0] if len(values) > 1 else result[0][key]

    if len(result) > 1:
        result_with_refer_code = next((
            item for item in result
            if any(refer_code in item[k] for k in item if name_lower in k.lower())
        ), None)

        if not result_with_refer_code:
            return ""

        key = next((k for k in result_with_refer_code if name_lower in k.lower()), None)
        if key:
            return result_with_refer_code[key].replace(f", {refer_code}", "")

    return ""

def find_ky_tu_tinh(tinh_name):
    try:
        with open('data/ky_tu_tinh.json', 'r', encoding='utf-8') as file:
            ky_tu_data = json.load(file)
        
        tinh_lower = tinh_name.lower()
        for item in ky_tu_data:
            key = next(iter(item))  # Lấy key đầu tiên trong dictionary
            if tinh_lower == key.lower():
                return item[key]
        return ""  # Trả về rỗng nếu không tìm thấy
    except Exception as e:
        print(f"Error reading ky_tu_tinh.json: {str(e)}")
        return ""

def qr_code_reader(path):
    try:
        image = cv2.imread(path)
        if image is None:
            return "Không thể đọc file ảnh"
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        decoded_text = qreader.detect_and_decode(image=image)
        
        if decoded_text and isinstance(decoded_text, tuple):
            qr_data = decoded_text[0]
        else:
            return "Không thể giải mã QR code"
        return qr_data
    except Exception as e:
        return f"Error: {str(e)}"

# image_folder = "images"

# results = {}
# error_images = {}

# for filename in os.listdir(image_folder):
#     if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
#         file_path = os.path.join(image_folder, filename)
#         try:
#             qr_result = qr_code_reader(file_path)
#             if isinstance(qr_result, str):
#                 error_images[filename] = qr_result
#                 print(f"Error processing {filename}: {qr_result}")
#             else:
#                 results[filename] = qr_result
#                 print(f"Processed {filename}: {qr_result}")
#         except Exception as e:
#             error_images[filename] = f"Error: {str(e)}"
#             print(f"Error processing {filename}: {str(e)}")

# with open('result_infomations.json', 'w', encoding='utf-8') as json_file:
#     json.dump(results, json_file, ensure_ascii=False, indent=4)

# if error_images:
#     with open('error_images.json', 'w', encoding='utf-8') as error_file:
#         json.dump(error_images, error_file, ensure_ascii=False, indent=4)
#     print(f"Found {len(error_images)} error images. Details saved to error_images.json")
# else:
#     print("No error images found")

# print("All results have been saved to result_infomations.json")