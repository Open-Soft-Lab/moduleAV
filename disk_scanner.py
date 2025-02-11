import os
import hashlib
import threading
import psutil
import zipfile
import patoolib  # Для работы с архивами

# Функция для вычисления хеша файла
def calculate_hash(file_path, hash_type):
    BUF_SIZE = 65536
    if hash_type == "sha256":
        hasher = hashlib.sha256()
    elif hash_type == "md5":
        hasher = hashlib.md5()
    else:
        raise ValueError("Unsupported hash type")
    
    try:
        with open(file_path, 'rb') as f:
            while data := f.read(BUF_SIZE):
                hasher.update(data)
        return hasher.hexdigest()
    except Exception as e:
        return None

# Загрузка списка сигнатур из всех .txt файлов в указанной директории
def load_signatures(directory):
    signatures = {}
    if os.path.exists(directory):
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith('.txt'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as f:
                        for line in f:
                            hash_value = line.strip()
                            if hash_value:
                                signatures[hash_value] = file  # Сохраняем имя файла базы
    return signatures

# Проверка одного файла на наличие угроз
def check_file(file_path, sha256_signatures, md5_signatures, output_file):
    try:
        sha256_hash = calculate_hash(file_path, "sha256")
        if sha256_hash and sha256_hash in sha256_signatures:
            print(f"Зараженный файл найден: {file_path} (SHA-256)")
            with open(output_file, "a") as log_file:
                log_file.write(f"Путь: {file_path}\n")
                log_file.write(f"Тип хэша: SHA-256\n")
                log_file.write(f"Хэш: {sha256_hash}\n")
                log_file.write(f"Файл базы: {sha256_signatures[sha256_hash]}\n\n")  # Добавляем имя файла базы
            return True
        
        md5_hash = calculate_hash(file_path, "md5")
        if md5_hash and md5_hash in md5_signatures:
            print(f"Зараженный файл найден: {file_path} (MD5)")
            with open(output_file, "a") as log_file:
                log_file.write(f"Путь: {file_path}\n")
                log_file.write(f"Тип хэша: MD5\n")
                log_file.write(f"Хэш: {md5_hash}\n")
                log_file.write(f"Местоположение в базе: {md5_signatures[md5_hash]}\n\n")  # Добавляем имя файла базы
            return True
    except Exception as e:
        print(f"Ошибка при проверке файла {file_path}: {e}")
    return False

# Функция для сканирования архива
def scan_archive(archive_path, sha256_signatures, md5_signatures, output_file, temp_dir="temp"):
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    try:
        print(f"Сканирование архива: {archive_path}")
        # Определение типа архива
        if zipfile.is_zipfile(archive_path):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
        else:
            # Используем patool для других форматов архивов
            patoolib.extract_archive(archive_path, outdir=temp_dir)

        # Сканирование распакованных файлов
        for root, _, files in os.walk(temp_dir):
            for file in files:
                file_path = os.path.join(root, file)
                if check_file(file_path, sha256_signatures, md5_signatures, output_file):
                    print(f"Обнаружен зараженный файл в архиве: {file_path}")

    except Exception as e:
        print(f"Ошибка при обработке архива {archive_path}: {e}")
    finally:
        # Удаление временной директории
        for root, dirs, files in os.walk(temp_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(temp_dir)

# Основная функция сканирования
def scan_directory(directory, sha256_signatures, md5_signatures, output_file="infected_files.txt"):
    total_files = sum(len(files) for _, _, files in os.walk(directory))
    print(f"Сканирование директории: {directory}")
    print(f"Общее количество файлов для сканирования: {total_files}")

    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if not os.path.isfile(file_path):
                continue

            try:
                print(f"Текущий файл: {file_path}")

                # Если файл является архивом, сканируем его содержимое
                if file.lower().endswith(('.zip', '.rar', '.7z', '.tar', '.gz')):
                    scan_archive(file_path, sha256_signatures, md5_signatures, output_file)
                else:
                    # Иначе проверяем сам файл
                    check_file(file_path, sha256_signatures, md5_signatures, output_file)

            except Exception as e:
                print(f"Ошибка при обработке файла {file_path}: {e}")

    print("Сканирование завершено.")

# Получение списка дисков
def get_available_drives():
    drives = [partition.mountpoint for partition in psutil.disk_partitions() if partition.device and partition.mountpoint]
    return drives

# Выбор диска пользователем
def select_drive(drives):
    print("Доступные диски для сканирования:")
    for idx, drive in enumerate(drives, start=1):
        print(f"{idx}. {drive}")
    
    while True:
        try:
            choice = int(input("Выберите номер диска для сканирования: "))
            if 1 <= choice <= len(drives):
                return drives[choice - 1]
            else:
                print("Неверный выбор. Пожалуйста, введите корректный номер.")
        except ValueError:
            print("Введите число.")

# Главная функция
def main():
    drives = get_available_drives()
    if not drives:
        print("Не удалось найти доступные диски.")
        return
    
    selected_drive = select_drive(drives)
    sha256_signatures = load_signatures("bases/sha256")
    md5_signatures = load_signatures("bases/md5")

    if not sha256_signatures and not md5_signatures:
        print("Не найдено ни одной сигнатуры для сканирования.")
        return
    
    def run_scan():
        scan_directory(selected_drive, sha256_signatures, md5_signatures)
        print("\nСканирование завершено.")
        input("Нажмите Enter для выхода...")  # Запрос нажатия Enter
    
    scan_thread = threading.Thread(target=run_scan)
    scan_thread.start()
    scan_thread.join()

if __name__ == "__main__":
    main()
