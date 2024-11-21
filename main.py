from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

def get_paragraphs(driver):
    """Получить список параграфов текущей статьи."""
    paragraphs = driver.find_elements("css selector", "p")
    return [p.text for p in paragraphs if p.text.strip()]

def list_paragraphs(paragraphs):
    """Листать параграфы текущей статьи."""
    for idx, paragraph in enumerate(paragraphs):
        print(f"\nПараграф {idx + 1}:")
        print(paragraph)
        next_action = input("\nНажмите Enter, чтобы продолжить, или 'q' для выхода из листания: ")
        if next_action.lower() == 'q':
            break

def get_internal_links(driver):
    """Получить список внутренних ссылок."""
    links = driver.find_elements("css selector", "#mw-content-text a")
    internal_links = [(link.text, link.get_attribute("href")) for link in links if link.get_attribute("href") and "wikipedia.org/wiki" in link.get_attribute("href")]
    return internal_links

def list_internal_links(internal_links):
    """Отобразить список связанных страниц."""
    print("\nДоступные внутренние страницы:")
    for idx, (title, url) in enumerate(internal_links[:10]):  # Показать только первые 10 ссылок
        print(f"{idx + 1}. {title} ({url})")
    return internal_links

def navigate_to_internal_link(driver, link):
    """Перейти по внутренней ссылке."""
    driver.get(link)
    time.sleep(3)

def search_wikipedia():
    # Запрашиваем у пользователя ввод для поиска
    query = input("Введите запрос для поиска на Википедии: ")

    # Указываем путь к драйверу браузера
    #driver_path = "path/to/chromedriver"  # Замените на путь к вашему драйверу
    driver = webdriver.Chrome()

    try:
        # Переходим на сайт Википедии
        driver.get("https://www.wikipedia.org/")

        # Находим поле ввода для поиска
        search_box = driver.find_element("id", "searchInput")

        # Вводим запрос и нажимаем Enter
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        # Ждем загрузки страницы
        time.sleep(3)

        while True:
            print("\n--- Меню ---")
            print("1. Листать параграфы текущей статьи.")
            print("2. Перейти на одну из связанных страниц.")
            print("3. Выйти из программы.")

            choice = input("Выберите действие (1, 2 или 3): ")

            if choice == "1":
                # Листать параграфы
                paragraphs = get_paragraphs(driver)
                if paragraphs:
                    list_paragraphs(paragraphs)
                else:
                    print("Нет доступных параграфов для отображения.")

            elif choice == "2":
                # Показать связанные страницы
                internal_links = get_internal_links(driver)
                if not internal_links:
                    print("Нет доступных связанных страниц.")
                    continue

                internal_links = list_internal_links(internal_links)
                link_choice = input("\nВведите номер страницы, чтобы перейти, или 'q' для возврата в меню: ")
                if link_choice.lower() == 'q':
                    continue

                try:
                    link_index = int(link_choice) - 1
                    if 0 <= link_index < len(internal_links):
                        navigate_to_internal_link(driver, internal_links[link_index][1])
                    else:
                        print("Неверный выбор.")
                except ValueError:
                    print("Пожалуйста, введите число.")

            elif choice == "3":
                print("Спасибо за использование программы! Выход.")
                break

            else:
                print("Неверный выбор. Пожалуйста, попробуйте снова.")

    except Exception as e:
        print(f"Произошла ошибка: {e}")

    finally:
        # Закрываем браузер
        driver.quit()

# Запуск программы
if __name__ == "__main__":
    search_wikipedia()
