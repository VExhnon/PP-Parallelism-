import threading
import requests
import time

# Список сайтов для мониторинга
sites = [
    "https://www.google.com",
    "https://www.github.com",
    "https://www.python.org",
    "https://stackoverflow.com",
    "https://www.reddit.com",
    "https://www.youtube.com"
]


# Функция для проверки доступности сайта
def check_site_status(site):
    try:
        response = requests.get(site, timeout=5)
        if response.status_code == 200:
            result = f"{time.ctime()}: {site} is up!"
        else:
            result = f"{time.ctime()}: {site} is down! Status code: {response.status_code}"
    except requests.RequestException as e:
        result = f"{time.ctime()}: {site} is down! Error: {str(e)}"

    print(result)

    # Записываем результат в файл
    with open("site_status_log.txt", "a") as log_file:
        log_file.write(result + "\n")



# Функция для мониторинга сайтов с многопоточностью
def monitor_sites():
    threads = []
    for site in sites:
        thread = threading.Thread(target=check_site_status, args=(site,))
        threads.append(thread)
        thread.start()

    # Ожидаем завершения всех потоков
    for thread in threads:
        thread.join()


if __name__ == "__main__":
    while True:
        print(f"\nStarting site check at {time.ctime()}...\n")
        monitor_sites()
        # Пауза на 60 секунд перед следующей проверкой
        time.sleep(60)
