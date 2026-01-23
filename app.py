from selenium import webdriver;
from selenium.webdriver.common.by import By;
from selenium.webdriver.chrome.options import Options
import time as time
import re

class ControllerAPI:
	def __init__(self, username=None, number_badges=None, f=None):
		self.USER = username
		
	def varrerDadosAlura(self):
		try:
			# Configuração necessária para rodar dentro do GitHub Actions (sem interface gráfica)
			options = Options()
			options.add_argument("--headless=new")
			options.add_argument("--no-sandbox")
			options.add_argument("--disable-dev-shm-usage")
			
			driver = webdriver.Chrome(options=options)
			driver.get(f"https://cursos.alura.com.br/user/{self.USER}")
			driver.maximize_window() #ABRE COM A JENALA FULL
			driver.implicitly_wait(5) 
			#BARRA LATERAL AUTO SCROLL
			scroll = driver.execute_script('return document.body.scrollHeight')
			for contador in range(20):
				driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
				time.sleep(2)
				new_scroll = driver.execute_script('return document.body.scrollHeight')
				if new_scroll == scroll:
					break
				scroll = new_scroll

			# Clicar no 'Ver mais' se existir
			try:
				driver.find_element(By.XPATH, "(//button[@class='seeMoreButton'])[2]").click()
				time.sleep(1)
			except:
				pass

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

				taghtml.append(f'<a href="{html_da_href}"><img src="{html_da_src}" alt="{html_da_title}" width="60px" margin="5px"/></a>')

			self.atualizar_readme("\n".join(taghtml))
			print("README atualizado com sucesso!")
		
		except Exception as e:
			print(f"Erro ao varrer dados: {e}")
		finally:
			driver.quit

	def atualizar_readme(self, badges_html):
		# Marcadores que devem existir no seu README.md
		START_COMMENT = ""
		END_COMMENT = ""
		
		with open("README.md", "r", encoding="utf-8") as readFile:
			readme = readFile.read()

		# Regex para substituir o conteúdo entre os marcadores
		pattern = f"{START_COMMENT}[\\s\\S]+{END_COMMENT}"
		new_badges_section = f"{START_COMMENT}\n{badges_html}\n{END_COMMENT}"
		
		if re.search(pattern, readme, re.DOTALL):
			readme_atualizado = re.sub(pattern, new_badges_section, readme, flags=re.DOTALL)
			with open("README.md", "w", encoding="utf-8") as writeFile:
				writeFile.write(readme_atualizado)
		else:
			print("Erro: Marcadores não encontrados no README.md")