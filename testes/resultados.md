# Resultados

Os testes realizados demonstraram o funcionamento da API e dos mecanismos de segurança implementados.

## Teste 1 — Criação do cofre

Foi realizada a criação de um novo cofre utilizando uma senha-mestra.

### Resultado

- Cofre criado com sucesso.
- A API retornou o código `201 Created`.
- Foi gerado um identificador único para o cofre.

---

## Teste 2 — Validação da senha-mestra

Foi realizado um teste utilizando a senha-mestra correta e outro utilizando uma senha incorreta.

### Resultado

- A senha correta permitiu o acesso ao cofre.
- A senha incorreta retornou `401 Unauthorized`.
- A senha-mestra não é armazenada diretamente no banco de dados.

---

## Teste 3 — Criação de segredo

Foi criado um segredo contendo título, usuário, URL e senha.

### Resultado

- O segredo foi criado com sucesso.
- A API retornou `201 Created`.
- A senha foi criptografada antes de ser armazenada no banco de dados.

---

## Teste 4 — Armazenamento criptografado

Foi realizada uma consulta diretamente no banco de dados para verificar os dados armazenados.

### Resultado

- A senha não aparece em texto puro.
- O banco contém o criptograma, nonce e etiqueta de autenticação.
- Os valores criptográficos são armazenados em Base64.

---

## Teste 5 — Listagem de segredos

Foi realizada uma requisição para listar os segredos de um cofre.

### Resultado

- A API retornou `200 OK`.
- Foram retornados apenas os metadados dos segredos.
- A senha não é exibida na listagem.

---

## Teste 6 — Recuperação de segredo

Foi realizada uma requisição para consultar um segredo específico utilizando a senha-mestra correta.

### Resultado

- A senha-mestra foi validada.
- O segredo foi descriptografado com sucesso.
- A API retornou `200 OK`.

---

## Teste 7 — Nonce diferente

A mesma senha foi criptografada mais de uma vez.

### Resultado

- Cada criptografia gerou um nonce diferente.
- Os criptogramas também foram diferentes.

Isso demonstra que não é utilizado um nonce fixo nas operações de criptografia.

---

## Teste 8 — Alteração do criptograma

O criptograma armazenado no banco de dados foi alterado manualmente.

### Resultado

- A descriptografia falhou.
- A autenticação do AES-GCM detectou a alteração.
- A API retornou erro `500 Internal Server Error`.

Isso demonstra a proteção de integridade fornecida pelo AES-GCM.

---

## Teste 9 — Troca de dados entre segredos

Os dados criptográficos de dois segredos foram trocados no banco de dados.

### Resultado

- A descriptografia falhou.
- O AAD detectou que os dados pertenciam a outro segredo.
- A API retornou erro `500 Internal Server Error`.

Isso demonstra a utilização do AAD para associar os dados criptográficos ao `cofre_id` e ao `segredo_id`.

---

## Teste 10 — Atualização de segredo

Foi realizada a atualização de um segredo existente.

### Resultado

- O segredo foi atualizado com sucesso.
- A API retornou `200 OK`.
- A nova senha foi criptografada.
- Um novo nonce foi utilizado na criptografia.

---

## Teste 11 — Exclusão de segredo

Foi realizada a exclusão de um segredo existente.

### Resultado

- O segredo foi removido com sucesso.
- A API retornou `200 OK`.
- Após a exclusão, o segredo não apareceu mais na listagem.

---

# Resumo dos resultados

| Teste | Resultado |
|---|---|
| Criação do cofre | Sucesso |
| Validação da senha-mestra | Sucesso |
| Criação de segredo | Sucesso |
| Armazenamento criptografado | Sucesso |
| Listagem de segredos | Sucesso |
| Recuperação de segredo | Sucesso |
| Nonce diferente | Sucesso |
| Detecção de alteração do criptograma | Sucesso |
| Proteção por AAD | Sucesso |
| Atualização de segredo | Sucesso |
| Exclusão de segredo | Sucesso |

## Conclusão

Os testes realizados confirmaram o funcionamento das principais funcionalidades da API e dos mecanismos de segurança implementados.

A aplicação utiliza **PBKDF2-HMAC-SHA256** para derivação da chave e **AES-256-GCM** para criptografia dos segredos, utilizando salt e nonce aleatórios.

Também foi verificada a proteção de integridade dos dados por meio da autenticação do AES-GCM e do uso de AAD.
