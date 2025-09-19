from llm import LocalLLM
from api_client import ClienteAPI

class MCPAgent:
    def __init__(self):
        self.llm = LocalLLM()
        self.api = ClienteAPI()

    def processar_comando(self, comando: str):
        """
        Usa o LLM para interpretar o comando do usuário
        e decidir qual operação de CRUD executar.
        """
        prompt = f"""
        Você é um assistente que gerencia clientes via API.
        Comando: {comando}
        Responda em JSON no formato:
        {{"acao": "listar|obter|criar|atualizar|deletar", "dados": ...}}
        """
        resposta = self.llm.chat(prompt)
        print("🔎 LLM output:", resposta)

        # Aqui entraria um parser robusto (regex/json) para extrair a ação e dados
        # Exemplo fictício:
        if "listar" in resposta.lower():
            return self.api.listar()
        elif "obter" in resposta.lower():
            return self.api.obter(1)
        elif "criar" in resposta.lower():
            return self.api.criar({"nome": "João", "email": "joao@email.com"})
        else:
            return {"erro": "Não entendi o comando"}
