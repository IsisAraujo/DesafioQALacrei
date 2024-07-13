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

def preencher_codigo(pagina, codigo):
    for i, digito in enumerate(codigo):
        pagina.locator(f".sc-4614c78e-2:nth-child({i + 1})").fill(digito)
        time.sleep(1)

def login(pagina, email, senha):
    pagina.goto("https://paciente-staging.lacreisaude.com.br/")
    time.sleep(2)
    pagina.get_by_placeholder("Digite seu e-mail").fill(email)
    pagina.get_by_placeholder("Digite sua senha").fill(senha)
    time.sleep(1)
    pagina.get_by_role("button", name="Entrar").click()
    time.sleep(2)

def buscar_profissional(pagina):
    pagina.locator("#search").fill("medico")
    time.sleep(1)
    pagina.locator("#search").press("Enter")
    time.sleep(2)
    
    pagina.get_by_role("link", name="Lucas Pelusi").click()
    time.sleep(1)
    pagina.get_by_text("Atendimentos").click()
    time.sleep(1)
    pagina.get_by_role("button", name="Exibir contato").click()
    time.sleep(1)

    pagina.get_by_placeholder("(99) 99999-").fill("79935001474")
    time.sleep(1)
    pagina.get_by_role("button", name="Enviar código").click()
    time.sleep(2)

    codigo_confirmacao = input("Digite o código de confirmação (6 dígitos): ")
    preencher_codigo(pagina, codigo_confirmacao)
    time.sleep(1)
    pagina.get_by_role("button", name="Confirmar").click()
    time.sleep(1)
    
    mensagem_erro = pagina.get_by_text("Código incorreto. Verifique").inner_text()
    if "Código incorreto. Verifique" in mensagem_erro:
        print("BUG ENCONTRADO: A mensagem de erro 'Código incorreto. Verifique' foi exibida.")
    else:
        print("Nenhum bug encontrado ao verificar o código de confirmação.")
    
    time.sleep(2)

def teste_fluxo_usuario():
    with sync_playwright() as playwright:
        pagina, navegador = iniciar(playwright)
        email, senha = carregar_credenciais()
        
        login(pagina, email, senha)
        buscar_profissional(pagina)
        
        navegador.close()

if __name__ == "__main__":
    teste_fluxo_usuario()
