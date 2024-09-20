import os
from PIL import Image
import multiprocessing
import time

# Папка с изображениями
input_folder = "images"
output_folder = "processed_images"

# Убедимся, что папка для обработанных изображений существует
if not os.path.exists(output_folder):
    os.makedirs(output_folder)


# Функция для обработки изображения (изменение размера)
def process_image(image_path):
    try:
        img = Image.open(image_path)
        img = img.resize((800, 800))  # Изменение размера до 800x800 пикселей
        img = img.convert("L")  # Конвертация в черно-белый формат

        # Сохранение обработанного изображения в папку output
        base_name = os.path.basename(image_path)
        output_path = os.path.join(output_folder, base_name)
        img.save(output_path)
        print(f"Processed {image_path} and saved to {output_path}")
    except Exception as e:
        print(f"Failed to process {image_path}: {e}")


# Функция для обработки изображений с многопроцессорностью
def process_images_concurrently():
    images = [os.path.join(input_folder, img) for img in os.listdir(input_folder) if
              img.endswith(".jpg") or img.endswith(".png")]

    # Запускаем процессы для каждой задачи
    with multiprocessing.Pool() as pool:
        pool.map(process_image, images)


if __name__ == "__main__":
    start_time = time.time()
    print("Starting image processing...")

    process_images_concurrently()

    end_time = time.time()
    print(f"Finished processing in {end_time - start_time:.2f} seconds")
