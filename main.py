import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC



MESSAGE = "Сообщение в группу"
USER_LIST = "users.txt"

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


def main():
    options = webdriver.ChromeOptions()
    options.add_argument(r"--user-data-dir=D:\newdir")
    options.add_argument(r'--profile-directory=Profile')
    service = Service(executable_path="C:\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=options)

    users_and_links = create_user_dict_from_file(USER_LIST)
    print(users_and_links)

    for user_name, link in users_and_links.items():
        driver.get(link)
        # Ожидание загрузки страницы
        selector = (By.CSS_SELECTOR, "#main > footer > div._2lSWV._3cjY2.copyable-area")
        if not wait_for_element(driver, selector, max_wait_time=60, retry_interval=20):
            print("Элемент не был найден после максимального времени ожидания.")
            continue

        input_box = driver.find_element(By.CSS_SELECTOR,
                                        "#main > footer > div._2lSWV._3cjY2.copyable-area > div > span:nth-child(2) > div > div._1VZX7 > div._3Uu1_ > div.g0rxnol2.ln8gz9je.lexical-rich-text-input > div.to2l77zo.gfz4du6o.ag5g9lrv.bze30y65.kao4egtt")
        input_box.send_keys(MESSAGE)


        label_name_group = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "#main > header > div._2au8k > div._6u0RM > div > span")))
        print(f"В группу: {label_name_group.text} - Сообщение отправленно!")962


        input_box.send_keys(Keys.RETURN)
        time.sleep(2)

    driver.quit()


if __name__ == "__main__":
    main()
