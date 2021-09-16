from time import sleep
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--window-size=1920,1080')
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])


province_dropdown = "digital-flyer-subscriptions-form__form__province__select"

accept_button = "input-checkbox__input"

submit_button = "digital-flyer-subscriptions-form__form__submit--button"


filename = "emails.txt"
filename2 = "used_emails.txt"

def get_emails(filename):
    # Retrieve emails from a list (emails should be using the dot trick)
    with open(filename) as f:
        data = f.readlines()

        emails_list = [] 
        for line in data:
            emails_list.append(line.strip("\n"))

    return emails_list

def write_emails(filename2, used_email):
    # Creates a new text file of emails that were used to sign up
    with open(filename2, 'a') as f:
        f.write(used_email + "\n")


def select_qc(driver):
    # Selects the Quebec option in the dropdown
    select = Select(driver.find_element_by_id('province'))
    select.select_by_value('QC')


def click_accept(driver, accept_button):
    # Clicks the accept checkbox
    driver.find_element_by_class_name(accept_button).click()


def submit(driver, submit_button):
    # Clicks the submit button to process to form
    driver.find_element_by_class_name(submit_button).click()


def enter_email(driver, email):
    # Enters the email retrieved from the parsed text file
    email_input = driver.find_element_by_id("email")
    email_input.clear()
    email_input.send_keys(email)


def main():
    counter = 0
    
    emails_list = get_emails(filename)
    list_len = len(emails_list)

    while list_len != counter:

        # prob dont need a new driver every time, change to refresh when i have time
        driver = webdriver.Chrome(executable_path="./chromedriver", options=chrome_options)
        url = "https://www.maxi.ca/digital-flyer-subscriptions?icta=weekly-flyer-signup-link&utm_campaign=na_05202021_Lcl-Mx-Q2-Acquisition-Ca-Fr&utm_medium=1PCC_ds&utm_source=Radio-Canada-ca&utm_term=na&utm_content=na_Display_Maxi-Sustain-Email-Acquisition-banane-300x6"
        driver.get(url)

        # increase if email addresses are skipping
        sleep(3.5)

        email = emails_list[counter]

        select_qc(driver)
        click_accept(driver, accept_button)
        enter_email(driver, email)
        submit(driver, submit_button)

        print("Registered for " + email)

        write_emails(filename2, email)

        counter += 1

    print("Submitted " + str(counter) + " times")

main()
