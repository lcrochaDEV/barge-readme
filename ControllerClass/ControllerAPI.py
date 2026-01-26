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
			spans_subs = driver.find_elements(By.XPATH, "//span[@class='course-card__name']/text()[1]")
			for linkA, img, span, span_sub in  zip(linkA, imgs, spans, spans_subs):
				# Captura o HTML completo da tag
				html_da_href = linkA.get_attribute("href")
				html_da_src = img.get_attribute("src")
				html_da_title = span.get_attribute("textContent").replace(":", "")
				html_p = span_sub.get_attribute("innerText")
				print(html_p)
				taghtmlReturn = self.criateTagHTML(html_da_href, html_da_src, html_da_title, html_p)
				taghtml.append(taghtmlReturn)

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
		
	def criateTagHTML(self, html_da_href, html_da_src, html_da_title, html_p):
		return f'''\
			<div style="border-radius: 5px; width: 60px; height: 60px; margin: 5px; background-color: rgb(130, 58, 203); color: aliceblue; font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;">
				<img src="https://capsule-render.vercel.app/api?type=waving&color=gradient&height=200&section=header" style="width: 60px; border-top-left-radius: 5px; border-top-right-radius: 5px; position: absolute; z-index:0;"/>
				<div class="alura" style="display: flex; position: relative; z-index:1; padding: 3px 3px; position: relative; z-index:1;">
					<a href="{html_da_href}"><img src="{html_da_src}" title="{html_da_title}" alt="{html_da_title}" style="width: 25px;"/></a>
					<img src="https://cursos.alura.com.br/assets/images/logos/logo-alura.svg" style="width: 20px; filter: brightness(0) invert(1); margin: 0 5px; position: relative; top: 3px"/>
				</div>
				<img src="https://capsule-render.vercel.app/api?type=waving&color=000000&height=410&section=header" style="width: 60px; border-top-left-radius: 5px; border-top-right-radius: 5px; transform: rotate(180deg); position: absolute; z-index:0;"/>
				<h4 style="font-size: 6px; position: relative; bottom: 16px; margin: 10px 25px;">{html_da_title}</h4>
				<p style="font-size: 6px; text-align: left; position: relative; bottom: 20px; z-index: 1; padding-left: 3px; text-shadow: 5px 5px 0 rgba(130, 58, 203, 0.578); overflow-wrap: break-word; word-wrap: break-word; line-height: 1.1;">{html_p}</p>
			</div>
		'''
		