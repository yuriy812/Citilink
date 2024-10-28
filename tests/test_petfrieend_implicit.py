from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import setup_edge, USER_EMAIL, USER_PASSWORD  # Импортируйте переменные


def test_show_all_pets(setup_edge):
    driver = setup_edge
    driver.implicitly_wait(10)  # Устанавливаем неявное ожидание на 10 секунд
    driver.get("https://petfriends.skillfactory.ru/login")

    field_email = driver.find_element(By.ID, "email")
    field_email.clear()
    field_email.send_keys(USER_EMAIL)

    field_pass = driver.find_element(By.ID, "pass")
    field_pass.clear()
    field_pass.send_keys(USER_PASSWORD)

    btn_submit = driver.find_element(By.XPATH, "//button[@type='submit']")
    btn_submit.click()

    # Ждем, пока заголовок страницы станет видимым и проверяем его текст
    assert WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.TAG_NAME, 'h1'))).text == "PetFriends"

    # Получаем элементы с карточками питомцев
    images = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-img-top')
    names = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-title')
    descriptions = driver.find_elements(By.CSS_SELECTOR, '.card-deck .card-text')

    try:
        for image, name, description in zip(images, names, descriptions):
            img_src = image.get_attribute('src')
            print(f"Источник изображения: '{img_src}'")
            assert img_src != '', "Image source is empty"
            assert name.text != '', "Name is empty"
            assert description.text != '', "Description is empty"
            assert ', ' in description.text, "Description format is incorrect"
            parts = description.text.split(", ")
            assert len(parts) >= 2, "Description must contain at least two parts"
            assert len(parts[0]) > 0, "First part of description is empty"
            assert len(parts[1]) > 0, "Second part of description is empty"

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    print(f"Количество изображений: {len(images)}")
    print(f"Список имен питомцев: {['Питомец: ' + n.text for n in names]}")
    print(f"Список описаний: {['Описание: ' + d.text for d in descriptions]}")