
# Relatório de QA: Cadastro e Funcionalidade do Usuário (Versão Mobile)

## Desafio Quality Assurance
### Objetivo

Verificar a funcionalidade completa dos principais fluxos de interação da pessoa usuária no sistema Lacrei Saúde, garantindo que todas as etapas sejam concluídas corretamente e que não haja falhas ou bugs.

## Escopo
Este relatório abrange os seguintes fluxos de teste:

### 1. Cadastro da Pessoa Usuária
1. Acessar a página inicial do sistema.
2. Clicar no botão "Criar conta".
3. Preencher o formulário com dados válidos:
   - **Nome:** [Nome da Pessoa Usuária]
   - **Sobrenome:** [Sobrenome da Pessoa Usuária]
   - **E-mail:** [E-mail gerado pelo Guerrilla Mail]
   - **Senha:** [Senha definida]
   - **Confirmar Senha:** [Senha definida]
   - Aceitar os termos de serviço e confirmar maioridade.
4. Enviar o formulário e aguardar a confirmação por e-mail.

### 2. Pós Cadastro
1. Acessar o e-mail temporário criado no Guerrilla Mail.
2. Localizar e clicar no link de confirmação recebido.
3. Após a confirmação, retornar ao sistema Lacrei Saúde.
4. Realizar o login com os dados cadastrados anteriormente.
5. Completar o cadastro adicional se necessário.

### 3. Buscar Profissional
1. Após login, acessar a funcionalidade de busca de profissional.
2. Digitar "médico" na barra de pesquisa e pressionar Enter.
3. Verificar se a lista de profissionais é exibida corretamente.
4. Selecionar um profissional e verificar se as informações são precisas.
5. Validar se é possível interagir com as opções disponíveis para o profissional selecionado.

### 4. Contatar Profissional
1. Selecionar um profissional da lista de resultados da busca.
2. Clicar no botão "Atendimentos" para visualizar as opções de atendimento.
3. Clicar no botão "Exibir contato" para revelar as informações de contato do profissional.
4. Preencher o campo de telefone com um número válido.
5. Clicar no botão "Enviar código" para solicitar o código de confirmação.
6. Aguardar a chegada do código de confirmação, seja por SMS.
7. Digitar o código recebido no campo correspondente.
8. Clicar no botão "Confirmar" para completar o processo de confirmação.
   - Bug confirmado na etapa 8.

### 5. Edição do Perfil da Pessoa Usuária
1. Acessar a página de perfil da pessoa usuária.
2. Clicar no link "Editar Perfil".
3. Preencher os campos obrigatórios com novos dados:
   - Campo A: Insira um novo valor.
   - Campo B: Selecione uma opção válida.
   - Campo C: Atualize a data conforme especificado.
   - Campo D: Escolha uma opção do menu suspenso.
4. Clicar no botão "Salvar" ou equivalente para aplicar as alterações.

### 6. Recuperação de Senha
1. Abrir o navegador e acessar a URL do sistema de teste.
2. Navegar até a página inicial do site.
3. Clicar no link "Esqueci minha senha".
4. Preencher o campo de e-mail com um endereço válido.
5. Clicar no botão para enviar o link de recuperação.
6. Verificar se o e-mail foi recebido na caixa de entrada especificada.

### 7. Redefinição de Senha
1. Navegar até o link de redefinição de senha.
2. Preencher o formulário de redefinição com uma nova senha.
3. Submeter o formulário e verificar o sucesso da operação.


