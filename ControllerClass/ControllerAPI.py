from selenium import webdriver;
from selenium.webdriver.common.by import By;
from selenium.webdriver.chrome.options import Options
import time as time
import re

from settings import LIST_REGEX # Import local para usar o padrão definido

class ControllerAPI:
	def __init__(self, number_badges=16, start_section="", end_section=""):
		self.START_SECTION = start_section
		self.END_SECTION = end_section
		self.number_badges = number_badges

		# Configuração necessária para rodar dentro do GitHub Actions (sem interface gráfica)
		self.options = Options()
		self.options.add_argument("--headless=new")
		self.options.add_argument("--no-sandbox")
		self.options.add_argument("--disable-dev-shm-usage")
		
		self.driver = webdriver.Chrome(options=self.options)
		
	def varrerDadosAlura(self, USER=None):
		try:
			# Configuração necessária para rodar dentro do GitHub Actions (sem interface gráfica)
			#options = Options()
			#options.add_argument("--headless=new")
			#options.add_argument("--no-sandbox")
			#options.add_argument("--disable-dev-shm-usage")
			
			#driver = webdriver.Chrome(options=options)
			self.driver.get(f"https://cursos.alura.com.br/user/{USER}")
			self.driver.maximize_window() #ABRE COM A JENALA FULL
			self.driver.implicitly_wait(5) 
			#BARRA LATERAL AUTO SCROLL
			scroll = self.driver.execute_script('return document.body.scrollHeight')
			for contador in range(20):
				self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
				time.sleep(2)
				new_scroll = self.driver.execute_script('return document.body.scrollHeight')
				if new_scroll == scroll:
					break
				scroll = new_scroll

			# Clicar no 'Ver mais' se existir
			try:
				self.driver.find_element(By.XPATH, "(//button[@class='seeMoreButton'])[2]").click()
				time.sleep(1)
			except:
				pass

			taghtml = []
			# TAG IMG
			linkA = self.driver.find_elements(By.XPATH, "(//a[@class='course-card__certificate bootcamp-text-color'])")
			imgs = self.driver.find_elements(By.XPATH, "(//img[@class='course-card__icon'])")
			spans = self.driver.find_elements(By.XPATH, "(//span[@class='course-card__short-title'])")
			spans_subs = self.driver.find_elements(By.XPATH, "//span[@class='course-card__name']")
			for linkA, img, span, span_sub in  zip(linkA, imgs, spans, spans_subs):
				# Captura o HTML completo da tag
				html_da_href = linkA.get_attribute("href")
				html_da_src = img.get_attribute("src")
				html_da_title = span.get_attribute("textContent").replace(":", "")
				html_p = img.get_attribute("innerText").strip()

				tag = self.criateTagHTML(html_da_href, html_da_src, html_da_title, html_p)
				taghtml.append(tag)

			if not taghtml:
				return ""
			
			LIMITE_VISIVEL = 13
			
			# As primeiras 13 badges
			exibicao_direta = taghtml[:LIMITE_VISIVEL]
			
			# O restante (da 14ª em diante)
			exibicao_oculta = taghtml[LIMITE_VISIVEL:]

			if exibicao_oculta:
				# Criamos o bloco expansível
				bloco_expandivel = [
					"\n<details>",
					f"  <summary><b>🔍 Ver mais {len(exibicao_oculta)} certificados...</b></summary>",
					*exibicao_oculta, # O '*' desempacota a lista aqui dentro
					"</details>\n"
				]
				# Unimos as badges visíveis com o bloco que abre/fecha
				resultado_final = exibicao_direta + bloco_expandivel
			else:
				# Se tiver menos de 13, apenas a lista normal
				resultado_final = exibicao_direta

			print(f"Sucesso! {len(taghtml)} badges processadas.")
			return "\n".join(resultado_final)
		except Exception as e:
			print(f"Erro ao varrer dados: {e}")
			return ""
		#finally:
		#	self.driver.quit()

	def finalizar(self):
		"""Encerra o driver apenas quando todas as varreduras acabarem."""
		self.driver.quit()

	def criateTagHTML(self, html_da_href, html_da_src, html_da_title, html_p):
		return f'''<a href="{html_da_href}" target="_blank" rel="noopener noreferrer"><img src="{html_da_src}" title="{html_da_title}" alt="{html_da_title}" width="60px" style="margin: 5px;"/></a>'''

	def varrerDadosCredly(self, USER=None):
		try:
			self.driver.get(f"https://www.credly.com/users/{USER}/badges#credly")
			self.driver.maximize_window() #ABRE COM A JENALA FULL
			self.driver.implicitly_wait(5) 
			#BARRA LATERAL AUTO SCROLL
			scroll = self.driver.execute_script('return document.body.scrollHeight')
			for contador in range(20):
				self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
				time.sleep(2)
				new_scroll = self.driver.execute_script('return document.body.scrollHeight')
				if new_scroll == scroll:
					break
				scroll = new_scroll

			taghtml = []
			# TAG IMG
			linkA = self.driver.find_elements(By.XPATH, "(//div[@data-testid='desktop-badge-card']/@href)")
			imgs = self.driver.find_elements(By.XPATH, "(//div[@data-testid='desktop-badge-card']//img)")
			spans = self.driver.find_elements(By.XPATH, "(//span[@data-testid='Typography'])")
			for linkA, img, span in  zip(linkA, imgs, spans):
				# Captura o HTML completo da tag
				html_da_href = linkA.get_attribute("href")
				html_da_src = img.get_attribute("src")
				html_da_title = span.get_attribute("textContent")
				html_p = img.get_attribute("innerText").strip()

				tag = self.credlyTagHTML(html_da_href, html_da_src, html_da_title, html_p)
				taghtml.append(tag)

			if not taghtml:
				return ""
			
			LIMITE_VISIVEL = 13
			
			# As primeiras 13 badges
			exibicao_direta = taghtml[:LIMITE_VISIVEL]
			
			# O restante (da 14ª em diante)
			exibicao_oculta = taghtml[LIMITE_VISIVEL:]

			if exibicao_oculta:
				# Criamos o bloco expansível
				bloco_expandivel = [
					"\n<details>",
					f"  <summary><b>🔍 Ver mais {len(exibicao_oculta)} certificados...</b></summary>",
					*exibicao_oculta, # O '*' desempacota a lista aqui dentro
					"</details>\n"
				]
				# Unimos as badges visíveis com o bloco que abre/fecha
				resultado_final = exibicao_direta + bloco_expandivel
			else:
				# Se tiver menos de 13, apenas a lista normal
				resultado_final = exibicao_direta

			print(f"Sucesso! {len(taghtml)} badges processadas.")
			return "\n".join(resultado_final)
		except Exception as e:
			print(f"Erro ao varrer dados: {e}")
			return ""
		#finally:
		#	self.driver.quit()
		
	def credlyTagHTML(self, html_da_href, html_da_src, html_da_title, html_p):
		return f'''<a href="{html_da_href}" target="_blank" rel="noopener noreferrer"><img src="{html_da_src}" title="{html_da_title}" alt="{html_da_title}" width="100px" style="margin: 5px;"/></a>'''

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
		
	def varrerDadosGeneric(self, url=None, XPATH_a=None, XPATH_b=None, XPATH_c=None):
		try:
			self.driver.get(url)
			self.driver.maximize_window() #ABRE COM A JENALA FULL
			self.driver.implicitly_wait(5) 
			#BARRA LATERAL AUTO SCROLL
			scroll = self.driver.execute_script('return document.body.scrollHeight')
			for contador in range(20):
				self.driver.execute_script('window.scrollBy(0, document.body.scrollHeight);')
				time.sleep(2)
				new_scroll = self.driver.execute_script('return document.body.scrollHeight')
				if new_scroll == scroll:
					break
				scroll = new_scroll

			taghtml = []
			# TAG IMG
			linkA = self.driver.find_elements(By.XPATH, XPATH_a)
			imgs = self.driver.find_elements(By.XPATH, XPATH_b)
			spans = self.driver.find_elements(By.XPATH, XPATH_c)
			for linkA, img, span in  zip(linkA, imgs, spans):
				# Captura o HTML completo da tag
				html_da_href = linkA.get_attribute("href")
				html_da_src = img.get_attribute("src")
				html_da_title = span.get_attribute("textContent").replace(":", "")
				html_p = img.get_attribute("innerText").strip()

				tag = self.criateTagHTML(html_da_href, html_da_src, html_da_title, html_p)
				taghtml.append(tag)

			if not taghtml:
				return ""
			
			LIMITE_VISIVEL = 13
			
			# As primeiras 13 badges
			exibicao_direta = taghtml[:LIMITE_VISIVEL]
			
			# O restante (da 14ª em diante)
			exibicao_oculta = taghtml[LIMITE_VISIVEL:]

			if exibicao_oculta:
				# Criamos o bloco expansível
				bloco_expandivel = [
					"\n<details>",
					f"  <summary><b>🔍 Ver mais {len(exibicao_oculta)} certificados...</b></summary>",
					*exibicao_oculta, # O '*' desempacota a lista aqui dentro
					"</details>\n"
				]
				# Unimos as badges visíveis com o bloco que abre/fecha
				resultado_final = exibicao_direta + bloco_expandivel
			else:
				# Se tiver menos de 13, apenas a lista normal
				resultado_final = exibicao_direta

			print(f"Sucesso! {len(taghtml)} badges processadas.")
			return "\n".join(resultado_final)
		except Exception as e:
			print(f"Erro ao varrer dados: {e}")
			return ""
		#finally:
		#	self.driver.quit()
		

