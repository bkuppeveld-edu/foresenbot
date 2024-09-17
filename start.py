from datetime import timedelta, date
import datetime
import holidays
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import easygui
import os
import PySimpleGUI as sg
from keyboard import press

sg.set_options(font=("Arial Bold", 12))
sg.theme("Reddit")

rb = [
    sg.Text("Voer start datum in naar format DD-MM-YYYY"),
    sg.InputText(key="startDate"),
    sg.Text("Voer eind datum in naar format DD-MM-YYYY"),
    sg.InputText(key="eindDate"),
]

rlo = sg.Frame("Automatisch data aanmaken", [rb], title_color="blue")

instructie = [
    [
        sg.Text(
            "Welkom bij de automatisering van de forensen en thuiswerk vergoedingen."
        )
    ],
    [
        sg.Text(
            "de applicatie zal een browser starten waarin je moet inloggen op AFAS. "
        )
    ],
    [sg.Text("voor het inloggen en authenticaten heb je 45 seconden de tijd. ")],
    [sg.Text("de applicatie zal de browser sluiten als de data is ingevoerd. ")],
    [sg.Text("Bart Kuppeveld ROC Team SD\n")],
]

actions = [[sg.Button("Stop"), sg.Button("Start"), sg.Button("Lijst")]]

layout = [[instructie], [rlo], [actions]]


def write_workdays(start_date, end_date):
    # Define the holiday calendar for the current year
    holiday_calendar = holidays.CountryHoliday("NL", years=datetime.date.today().year)

    # Open a text file for writing
    filename = "forensen_data.txt"
    with open(filename, "w") as file:
        # Iterate over each day between start date and end date
        delta = datetime.timedelta(days=1)
        while start_date <= end_date:
            # If the current date is a workday, write it to the file
            if start_date.weekday() < 5 and start_date not in holiday_calendar:
                file.write(start_date.strftime("%d-%m-%Y") + "\n")
            start_date += delta

    print(f"Successfully wrote workdays to {filename}")


# Prompt the user for a start and end date


# Call the write_workdays function to write all workdays to a text file


def login_afas():
    browser = webdriver.Edge()

    browser.get("https://86210.afasinsite.nl/")
    browser.maximize_window()

    # wait for redirect ->surf
    time.sleep(10)

    # click 'mijnInsite'
    clickElement = browser.find_element(By.ID, "P_H_W_Menu_T_1_ctl01")
    clickElement.click()

    # wait for redirect ->Afas
    time.sleep(3)

    # click 'declaratie portaal'
    clickElement = browser.find_element(
        By.ID,
        "P_C_W_9470B8BA4DA0EAE9C7EFABBA711231C0_W_60086B3F484752EA2B18BCA46EF6A803_Content",
    )
    clickElement.click()

    # wait for redirect ->Afas
    time.sleep(3)

    # click 'forensen'
    clickElement = browser.find_element(
        By.XPATH, "//a[@_anta_linkid='E110D11D4289EB99CBF02AA7FE45AF69']"
    )
    clickElement.click()

    # wait for redirect ->decla
    time.sleep(2)

    # click 'dienstverband'
    inputElement = browser.find_element(
        By.ID, "Window_0_Verzameldeclaratie_HrZ82a_EnSe"
    )
    inputElement.send_keys("1")

    # lees forens data
    with open("forensen_data.txt", "r") as f:
        forens = [i.strip() for i in f.readlines()]

    for datum in forens:
        time.sleep(5)
        # click 'forensenbeweging'
        clickElement = browser.find_element(
            By.ID, "Window_0_F3481E3D44517B20843ECA94560DFB60_action_new"
        )
        clickElement.click()

        time.sleep(5)

        # datum invoeren
        inputElement = browser.find_element(
            By.XPATH, "//input[@data-title='Datum boeking']"
        )
        inputElement.send_keys(datum)
        time.sleep(2)
        # periode invoeren, maar eerst select en delete
        # inputElement = browser.find_element(By.CLASS_NAME, "typeahead__input-dummy")
        # typeahead-item__description-wrapper
        inputElement = browser.find_element(By.XPATH, "//div[@class='typeahead__value']")
        inputElement.click()
        time.sleep(1)
        inputElement = browser.find_element(By.XPATH, "//input[@placeholder='Typ om te zoeken...']")
        time.sleep(1)
        
        # maand (periode) uit datum peuteren
        periode = datum.split("-")
        periodeVar = periode[1].replace("0", "")
        inputElement.send_keys(periodeVar)
        time.sleep(1)
        clickDropdown = browser.find_element(By.XPATH, "//div[@class='content-menu__item']")

        clickDropdown.click()
 

        # aanmaken
        clickElement = browser.find_element(By.XPATH, "//button[@id='Window_1_Actions_AntaUpdateCloseWebForm']")
        browser.execute_script("arguments[0].click();", clickElement)
        time.sleep(2)
        clickElement.click()



    # lees thuiswerk data

    print("That's All Folks!")

    window.close()


# Create the window
window = sg.Window("Forensen APP", layout)
sg.theme("LightBlue2")

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "Stop" or event == sg.WIN_CLOSED:
        break

    if event == "Start":
        login_afas()

    if event == "Lijst":
        event, values = window.Read()
        start_date_str = values["startDate"]
        end_date_str = values["eindDate"]
        start_date = datetime.datetime.strptime(start_date_str, "%d-%m-%Y").date()
        end_date = datetime.datetime.strptime(end_date_str, "%d-%m-%Y").date()
        write_workdays(start_date, end_date)
