import pandas as pd
import os

# Загрузка CSV-файла
df = pd.read_csv("train.csv", usecols=["filename", "x_c", "y_c", "w", "h", "class_label"])

# Создание папки для YOLO-разметки
output_dir = "yolo_annotations"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Словарь для хранения аннотаций
annotations = {}

# Итерация по строкам CSV-файла
for i in range(df.shape[0]):
    # Получение информации о записи
    filename = df.loc[i, "filename"]
    x_center = df.loc[i, "x_c"]
    y_center = df.loc[i, "y_c"]
    width = df.loc[i, "w"]
    height = df.loc[i, "h"]

    # Определение label_class
    if df.loc[i, "class_label"] == "reindeer":
        label_class = 0
    elif df.loc[i, "class_label"] == "fawn":
        label_class = 1
    else:
        raise ValueError(f"Неизвестный класс: {df.loc[i, 'class_label']}")

    # Формирование строки аннотации YOLO
    annotation = f"{label_class} {x_center} {y_center} {width} {height}"

    # Добавление аннотации в список
    if filename not in annotations:
        annotations[filename] = []
    annotations[filename].append(annotation)

# Сохранение аннотаций
for filename, annotations in annotations.items():
    filename_without_ext = os.path.splitext(filename)[0]
    
    with open(os.path.join(output_dir, f"{filename.split('.')[0]}.txt"), "w") as f:
        f.write("\n".join(annotations))

print("Файлы YOLO-разметки успешно созданы!")