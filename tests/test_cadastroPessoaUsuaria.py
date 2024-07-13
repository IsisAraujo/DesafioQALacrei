import re
import time
import json  

from guerrillamail import GuerrillaMailSession
from playwright.sync_api import sync_playwright

def criar_email_temporario():
    session = GuerrillaMailSession()
    email_teste = session.get_session_state()['email_address']
    print(f"E-mail temporário criado: {email_teste}")
    return email_teste, session

def salvar_credenciais(email_teste, senha):
    credenciais = {
        "email": email_teste,
        "senha": senha
    }
    with open("credenciais.json", "w") as file:
        json.dump(credenciais, file)

def buscar_email_confirmacao(session):
    email_content = None
    while not email_content:
        email_list = session.get_email_list()
        for email in email_list:
            if "[sandbox] Confirme sua conta na Lacrei Saúde" in email.subject or "suporte.staging@lacreisaude.com.br" in email.sender:
                email_content = session.get_email(email.guid)
                break
        if not email_content:
            time.sleep(5)  # Aguarda 5 segundos antes de verificar novamente
    # Salvar o corpo do email em um arquivo .txt
    with open("email_body.txt", "w", encoding="utf-8") as file:
        file.write(f"Email Subject: {email_content.subject}\n")
        file.write(f"Email Sender: {email_content.sender}\n")
        file.write("Email Body:\n")
        file.write(email_content.body)
    return email_content

def ler_link_confirmacao_do_arquivo():
    with open("email_body.txt", "r", encoding="utf-8") as file:
        conteudo = file.read()
        # Encontrar o link de confirmação após a frase específica
        match = re.search(r'<p[^>]*>\s*Para confirmação, basta clicar no botão ou copiar o link no seu navegador:\s*<a\s+href="(https?://\S+)">', conteudo, re.DOTALL)
        if match:
            link_confirmacao = match.group(1)
            return link_confirmacao
        else:
            raise ValueError("Link de confirmação não encontrado no corpo do e-mail.")

def iniciar(playwright):
    iphone_12 = playwright.devices["iPhone 12"]
    navegador = playwright.webkit.launch(headless=False)
    contexto = navegador.new_context(**iphone_12, locale="pt-BR", record_video_dir="videos/")
    pagina = contexto.new_page()
    return pagina, navegador

def teste_fluxo_usuario():
    with sync_playwright() as playwright:
        email_teste, session = criar_email_temporario()
        senha = "Teste123@"  # Defina sua senha aqui
        
        # Salvar as credenciais em um arquivo JSON
        salvar_credenciais(email_teste, senha)
        
        pagina, navegador = iniciar(playwright)
        
        pagina.goto("https://paciente-staging.lacreisaude.com.br/")
        
        # Preenchimento do formulário de cadastro
        pagina.get_by_role("button", name="Criar conta").click()
        pagina.get_by_placeholder("Digite seu nome civil ou").fill("Isis")
        pagina.get_by_placeholder("Digite seu sobrenome").fill("Ferreira Araujo")
        pagina.get_by_placeholder("Digite seu e-mail").fill(email_teste)
        pagina.get_by_placeholder("Digite sua senha").fill(senha)
        pagina.get_by_placeholder("Confirme sua senha").fill(senha)
        pagina.locator("label").filter(has_text="Li e concordo com os Termos e").locator("span").nth(1).click()
        pagina.locator("label").filter(has_text="Tenho 18 anos ou mais").locator("span").nth(1).click()
        pagina.locator('button.sc-43e2db29-1.fgDeQn.button[type="submit"]').click()
        time.sleep(5)
        
        # Buscar email de confirmação
        buscar_email_confirmacao(session)
        
        # Ler o link de confirmação do arquivo
        confirmation_link = ler_link_confirmacao_do_arquivo()
        
        # Abrir link de confirmação
        pagina.goto(confirmation_link)
        time.sleep(5)
        
        # Pós Cadastro (login)
        pagina.get_by_placeholder("Digite seu e-mail").fill(email_teste)
        pagina.get_by_placeholder("Digite sua senha").fill(senha)
        pagina.get_by_role("button", name="Entrar").click()
        pagina.get_by_role("button", name="Continuar cadastro").click()
        pagina.locator(".sc-c48c9750-3").first.click()
        pagina.get_by_role("button", name="Próximo").click()
        pagina.locator("div:nth-child(3) > .sc-c48c9750-1 > .sc-c48c9750-2 > .sc-c48c9750-3").click()
        pagina.get_by_role("button", name="Próximo").click()
        pagina.locator("div:nth-child(7) > .sc-c48c9750-1 > .sc-c48c9750-2 > .sc-c48c9750-3").click()
        pagina.get_by_role("button", name="Próximo").click()
        pagina.locator("div:nth-child(8) > .sc-c48c9750-1 > .sc-c48c9750-2 > .sc-c48c9750-3").click()
        pagina.get_by_role("button", name="Próximo").click()
        pagina.locator("div").filter(has_text=re.compile(r"^Não possuo deficiência$")).nth(3).click()
        pagina.get_by_role("button", name="Concluir").click()
        pagina.get_by_role("button", name="Buscar profissional").click()
        
        pagina.locator("#search").fill("medico")
        pagina.locator("#search").press("Enter")
        time.sleep(5)
        
        navegador.close()

if __name__ == "__main__":
    teste_fluxo_usuario()
