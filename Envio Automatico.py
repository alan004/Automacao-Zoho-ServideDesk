#importando biblioteca
import selenium
import time

#importando browser
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

#caminho do browser
PATH = 'C:\\chromedriver.exe'
driver = webdriver.Chrome(PATH)

#criar um driver passando a url a ser acessada
driver.get('https://sdpondemand.manageengine.com/app/itdesk/ui/requests')

try:
    #Faz login no sistema        
    def faz_login():
        email_login = driver.find_element(By.ID, 'login_id')
        email_login.send_keys('####') #preencher com seu email
        time.sleep(5)
        proximo_botao =  driver.find_element(By.ID, 'nextbtn')
        proximo_botao.click()
        time.sleep(5)        
        senha_login = driver.find_element(By.ID, 'password')
        senha_login.send_keys('####') #preencher com sua senha
        proximo_botao.click()
        time.sleep(15)
    faz_login()

    ##espera para a página carregar
    time.sleep(5)

    #Ação após logar no sistema
    ##encontra os chamados da lista com ícone de "sem resposta"
    table_rows = driver.find_elements(By.XPATH, "//tbody/tr[contains(.//div/@class, 'replyicon_null')]")
    ##Cria um loop para executar enquanto existirem itens da lista
    index = 0
    while index < len(table_rows):
        print(f'Selecionando a solicitação {index + 1} de {len(table_rows)}')
        time.sleep(3)
        ###recupera a lista para a segunda execução em diante
        table_rows = driver.find_elements(By.XPATH, "//tbody/tr[contains(.//div/@class, 'replyicon_null')]")
        while True:
            try:
                ##clica no item
                table_rows[index].click()
                break
            except StaleElementReferenceException:
                table_rows = driver.find_elements(By.XPATH, "//tbody/tr[contains(.//div/@class, 'replyicon_null')]")
        ##Comportamento para responder um chamado
        def responde_chamado():
            try:       
                botao_resposta = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.CLASS_NAME, 'reply-ico'))
                                )
                botao_resposta.click()
                menu_selecao = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.ID, 'replytemplate_selectspan'))
                                )
                menu_selecao.click()
                ##seleciona o segundo item da lista
                primeira_resposta = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.CSS_SELECTOR, "option[value='51970000001914001']"))#substituir value para o do modelo desejado
                                    )
                primeira_resposta.click()
                botao_sim = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Sim')]"))
                                )
                botao_sim.click()
                time.sleep(5)
                enviar_mensagem = WebDriverWait(driver, 10).until(
                                    EC.element_to_be_clickable((By.NAME, 'submit'))
                                )
                enviar_mensagem.click()
                time.sleep(10)
            except:
                    print("Não há mais chamados a serem respondidos!")    
        responde_chamado()
        ##index += 1 #O incremento aqui fazia com que o script pule um chamdo ao voltar para a lista por isso o removi.
        ##volta para a lista de chamados
        driver.get('https://sdpondemand.manageengine.com/app/itdesk/ui/requests')

finally:
    time.sleep(5)
    ##faz logoff da plataforma evitando que o número limete de sessões seja atingido
    botao_perfil = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, 'sdp_profile_popup'))
        )  
    botao_perfil.click()
    botao_sair = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Sair')]"))
        )
    botao_sair.click()
    time.sleep(5)
    driver.quit()