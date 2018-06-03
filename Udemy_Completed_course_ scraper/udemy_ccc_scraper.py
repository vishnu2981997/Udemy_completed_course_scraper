"""
Udemy_CCC_Extractor : Given proper user login details fetches the users completed course names.
"""
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def get_course_names(username, password):
    """
    :param username: Udemy username
    :param password: Password
    :return: A list containing the completed course names
    """

    course_names = []

    # Initializing the browser and logging in

    driver = webdriver.Firefox()

    url = 'https://www.udemy.com/'

    url = url+'join/login-popup/?next=/home/my-courses/learning/%3Fprogress_filter%3Dcompleted'

    driver.get(url)

    # Entering the email id

    link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "id_email")))
    ActionChains(driver).move_to_element(link).perform()
    link.send_keys(username)

    # Entering the password

    link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "id_password")))
    ActionChains(driver).move_to_element(link).perform()
    link.send_keys(password)

    # Submitting the logging in

    link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "submit-id-submit")))
    ActionChains(driver).move_to_element(link).perform()
    link.click()

    # Iterrating through multiple pages for all courses

    for i in range(1, 5):

        url = "https://www.udemy.com/home/my-courses/learning/?progress_filter=completed&p="+str(i)

        driver.get(url)

        # Fetching page source(html)

        html = driver.page_source
        soup = BeautifulSoup(html, "lxml")

        # Fetching completed course cards

        completed_courses = soup.find("body").find_all("div", {"class" : "card card--learning"})

        # Fetching completed course names

        for course in completed_courses:

            course_names.append(course.find("strong").string)

    return course_names

def gen_text(course_names):
    """
    :param course_names: list of strings
    :return: Null
    """

    with open("result.txt", "w") as file:

        if course_names:

            for name in course_names:

                file.write(name)
                file.write("\n")

            file.write("\n")

    file.close()

def main():
    """
    :return: Null
    """
    username = input("E-Mail   : ")
    password = input("Password : ")

    course_names = get_course_names(username, password)

    gen_text(course_names)

if __name__ == "__main__":
    main()
