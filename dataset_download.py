#downloading dataset directly from kaggle through api
import kagglehub
import shutil
import os

# Download to default kagglehub location
download_path = kagglehub.dataset_download("purvitsharma/amazonn-reviews")

# Your custom target folder
custom_path = "/home/kefi/Documents/program01/"

# Create target directory if it doesn't exist
os.makedirs(custom_path, exist_ok=True)

# Move contents to your custom directory
for file_name in os.listdir(download_path):
    full_file_name = os.path.join(download_path, file_name)
    if os.path.isfile(full_file_name):
        shutil.copy(full_file_name, custom_path)

print("Files copied to:", os.path.abspath(custom_path))
