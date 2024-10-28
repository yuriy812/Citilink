from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import setup_edge, USER_EMAIL, USER_PASSWORD  # Импортируйте переменные
import time



def test_example(setup_edge):
    driver = setup_edge
    driver.get("https://petfriends.skillfactory.ru/")

    # Проверка заголовка страницы
    assert "PetFriends" in driver.title

def test_petfriends(setup_edge):
    # Open PetFriends base page:
    driver = setup_edge
    driver.get("https://petfriends.skillfactory.ru/")

    WebDriverWait(driver, 10).until(  # Увеличено время ожидания
        EC.presence_of_element_located((By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]"))
    )

    # click on the new user button
    btn_newuser = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[@onclick=\"document.location='/new_user';\"]")
        )
    )
    btn_newuser.click()

    # click existing user button
    btn_exist_acc = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, u"У меня уже есть аккаунт"))
    )
    btn_exist_acc.click()

    # add email
    field_email = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "email"))
    )
    field_email.clear()
    field_email.send_keys(USER_EMAIL)

    # add password
    field_pass = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "pass"))
    )
    field_pass.clear()
    field_pass.send_keys(USER_PASSWORD)

    # click submit button
    btn_submit = driver.find_element(By.XPATH, "//button[@type='submit']")
    btn_submit.click()

    # Явное ожидание, чтобы убедиться, что мы на нужной странице
    WebDriverWait(driver, 10).until(
        EC.url_contains('/all_pets')
    )

    if driver.current_url == 'https://petfriends.skillfactory.ru/all_pets':
        # Сохранение скриншота
        timestamp = int(time.time())  # Получаем текущую временную метку
        screenshot_filename = f'images/result_{timestamp}.png'
        driver.save_screenshot(screenshot_filename)
        print(f'Screenshot saved as: {screenshot_filename}')
    else:
        raise Exception("Login error: Current URL does not match expected.")