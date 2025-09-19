import requests

BASE_URL = "http://localhost:8000/interacoes/"

class InteracoesAPI:
    def __init__(self, token: str):
        self.headers = {"Authorization": f"Bearer {token}"}


    def listar(self):
        resp = requests.get(BASE_URL, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def obter(self, interacao_id: int):
        resp = requests.get(f"{BASE_URL}{interacao_id}", headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def criar(self, dados: dict):
        resp = requests.post(BASE_URL, json=dados, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def atualizar(self, interacao_id: int, dados: dict):
        resp = requests.put(f"{BASE_URL}{interacao_id}", json=dados, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def deletar(self, interacao_id: int):
        resp = requests.delete(f"{BASE_URL}{interacao_id}", headers=self.headers)
        resp.raise_for_status()
        return {"status": "Interação removida com sucesso"}