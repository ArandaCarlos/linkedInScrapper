import time
import json

from linkedin_scraper import Person, actions
import undetected_chromedriver as uc
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

driver = uc.Chrome()
# driver = webdriver.Chrome(executable_path="chromedriver.exe")

# Define la lista de títulos de trabajo y industrias a buscar
job_titles = ['Shipping coordinators', 'Logistics coordinators', 'Supply chain managers', 'Shipping managers']
industries = ['Shipping and Logistics']
location = "United States"

# Inicializa una lista vacía para almacenar los perfiles recolectados
list_full_text_job = []


def logIn(email, password):
    actions.login(driver, email, password)  # if email and password isnt given, it'll prompt in terminal


# Acceder a sección Jobs y buscar por Keyword y Location
def searchJob(keywords, location):
    search_emp = driver.find_element(By.CLASS_NAME, 'search-global-typeahead__input')
    search_emp.click()
    search_emp.send_keys(keywords)
    search_emp.send_keys(Keys.ENTER)
    time.sleep(7)
    driver.find_element(By.XPATH, '//button[text()="Jobs"]').click()
    time.sleep(7)
    location_elem = driver.find_element(By.XPATH, '/html/body/div[5]/header/div/div/div/div[2]/div[2]/div/div/input[1]')
    location_elem.click()
    location_elem.clear()
    location_elem.send_keys(location)
    location_elem.send_keys(Keys.ENTER)


# Recorre cada título de trabajo y industria

def run(email, user):
    logIn(email, user)
    time.sleep(7)
    for job_title in job_titles:
        searchJob(job_title, location)
        time.sleep(4)
        index = 0
        # guardamos url actual para avanzar por las paginas
        current_url = driver.current_url
        list_pagination = driver.find_elements(By.CLASS_NAME, "artdeco-pagination__indicator--number")
        count_pages = int(list_pagination[-1].text)
        # recorre todas las paginas de los resultados
        for page in range(1, count_pages - 1):
            time.sleep(5)
            list_jobs = driver.find_elements(By.CLASS_NAME, "jobs-search-results__list-item")

            for jobs in list_jobs:
                try:
                    driver.execute_script("arguments[0].scrollIntoView();", jobs)
                    title = jobs.find_element(By.CLASS_NAME, "job-card-list__title").text
                    time.sleep(2)
                    tab_title = driver.title
                    list_tabs = driver.current_window_handle
                    try:
                        jobs.find_element(By.CLASS_NAME, 'job-card-list__title').click()
                    except:
                        print("error jobs.findElement")
                        jobs.click()
                    time.sleep(2)
                    if tab_title != driver.title:
                        print()
                        driver.execute_script("window.history.go(-1)")
                        time.sleep(3)
                        driver.execute_script("arguments[0].scrollIntoView();", jobs)
                        title = jobs.find_element(By.CLASS_NAME, "job-card-list__title").text
                    text_job = driver.find_element(By.CLASS_NAME, "jobs-details__main-content").text
                    content = {
                        "title": title,
                        "description": text_job
                    }
                    list_full_text_job.append(content)
                except Exception as e:
                    print("excepción")
                    print(e)

            time.sleep(7)
            # list_pagination[page].click()
            index += 25
            # actualiza la url y avanza a la siguiente pagina
            driver.get(current_url + '&start=' + str(index))

        with open('data.json', 'w') as file:
            # Utiliza el argumento indent para especificar el nivel de identación
            json.dump(list_full_text_job, file, indent=4)
        break
    with open('data.json', 'w') as file:
        # Utiliza el argumento indent para especificar el nivel de identación
        json.dump(list_full_text_job, file, indent=4)


run("INSERT_YOU_EMAIL", "INSERT_YOU_USER")
