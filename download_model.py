# if and if only use when you dont get access to the drive
from deepdanbooru import commands

commands.evaluate(
    image_files=[], 
    project_path="./models/deepdanbooru_model", 
    allow_folder=True, 
    save_txt=False
)
print("✅ DeepDanbooru model downloaded successfully.")