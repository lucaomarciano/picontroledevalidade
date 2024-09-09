Gestão Inteligente e Sustentável de Validade de Produtos
Descrição
Este projeto é um sistema de gerenciamento de produtos focado em supermercados, projetado para automatizar o controle de validade dos itens em estoque. Ele envia alertas via SMS sobre produtos que estão próximos do vencimento, ajudando a reduzir o desperdício de produtos e a otimizar o gerenciamento de estoque.

Funcionalidades
Cadastro de produtos com descrição, código de barras e data de validade.
Edição e exclusão de produtos.
Listagem de produtos próximos da data de vencimento.
Envio automático de notificações via SMS usando Twilio.
Sistema de autenticação (login/registro) com hash de senha (Bcrypt).
Interface web acessível e fácil de usar.

Tecnologias Utilizadas
Backend: Flask (Python)
Banco de Dados: SQLite
Autenticação: Flask-Login, Flask-Bcrypt
Frontend: HTML5, CSS3, JavaScript
Notificações: Twilio API
Hospedagem: Render
Controle de Versão: GitHub

Requisitos
Para rodar o projeto, você precisará das seguintes ferramentas instaladas:

Python 3.x (https://www.python.org/downloads/)
Flask (https://flask.palletsprojects.com/)
SQLite (https://www.sqlite.org/)
Twilio (https://www.twilio.com/)
Git (https://git-scm.com/)

Instalação
Clone o repositório:
git clone https://github.com/lucaomarciano/picontroledevalidade.git
cd projeto-validade-produtos

Crie um ambiente virtual e ative-o:
python -m venv venv
source venv/bin/activate  # No Windows, use venv\Scripts\activate

Instale as dependências:
pip install -r requirements.txt

Configure as variáveis de ambiente: Crie um arquivo .env na raiz do projeto e adicione suas credenciais do Twilio e a chave secreta:
SECRET_KEY=your_secret_key
TWILIO_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number

Inicialize o banco de dados:
Crie o banco de dados e as tabelas:
python
>>> from app import create_users_table
>>> create_users_table()
>>> exit()

Executando o Projeto
Rodando o servidor localmente:
flask run
Abra o navegador e acesse http://127.0.0.1:5000.

Uso do Sistema
Página de Login: Faça login com seu nome de usuário e senha.
Adicionar Produto: Insira descrição, código de barras e data de validade.
Notificações por SMS: Produtos próximos da validade (10 dias antes) serão enviados via SMS.
Gerenciamento: Liste, edite ou exclua produtos existentes.

Deploy
Para hospedar seu projeto em um servidor, como no Render, siga os seguintes passos:

Crie um arquivo Procfile:
web: flask run
Configuração no Render:

Faça o deploy do repositório no Render (https://render.com) e adicione as variáveis de ambiente configuradas no arquivo .env.

Contribuindo
Se você quiser contribuir com este projeto:

Faça um fork do projeto.
Crie uma branch para sua feature (git checkout -b feature/nova-feature).
Faça o commit das suas mudanças (git commit -m 'Adiciona nova feature').
Faça o push para a branch (git push origin feature/nova-feature).
Abra um Pull Request.

Licença
Este projeto é licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

Autores
LUCAS RIBEIRO MARCIANO DOS SANTOS
