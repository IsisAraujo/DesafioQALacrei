import json
import time
from playwright.sync_api import sync_playwright

def carregar_credenciais():
    with open("credenciais.json", "r") as file:
        credenciais = json.load(file)
        return credenciais["email"], credenciais["senha"]

def iniciar(playwright):
    iphone_12 = playwright.devices["iPhone 12"]
    navegador = playwright.webkit.launch(headless=False)
    contexto = navegador.new_context(**iphone_12, locale="pt-BR", record_video_dir="videos/")
    pagina = contexto.new_page()
    return pagina, navegador

def testar_reset_senha(pagina, email):
    pagina.goto("https://paciente-staging.lacreisaude.com.br/")
    pagina.wait_for_load_state("networkidle")
    
    # Aguarda até que o link "Esqueci minha senha" esteja visível e interagível
    pagina.get_by_role("link", name="Esqueci minha senha").click()
    time.sleep(2)
  
    pagina.wait_for_load_state("networkidle")
    pagina.get_by_placeholder("Digite seu e-mail").fill(email)
    pagina.get_by_text("Vamos enviar um link em seu e").click()
    pagina.click('button:has-text("Enviar link")')
    time.sleep(4)

def teste_fluxo_usuario():
    with sync_playwright() as playwright:
        pagina, navegador = iniciar(playwright)
        email, senha = carregar_credenciais()
        
        testar_reset_senha(pagina, email)
        
        navegador.close()

if __name__ == "__main__":
    teste_fluxo_usuario()
