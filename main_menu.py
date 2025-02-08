import disk_scanner
import link_scanner

def main_menu():
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
    main_menu()
