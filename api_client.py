import requests

BASE_URL = "http://localhost:8000/clientes/"

class ClienteAPI:
    def __init__(self, token: str):
        self.headers = {"Authorization": f"Bearer {token}"}

    def listar(self):
        resp = requests.get(BASE_URL, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def obter(self, cliente_id: int):
        resp = requests.get(f"{BASE_URL}{cliente_id}", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def criar(self, dados: dict):
        resp = requests.post(BASE_URL, json=dados, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def atualizar(self, cliente_id: int, dados: dict):
        resp = requests.put(f"{BASE_URL}{cliente_id}", json=dados, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def deletar(self, cliente_id: int):
        resp = requests.delete(f"{BASE_URL}{cliente_id}", headers=self.headers)
        resp.raise_for_status()
        return {"status": "Cliente removido com sucesso"}

    def buscar_por_nome(self, nome: str):
        resp = requests.get(BASE_URL, params={"nome": nome}, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def buscar_por_email(self, email: str):
        resp = requests.get(BASE_URL, params={"email": email}, headers=self.headers)
        resp.raise_for_status()
        return resp.json()
