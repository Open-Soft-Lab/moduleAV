import os
import requests

# Загрузка списка вредоносных ссылок из всех текстовых файлов в папке
def load_malicious_links(folder_path):
    links = set()
    if os.path.exists(folder_path):
        for filename in os.listdir(folder_path):
            if filename.endswith(".txt"):
                file_path = os.path.join(folder_path, filename)
                with open(file_path, 'r') as file:
                    for line in file:
                        links.add(line.strip())
    return links

# Функция для проверки ссылок
def check_links(user_links, malicious_links):
    infected_links = []
    for link in user_links:
        link = link.strip()
        if link in malicious_links:
            infected_links.append(link)
            print(f"Вредоносная ссылка обнаружена: {link}")
        else:
            print(f"Ссылка безопасна: {link}")
    return infected_links

# Главная функция модуля
def main():
    folder_path = "bases/links"
    malicious_links = load_malicious_links(folder_path)
    if not malicious_links:
        print("Не найдено ни одной вредоносной ссылки для сравнения.")
        input("Нажмите Enter, чтобы выйти...")
        return
    
    user_input = input("Введите ссылки для проверки (через запятую): ")
    user_links = [link.strip() for link in user_input.split(",")]
    infected_links = check_links(user_links, malicious_links)

    if infected_links:
        print("\nСписок зараженных ссылок:")
        for link in infected_links:
            print(link)
    else:
        print("Зараженные ссылки не найдены.")

    # Добавляем запрос на нажатие Enter перед выходом
    input("Проверка завершена. Нажмите Enter, чтобы выйти...")

if __name__ == "__main__":
    main()
