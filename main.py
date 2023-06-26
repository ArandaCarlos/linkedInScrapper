import time
import json

from linkedin_scraper import Person, actions
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

driver = uc.Chrome()
#driver = webdriver.Chrome(executable_path="chromedriver.exe")

email = "INSERT YOU EMAIL"
password = "INSERT YOU PASS"
actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal

#person = Person("https://www.linkedin.com/in/andre-iguodala-65b48ab5", driver=driver)

# Define la lista de títulos de trabajo y industrias a buscar
job_titles = ['Shipping coordinators', 'Logistics coordinators', 'Supply chain managers', 'Shipping managers']
industries = ['Shipping and Logistics']

# Inicializa una lista vacía para almacenar los perfiles recolectados
list_full_text_job = []

# Recorre cada título de trabajo y industria
driver.get("https://www.linkedin.com/jobs/search/?currentJobId=3435550677&geoId=103644278&keywords=Shipping%20coordinators&location=Estados%20Unidos&refresh=true")
for job_title in job_titles:
    time.sleep(7)
    list_jobs = driver.find_elements(By.CLASS_NAME, "jobs-search-results__list-item")
    list_pagination = driver.find_elements(By.CLASS_NAME, "artdeco-pagination__indicator--number")
    index = 0
    actual_page = list_pagination[index]
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
                "title":title,
                "description": text_job
            }
            driver.find_elements(By.CLASS_NAME, "artdeco-pagination__indicator--number")
            list_full_text_job.append(content)
        except Exception as e:
            print(e)
    if index == 7:
        with open('data.json', 'w') as file:
            # Utiliza el argumento indent para especificar el nivel de identación
            json.dump(list_full_text_job, file, indent=4)
        break
    index = index + 1
with open('data.json', 'w') as file:
    # Utiliza el argumento indent para especificar el nivel de identación
    json.dump(list_full_text_job, file, indent=4)

