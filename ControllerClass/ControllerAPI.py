from selenium import webdriver;
from selenium.webdriver.common.by import By;
from selenium.webdriver.chrome.options import Options
import time as time
import re

from settings import LIST_REGEX # Import local para usar o padrão definido

class ControllerAPI:
	def __init__(self, username=None, start_section="", end_section="", number_badges=16):
		self.USER = username
		self.START_SECTION = start_section
		self.END_SECTION = end_section
		self.number_badges = number_badges
		
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
			abriu_details = False
			for i, (linkA, img, span) in enumerate(zip(linkA, imgs, spans)):
				if i >= self.number_badges:
					break
				if i == 13:
					taghtml.append('\n<details>\n<summary><b>Ver mais certificados...</b></summary>\n')
					abriu_details = True
		
					# Captura o HTML completo da tag
					html_da_href = linkA.get_attribute("href")
					html_da_src = img.get_attribute("src")
					html_da_title = span.get_attribute("textContent").replace(":", "")

				taghtml.append(f'<a href="{html_da_href}"><img src="{html_da_src}" title="{html_da_title}" alt="{html_da_title}" width="60px" margin="5px"/></a>')
			
			if abriu_details:
				taghtml.append('\n</details>')
			# Aplica o limite de badges definido no seu main.py (self.number_badges)
			if hasattr(self, 'number_badges') and self.number_badges > 0:
				taghtml = taghtml[:self.number_badges]

			if taghtml:
				# Aplica o limite vindo do construtor
				badges_limitadas = taghtml[:self.number_badges] 
				
				print(f"Sucesso! {len(badges_limitadas)} badges atualizadas.")
				return "\n".join(badges_limitadas)
				##return self.atualizar_readme("\n".join(badges_limitadas))

		except Exception as e:
			print(f"Erro ao varrer dados: {e}")
		finally:
			driver.quit()

	def atualizar_readme(self, badges_html):
			
		with open("README.md", "r", encoding="utf-8") as readFile:
			readme = readFile.read()

		new_badges_section = f"{self.START_SECTION}\n{badges_html}\n{self.END_SECTION}"

		# Regex para substituir o conteúdo entre os marcadores
		pattern = f"{self.START_SECTION}[\\s\\S]*?{self.END_SECTION}"
					
		if re.search(LIST_REGEX, readme):
			readme_atualizado = re.sub(LIST_REGEX, new_badges_section, readme)
			with open("README.md", "w", encoding="utf-8") as writeFile:
				writeFile.write(readme_atualizado)
			print("README atualizado!")
			return readme_atualizado
		else:
			print("Erro: Marcadores não encontrados no README.md")
			return pattern