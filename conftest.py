import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# Глобальные переменные для аутентификации
USER_EMAIL = 'sitecadilac@mail.ru'
USER_PASSWORD = '7qQ3xJnOEwoNTBBXltpr'
@pytest.fixture
def edge_options():
    options = Options()
    options.add_argument('-foreground')  # Запуск в переднем плане
    return options


@pytest.fixture
def setup_edge(edge_options):
    driver_path = 'E:\\proect python 3\\edgedriver_win64\\msedgedriver.exe'
    service = Service(driver_path)
    driver = webdriver.Edge(service=service, options=edge_options)
    driver.set_window_size(1440, 900)  # Установка размера окна
    yield driver
    driver.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep

@pytest.fixture
def web_browser(setup_edge):
    return setup_edge

def test_example(web_browser):
    web_browser.get("https://www.example.com")

    # Добавляем задержку по времени
    wait = WebDriverWait(web_browser, 10)
    element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div > div:nth-of-type(2)")))

    # Продолжаем тестирование
    assert "card-deck" in web_browser.element.get_attribute("class")
