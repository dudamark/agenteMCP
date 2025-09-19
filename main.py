from llm import LocalLLM
from api_client import ClienteAPI
from agente_cliente import AgenteCliente
import requests
import json
import threading
import getpass
import textwrap
import os

# Função auxiliar para obter token JWT
def obter_token(username: str, password: str) -> str:
    url = "http://localhost:8000/token"
    data = {"username": username, "password": password}
    
    try:
        resp = requests.post(url, data=data)
        resp.raise_for_status()
        return resp.json()["access_token"]
    except requests.exceptions.HTTPError as e:
        # Se a resposta de erro tiver um corpo JSON, extraímos a mensagem de erro.
        try:
            error_detail = e.response.json().get('detail', 'Erro de autenticação desconhecido.')
        except (json.JSONDecodeError, AttributeError):
            error_detail = 'Credenciais inválidas ou serviço indisponível.'
        
        # Levanta uma nova exceção com uma mensagem mais clara.
        raise ValueError(f"❌ Erro de autenticação: {error_detail}")
    except requests.exceptions.RequestException as e:
        # Captura outros erros de requisição, como problemas de conexão.
        raise ConnectionError(f"❌ Erro de conexão com o servidor de token: {e}")

class MCPAgent:
    def __init__(self, token: str):
        print("🔄 Inicializando LLM...")
        self.llm = LocalLLM()
        print("✅ LLM pronto!")
        self.api = ClienteAPI(token)
        self.agente_cliente = AgenteCliente(self.api)

    def processar_comando(self, comando: str):
        comando_lower = comando.lower()

        # Tenta processar o comando com os agentes
        resultado = self.agente_cliente.processar_comando(comando)
        
        # Se o agente de cliente não processou o comando, tenta com a LLM
        if resultado is None:
            prompt = f"""
            Sou um assistente que gerencia clientes via API.
            Comando: {comando}
            Responda indicando qual ação deve ser tomada (listar, criar, atualizar, obter, deletar)
            e forneça dados se necessário no formato JSON.
            """
            resposta = None

            def gerar_resposta():
                nonlocal resposta
                resposta = self.llm.chat(prompt)

            thread = threading.Thread(target=gerar_resposta)
            thread.start()

            while thread.is_alive():
                print("🤖 LLM processando...", end="\r")
                thread.join(0.5)

            print(" " * 30, end="\r")

            # Limpa e exibe a resposta da LLM de forma legível
            resposta_formatada = textwrap.dedent(resposta).strip()
            print("🔎 LLM output:")
            print(resposta_formatada)
            return {"LLM_output": resposta_formatada}
        else:
            return resultado

if __name__ == "__main__":
    while True:
        try:
            username = input("Usuário para autenticação JWT: ")
            password = getpass.getpass("Senha: ")
            
            # Tenta obter o token
            token = obter_token(username, password)
            
            # Se o token for obtido com sucesso, sai do loop
            break
        except (ValueError, ConnectionError) as e:
            # Se houver um erro de autenticação ou conexão, exibe a mensagem amigável
            print(e)
            print("Tente novamente.\n")

    # A partir daqui, o token já foi obtido e o programa continua
    agent = MCPAgent(token)
    print("🤖 MCP Agent iniciado. Digite 'sair' para encerrar.\n")
    print("Comandos especiais: 'limpar' para limpar a tela.")

    while True:
        comando = input(">> ")

         # Lógica para o novo comando de limpeza
        if comando.lower() in ["limpar", "clear"]:
            os.system('cls' if os.name == 'nt' else 'clear')
            continue # Pula o resto do loop e pede o próximo comando

        if comando.lower() in ["sair", "exit", "quit"]:
            break
        resultado = agent.processar_comando(comando)
        if "LLM_output" in resultado:
            pass
        else:
            print(json.dumps(resultado, indent=2, ensure_ascii=False))