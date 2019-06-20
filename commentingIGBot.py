
# Script que comenta o username de três pessoas que segues
# Pré-requisitos:
#     - geckodriver(para Firefox) ou webdriver(para Edge) no PATH e, obviamente,
#       requer ter os browsers instalados;
#     - package numpy instalado;
#     - package selenium instalado;
#     - documento csv com os dados das pessoas que segues.
# Author: Ernesto González


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

import time
import random
import pandas as pd

# SELECIONAR BROWSER DE PREFERÊNCIA
#driver = webdriver.Edge()
driver = webdriver.Firefox()
# SELECIONAR TEMPO DE ESPERA (AUMENTAR PARA LIGAÇÕES LENTAS)
delay = 3


def extract_following(file_name):
    """Extrai os usernames do documento csv e devolve-os numa lista."""

    data = pd.read_csv(file_name)
    following = data['username'].values

    return following


class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = driver


    def closeBrowser(self):
        self.driver.close()


    def login(self):
        """Faz login na conta do utilizador escolhido."""
        self.driver.get("https://www.instagram.com/")

        time.sleep(delay)

        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()

        time.sleep(delay)

        user_name_elem = self.driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        password_elem = self.driver.find_element_by_xpath("//input[@name='password']")
        password_elem.clear()
        password_elem.send_keys(self.password)
        password_elem.send_keys(Keys.RETURN)

        time.sleep(delay)


    def comment(self, post_url, csv_file_name):
        """Comenta o nome de três perfis seguidos na publicação selecionada.
           post_url: endereço url da publicação onde se deseja comentar
           csv_file_name: nome do documento anexado com os dados sobre os seguindos
        """
        self.driver.get(post_url)

        time.sleep(delay)

        try:
            comment_button = lambda: self.driver.find_element_by_link_text('Comment')
            comment_button().click()
        except NoSuchElementException:
            pass

        try:
            comment_box_elem = lambda: self.driver.find_element_by_xpath("//textarea[@aria-label='Add a comment…']")
            comment_box_elem().click()
            comment_box_elem().send_keys('')
            comment_box_elem().clear()

            def friends_string_3():
                list_of_friends = extract_following(csv_file_name)
                random_friend_1 = random.randint(0,len(list_of_friends))
                random_friend_2 = random.randint(0,len(list_of_friends))
                random_friend_3 = random.randint(0,len(list_of_friends))

                return "@{} @{} @{}".format(list_of_friends[random_friend_1],list_of_friends[random_friend_2],list_of_friends[random_friend_3])

            comment_text = friends_string_3()
            for letter in comment_text:
                comment_box_elem().send_keys(letter)
                time.sleep((random.randint(1, 7) / 30))

        except StaleElementReferenceException and NoSuchElementException as e:
                    print(e)
                    return False

        post_comment_elem = self.driver.find_element_by_xpath("//button[@class='_0mzm- sqdOP yWX7d        ']")
        post_comment_elem.click()

        time.sleep(delay)


# USERNAME E PASSWORD ENTRE ASPAS
myBot = InstagramBot("USERNAME", "PASSWORD")
myBot.login()
time.sleep(delay)


try:
    while True:
        # ENDEREÇO URL DA PUBLICAÇÃO E FICHEIRO CSV ENTRE ASPAS
        myBot.comment("URL DA PUBLICAÇÃO","FILENAME")
except:
    pass
