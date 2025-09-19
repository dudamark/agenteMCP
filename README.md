MCP (Master of Customer Processes) Agent

Um agente inteligente de linha de comando para gerenciamento de clientes, combinando processamento de linguagem natural e interação com uma API.

🚀 Visão Geral
Este projeto é um Agente de Linha de Comando (CLI) que simplifica o gerenciamento de clientes. Em vez de interagir manualmente com uma API, o usuário pode usar comandos em linguagem natural, como "listar todos os clientes" ou "criar um novo cliente com nome João".

A aplicação é dividida em dois "cérebros":

Um agente de regras (agente_cliente.py), que processa comandos diretos e previsíveis usando expressões regulares.

Um modelo de linguagem local (LLM) (llm.py), que atua como um fallback inteligente para interpretar comandos mais complexos e ambíguos.

Essa arquitetura híbrida garante que a aplicação seja tanto precisa quanto flexível.

⚙️ Arquitetura e Componentes
A aplicação é modular e organizada em classes:

main.py: O ponto de entrada. Gerencia a autenticação JWT, inicializa os agentes e coordena o fluxo de comandos.

agente_cliente.py: O "cérebro" baseado em regras. Traduz comandos de linguagem natural para chamadas específicas da API.

llm.py: A camada de inteligência artificial. Carrega um modelo de linguagem local (EleutherAI/gpt-neo-125M) para interpretar a intenção do usuário quando o agente de regras não é suficiente.

api_client.py: A camada de comunicação. Abstrai a interação com a API de clientes, lidando com requisições HTTP e autenticação.

prerequisites
Antes de executar a aplicação, certifique-se de ter o Python 3.x instalado. Você também precisará de um servidor de API de clientes rodando em http://localhost:8000.

📦 Instalação
Clone o repositório:

Bash

git clone https://github.com/dudamark/
cd [NOME_DO_SEU_REPOSITORIO]
Instale as dependências necessárias:

Bash

pip install -r requirements.txt

Execute o arquivo principal a partir do terminal:

Bash

python main.py
A aplicação pedirá suas credenciais de usuário para autenticação.

📝 Comandos de Exemplo
Aqui estão alguns comandos que você pode testar:

Listar clientes:

listar clientes

quero ver a lista de clientes

Obter um cliente:

obter cliente id 1

buscar cliente de nome Ana

encontrar o cliente com email ana@exemplo.com

Criar um cliente:

criar novo cliente nome Maria email maria@exemplo.com telefone 12345678

Atualizar um cliente:

atualizar cliente id 20 nome Maria Silva

Deletar um cliente:

deletar o cliente 5

Limpar a tela:

limpar

clear

Sair da aplicação:

sair

exit

quit

Contribuição
Contribuições são bem-vindas! Se você tiver alguma ideia para melhorar o agente, sinta-se à vontade para abrir uma issue ou enviar um pull request.

📄 Licença
Este projeto está licenciado sob a Licença MIT.
