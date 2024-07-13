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

def login(pagina, email, senha):
    pagina.goto("https://paciente-staging.lacreisaude.com.br/")
    time.sleep(2)
    pagina.get_by_placeholder("Digite seu e-mail").fill(email)
    pagina.get_by_placeholder("Digite sua senha").fill(senha)
    pagina.get_by_role("button", name="Entrar").click()
    time.sleep(1)

def editar_perfil(pagina):
    pagina.get_by_role("link", name="Foto de perfil").click()
    time.sleep(2)
    pagina.get_by_role("button", name="Editar dados").click()
    time.sleep(1)
    pagina.locator("div:nth-child(3) > .sc-c48c9750-1 > .sc-c48c9750-2 > .sc-c48c9750-3").first.click()
    pagina.locator("div:nth-child(5) > .sc-bda10a04-0 > div:nth-child(4) > .sc-c48c9750-1 > .sc-c48c9750-2 > .sc-c48c9750-3").click()
    pagina.locator("div:nth-child(7) > .sc-c48c9750-1 > .sc-c48c9750-2 > .sc-c48c9750-3").first.click()
    pagina.locator("div:nth-child(7) > .sc-bda10a04-0 > div:nth-child(6) > .sc-c48c9750-1 > .sc-c48c9750-2 > .sc-c48c9750-3").click()
    pagina.locator("span").filter(has_text="Motora").first.click()
    pagina.get_by_placeholder("Invalid Date").fill("1986-04-19")
    pagina.locator("//section[@class='alternative-section']//div[5]/div[2]/div/button[@type='button']").click()

    time.sleep(5)

def teste_fluxo_usuario():
    with sync_playwright() as playwright:
        pagina, navegador = iniciar(playwright)
        email, senha = carregar_credenciais()
        
        login(pagina, email, senha)
        editar_perfil(pagina)
        
        navegador.close()

if __name__ == "__main__":
    teste_fluxo_usuario()
