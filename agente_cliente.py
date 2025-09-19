import re
import requests
from api_client import ClienteAPI

class AgenteCliente:
    def __init__(self, api_client: ClienteAPI):
        self.api = api_client

    def processar_comando(self, comando: str) -> dict:
        """
        Processa comandos específicos para a API de clientes e retorna o resultado.
        """
        # Extrai ID do comando
        match_id = re.search(r"\b\d+\b", comando)
        cliente_id = int(match_id.group()) if match_id else None
        comando_lower = comando.lower()

        try:
            if "listar" in comando_lower:
                return self.api.listar()

            elif "obter" in comando_lower:
                cliente_id = None
                nome = None
                email = None

                match_id = re.search(r"id\s+(\d+)", comando, re.IGNORECASE)
                if match_id:
                    cliente_id = match_id.group(1)

                match_nome = re.search(r"nome\s+(.+?)(?=\s+email|$)", comando, re.IGNORECASE)
                if match_nome:
                    nome = match_nome.group(1).strip()

                match_email = re.search(r"email\s+([\w\.\-_]+@[\w\.\-_]+)", comando, re.IGNORECASE)
                if match_email:
                    email = match_email.group(1).strip()

                try:
                    if cliente_id:
                        return self.api.obter(cliente_id)
                    elif nome:
                        return self.api.buscar_por_nome(nome)
                    elif email:
                        return self.api.buscar_por_email(email)
                    else:
                        return {"erro": "Não foi possível identificar ID, nome ou email do cliente."}
                except requests.exceptions.HTTPError as e:
                    if e.response.status_code == 404:
                        return {"erro": "Cliente não encontrado."}
                    else:
                        raise

            elif "criar" in comando_lower:
                dados = {}
                match_nome = re.search(r"nome\s+(.+?)(?=\s+email|\s+telefone|\s+endereco|$)", comando, re.IGNORECASE)
                match_email = re.search(r"email\s+([\w\.\-_]+@[\w\.\-_]+)", comando, re.IGNORECASE)
                match_telefone = re.search(r"telefone\s+([\(\)\d\s\-]+)", comando, re.IGNORECASE)
                match_endereco = re.search(r"endereco\s+(.+)", comando, re.IGNORECASE)

                if match_nome:
                    dados["nome"] = match_nome.group(1).strip()
                if match_email:
                    dados["email"] = match_email.group(1).strip()
                if match_telefone:
                    dados["telefone"] = match_telefone.group(1).strip()
                if match_endereco:
                    dados["endereco"] = match_endereco.group(1).strip()

                if not dados:
                    return {"erro": "Nenhum dado válido foi informado para criar o cliente."}

                return self.api.criar(dados)

            elif "atualizar" in comando_lower:
                if cliente_id:
                    dados = {}
                    match_nome = re.search(r"nome\s+([\w\s]+)", comando, re.IGNORECASE)
                    match_email = re.search(r"email\s+([\w\.\-_]+@[\w\.\-_]+)", comando, re.IGNORECASE)

                    if match_nome:
                        dados["nome"] = match_nome.group(1).strip()
                    if match_email:
                        dados["email"] = match_email.group(1).strip()

                    if not dados:
                        return {"erro": "Nenhum campo para atualizar foi identificado."}

                    return self.api.atualizar(cliente_id, dados)
                else:
                    return {"erro": "Não foi possível identificar o ID do cliente"}

            elif "deletar" in comando_lower:
                if cliente_id:
                    try:
                        return self.api.deletar(cliente_id)
                    except requests.exceptions.HTTPError as e:
                        if e.response.status_code == 404:
                            return {"erro": f"Cliente com ID {cliente_id} não encontrado."}
                        else:
                            raise
                else:
                    return {"erro": "Não foi possível identificar o ID do cliente"}
            else:
                return None
        except Exception as e:
            return {"erro": str(e)}