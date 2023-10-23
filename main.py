import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import logging
import datetime


USER_LIST = "users.txt"
TEXT_FILE_PATH = 'text.txt'

INPUT_BOX_CSS = "#main > footer > div._2lSWV._3cjY2.copyable-area > div > span:nth-child(2) > div > div._1VZX7 > " \
                "div._3Uu1_ > div.g0rxnol2.ln8gz9je.lexical-rich-text-input > div.to2l77zo.gfz4du6o.ag5g9lrv.bze30y65" \
                ".kao4egtt"
CHROMEDRIVER = "C:\chromedriver.exe"
SELECTOR_CSS = "#main > footer > div._2lSWV._3cjY2.copyable-area"
LABEL_NAME_GROUP_CSS = "#main > header > div._2au8k > div._6u0RM > div > span"

logging.basicConfig(filename='my_script.log',
                    level=logging.INFO)



# Создание словаря "клиент:ссылка_на_группу" из тектового файла USER_LIST
def create_user_dict_from_file(file_path):
    user_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()  # Удалить лишние пробелы и символы перевода строки
            if line:
                parts = line.split(' ')  # Разделить строку на части
                if len(parts) == 2:
                    user_name, user_link = parts
                    user_dict[user_name] = user_link
    return user_dict


# Ожидание элемента на странице для проверки того что страница загрузилась
def wait_for_element(driver, selector, max_wait_time, retry_interval):
    total_wait_time = 0

    while total_wait_time < max_wait_time:
        try:
            WebDriverWait(driver, retry_interval).until(
                EC.presence_of_element_located(selector)
            )
            return True  # Элемент найден, выходим из цикла
        except:
            total_wait_time += retry_interval
            print(f"Ожидание элемента... Прошло {total_wait_time} сек.")

    return False  # Элемент не был найден после максимального времени ожидания


# Главная функция
def main():
    options = webdriver.ChromeOptions()
    options.add_argument(r"--user-data-dir=D:\newdir")
    options.add_argument(r'--profile-directory=Profile')
    service = Service(executable_path=CHROMEDRIVER)
    driver = webdriver.Chrome(service=service, options=options)

    # Получаем словарь "Клиент:Ссылка"
    users_and_links = create_user_dict_from_file(USER_LIST)
    i = 0
    # Цикл по клиентам для отправки
    for user_name, link, in users_and_links.items():
        i += 1
        # Открываем лог для текущего клиента с именем клиента
        logger = logging.getLogger(user_name+" ")

        # Получаем текущую дату и время
        current_datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        driver.get(link)

        # Ожидание загрузки страницы
        selector = (By.CSS_SELECTOR, SELECTOR_CSS)
        if not wait_for_element(driver, selector, max_wait_time=120, retry_interval=20):
            print("Элемент не был найден после максимального времени ожидания.")
            continue

        # Открываем файл с текстом для копирования в буффер
        with open(TEXT_FILE_PATH, 'r', encoding='utf-8') as file:
            message_text = file.read()

        # Находим поле ввода текста и выделяем его для вставки текста ищ буффера
        input_box = driver.find_element(By.CSS_SELECTOR, INPUT_BOX_CSS)
        input_box.click()

        # Копируем текст в буфер обмена
        driver.execute_script("navigator.clipboard.writeText(arguments[0]);", message_text)

        # Вставляем текст из буфера обмена в поле ввода текста
        input_box.send_keys(Keys.CONTROL, 'v')

        # Отправляем сообщение
        input_box.send_keys(Keys.RETURN)

        # Получаем имя группы куда отправили
        label_name_group = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, LABEL_NAME_GROUP_CSS)))

        print(f"№{i}) В группу: {label_name_group.text} - Сообщение отправленно!")

        # Запись информации о факте отправки сообщения в лог клиента с указанием времени
        logger.info(f"{current_datetime} - Сообщение отправлено в группу: {label_name_group.text}")

        # Ждём 3 секунды для того что бы сообщение точно отправилось
        time.sleep(4)

    driver.quit()


if __name__ == "__main__":
    main()
