import os
import disk_scanner
import link_scanner

def main_menu():
    """Отображает главное меню программы."""
    print("Выберите режим работы:")
    print("1. Сканирование дисков")
    print("2. Сканирование ссылок")
    choice = input("Введите номер режима: ")
    if choice == "1":
        # Запуск сканирования дисков
        disk_scanner.main()
    elif choice == "2":
        # Запуск сканирования ссылок
        link_scanner.main()
    else:
        print("Неверный выбор. Пожалуйста, выберите 1 или 2.")

if __name__ == "__main__":
    # Константы
    extract_to = os.path.join(os.getcwd(), "bases")  # Целевая папка
    
    while True:
        # Проверяем, существует ли директория bases
        if os.path.exists(extract_to):
            print(f"Директория {extract_to} найдена. Переходим к главному меню.")
            main_menu()
            break
        else:
            print(f"Директория {extract_to} не найдена.")
            input("Нажмите Enter, чтобы проверить наличие директории снова...")
            # После нажатия Enter проверяем заново
