from selenium import webdriver
import pandas as pd
import sched, time

URL = "https://www.saopaulo.sp.gov.br/"
VACINOMETRO_CLASS_NAME="container-numeros-vacinados"
DATE_CLASS_NAME="data-atualizacao-vac"

vacinados = pd.read_csv("vacinados.csv")
s = sched.scheduler(time.time, time.sleep)

def get_vacinados(driver):
    element = driver.find_element_by_class_name(VACINOMETRO_CLASS_NAME)
    text = element.text.replace(".", "")
    return int(text)


def get_data(driver):
    element = driver.find_element_by_class_name(DATE_CLASS_NAME)
    text = element.text.split(":")[1].strip()
    return text


def fetch_data(vacinados):
    driver = webdriver.Chrome()
    driver.get(URL)
    new_data = {"Data": [get_data(driver)], "Vacinados":[get_vacinados(driver)]}
    driver.close()
    print(new_data)
    vacinados = vacinados.append(pd.DataFrame(new_data), ignore_index=True)
    vacinados.to_csv("vacinados.csv", index=False)
    s.enter(300, 1, fetch_data, (vacinados,))


s.enter(300, 1, fetch_data, (vacinados,))
s.run()
