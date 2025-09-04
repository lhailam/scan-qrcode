from reader_qr import qr_code_reader
import os
import json

image_folder = "image_test"

results = {}
error_images = {}

for filename in os.listdir(image_folder):
    if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
        file_path = os.path.join(image_folder, filename)
        try:
            qr_result = qr_code_reader(file_path)
            # Giả sử qr_code_reader trả về dict khi thành công và string khi lỗi
            print(f"Name {filename}: {qr_result}")
        except Exception as e:
            error_images[filename] = f"Error: {str(e)}"
            print(f"Error processing {filename}: {str(e)}")


print("All results have been saved to result_infomations.json")