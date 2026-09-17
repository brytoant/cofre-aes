# Cofre de Senhas Corporativo

API para armazenamento seguro de credenciais utilizando AES-256-GCM e PBKDF2-HMAC-SHA256.

## Tecnologias

- Python 3.10+
- FastAPI
- PyCryptodome
- Supabase
- PostgreSQL

## Segurança

- AES-256-GCM para criptografia das senhas
- PBKDF2-HMAC-SHA256 com 210.000 iterações
- Salt aleatório de 16 bytes por cofre
- Nonce aleatório de 12 bytes a cada criptografia
- AAD associando cada segredo ao seu cofre
- Senha-mestra e chave derivada não são armazenadas
- Dados sensíveis não são registrados em logs

## Estrutura

```text
cofre-aes/
├── app/
│   ├── __init__.py
│   ├── banco.py
│   ├── cripto.py
│   ├── main.py
│   └── modelos.py
├── .env.exemplo
├── .gitignore
├── README.md
└── requirements.txt
# API Cofre AES

## Configuração

Crie um arquivo `.env` na raiz do projeto:

```env
SUPABASE_URL=sua_url_do_supabase
SUPABASE_KEY=sua_chave_do_supabase
```

> **Importante:** o arquivo `.env` não deve ser enviado ao GitHub.

---

## Instalação

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

### No Windows

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## Executando a API

Execute o seguinte comando:

```bash
uvicorn app.main:app --reload
```

A documentação da API estará disponível em:

**http://127.0.0.1:8000/docs**

---

## Endpoints

### Cofres

| Método | Endpoint                   | Descrição      |
| ------ | -------------------------- | -------------- |
| POST   | `/cofres`                  | Criar um cofre |
| POST   | `/cofres/{cofre_id}/abrir` | Abrir um cofre |

### Segredos

| Método | Endpoint                                   | Descrição            |
| ------ | ------------------------------------------ | -------------------- |
| POST   | `/cofres/{cofre_id}/segredos`              | Criar um segredo     |
| GET    | `/cofres/{cofre_id}/segredos`              | Listar os segredos   |
| GET    | `/cofres/{cofre_id}/segredos/{segredo_id}` | Consultar um segredo |
| PUT    | `/cofres/{cofre_id}/segredos/{segredo_id}` | Alterar um segredo   |
| DELETE | `/cofres/{cofre_id}/segredos/{segredo_id}` | Excluir um segredo   |

---

## Testes de segurança realizados

* Verificação de armazenamento criptografado no banco.
* Nonce diferente para criptografias repetidas.
* Senha-mestra incorreta retorna `401`.
* Alteração do criptograma é detectada.
* Troca de dados criptográficos entre segredos é rejeitada pelo AAD.

---

## Resumo

Este README cobre:

* Configuração do projeto.
* Instalação das dependências.
* Execução da API.
* Estrutura dos endpoints.
* Principais requisitos de segurança.
* Testes de segurança realizados.

