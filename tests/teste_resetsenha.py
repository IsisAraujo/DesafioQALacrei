import json
import re
import time
from playwright.sync_api import sync_playwright
from guerrillamail import GuerrillaMailSession

def iniciar(playwright):
    iphone_12 = playwright.devices["iPhone 12"]
    navegador = playwright.webkit.launch(headless=False)
    contexto = navegador.new_context(**iphone_12, locale="pt-BR", record_video_dir="videos/")
    pagina = contexto.new_page()
    return navegador, pagina

def ler_link_confirmacao_do_arquivo():
    with open("email_body.txt", "r", encoding="utf-8") as file:
        conteudo = file.read()
        match = re.search(r'<p>Para redefinição, basta clicar no botão acima ou copiar o link a seguir no seu navegador:\s*<a\s+href="(https?://[^"]+)">', conteudo)
        if match:
            return match.group(1)
        else:
            return None

def executar_script_playwright(link):
    with sync_playwright() as playwright:
        navegador, pagina = iniciar(playwright)
        
        pagina.goto(link)
        pagina.wait_for_load_state("networkidle")
        
        # Preenchimento do formulário de cadastro
        pagina.get_by_placeholder("Digite a nova senha").fill("Lacrei123@")
        time.sleep(2)
        pagina.get_by_placeholder("Repita a nova senha").fill("Lacrei123@")
        time.sleep(2)
        pagina.get_by_role("button", name="Redefinir senha").click()
        time.sleep(5)
        
        navegador.close()

with open('credenciais.json', 'r') as f:
    credenciais = json.load(f)

email = credenciais.get('email', None)

if email:
    session = GuerrillaMailSession()
    session.set_email_address(email)
    email_list = session.get_email_list()
    if email_list:
        first_email_guid = email_list[0].guid
        print(f"First Email GUID: {first_email_guid}")
        email_content = session.get_email(first_email_guid)
        print("Email Subject:", email_content.subject)
        print("Email Sender:", email_content.sender)
        if hasattr(email_content, 'body'):
            print("Email Body:")
            print(email_content.body)
            with open("email_body.txt", "w", encoding="utf-8") as file:
                file.write(f"Email Subject: {email_content.subject}\n")
                file.write(f"Email Sender: {email_content.sender}\n")
                file.write("Email Body:\n")
                file.write(email_content.body)
            print("O corpo do email foi salvo em 'email_body.txt'.")
            link_confirmacao = ler_link_confirmacao_do_arquivo()
            if link_confirmacao:
                print("Link de confirmação encontrado:", link_confirmacao)
                executar_script_playwright(link_confirmacao)
            else:
                print("Link de confirmação não encontrado.")
        else:
            print("Corpo do email não encontrado.")
    else:
        print("Caixa de entrada vazia.")
else:
    print("Email não encontrado nas credenciais.")
