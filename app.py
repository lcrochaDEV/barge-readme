from selenium import webdriver;
from selenium.webdriver.common.by import By;
from datetime import datetime
import time as time
import re


class ControllerAPI:
	@staticmethod
	def varrerDadosAlura():
		try:
			#options = webdriver.ChromeOptions()
			#options.add_argument("--headless=new")
			#driver = webdriver.Chrome(options=options)
			driver = webdriver.Remote('http://192.168.1.252:4444', options=webdriver.ChromeOptions())
			#driver = webdriver.Chrome()
			driver.get("https://cursos.alura.com.br/user/guitarralcs")
			driver.maximize_window() #ABRE COM A JENALA FULL
			driver.implicitly_wait(5) 
			#BARRA LATERAL AUTO SCROLL
			scroll = driver.execute_script('return document.body.scrollHeight')
			for contador in range(200):
				driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
				time.sleep(2)
				new_scroll = driver.execute_script('return document.body.scrollHeight')
				if new_scroll == scroll:
					break
				scroll = new_scroll

			data_e_hora_atuais = datetime.now()
			data_e_hora_em_texto = data_e_hora_atuais.strftime('%d/%m/%Y')
			driver.find_element(By.XPATH, "(//button[@class='seeMoreButton'])[2]").click()
			taghtml = []
			# TAG IMG
			linkA = driver.find_elements(By.XPATH, "(//a[@class='course-card__certificate bootcamp-text-color'])")
			imgs = driver.find_elements(By.XPATH, "(//img[@class='course-card__icon'])")
			spans = driver.find_elements(By.XPATH, "(//span[@class='course-card__short-title'])")
			for linkA, img, span in  zip(linkA, imgs, spans):
				# Captura o HTML completo da tag
				html_da_href = linkA.get_attribute("href")
				html_da_src = img.get_attribute("src")
				html_da_title = span.get_attribute("textContent").replace(":", "")

				conteiner = f'''<a href="{html_da_href}"><img src="{html_da_src}" alt="{html_da_title}"/></a>'''
				taghtml.append(conteiner)

			return taghtml
			#print("\n".join(taghtml))
		except:	
			print(f'Sem acesso ao Site')
		finally:
			driver.quit
		

ControllerAPI.varrerDadosAlura()

