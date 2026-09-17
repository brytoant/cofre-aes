from fastapi import FastAPI, Header, HTTPException, status
from uuid import uuid4

from app.cripto import (
    derivar_chave,
    gerar_sal,
    criar_verificador,
    senha_mestra_correta,
    cifrar,
    decifrar,
    para_b64,
    de_b64,
    criar_aad_segredo
)

from app.banco import (
    criar_cofre,
    buscar_cofre,
    criar_segredo,
    listar_segredos,
    buscar_segredo,
    atualizar_segredo,
    excluir_segredo
)

from app.modelos import (
    CofreCriar,
    SegredoCriar,
    SegredoResposta,
    SegredoLista
)

app = FastAPI(title="Cofre AES")

@app.post("/cofres", status_code=status.HTTP_201_CREATED)
def criar_novo_cofre(dados: CofreCriar):
    cofre_id = str(uuid4())
    sal = gerar_sal()
    chave = derivar_chave(
        dados.senha_mestra,
        sal,
        210_000
    )

    nonce, criptograma, etiqueta = criar_verificador(
        chave,
        cofre_id
    )

    cofre = criar_cofre({
        "id": cofre_id,
        "nome": dados.nome,
        "kdf_sal": para_b64(sal),
        "kdf_iteracoes": 210_000,
        "verificador_nonce": nonce,
        "verificador_criptograma": criptograma,
        "verificador_etiqueta": etiqueta
    })

    return {"id": cofre["id"]}

@app.post("/cofres/{cofre_id}/abrir")
def abrir_cofre(
    cofre_id: str,
    x_senha_mestra: str = Header(...)
):
    cofre = buscar_cofre(cofre_id)

    if not cofre:
        raise HTTPException(
            status_code=404,
            detail="cofre não encontrado"
        )

    sal = de_b64(cofre["kdf_sal"])

    chave = derivar_chave(
        x_senha_mestra,
        sal,
        cofre["kdf_iteracoes"]
    )

    correta = senha_mestra_correta(
        chave,
        cofre["verificador_nonce"],
        cofre["verificador_criptograma"],
        cofre["verificador_etiqueta"],
        cofre_id
    )

    if not correta:
        raise HTTPException(
            status_code=401,
            detail="senha-mestra incorreta"
        )

    return {"mensagem": "cofre aberto"}

@app.post("/cofres/{cofre_id}/segredos", status_code=status.HTTP_201_CREATED)
def criar_novo_segredo(
    cofre_id: str,
    dados: SegredoCriar,
    x_senha_mestra: str = Header(...)
):
    cofre = buscar_cofre(cofre_id)

    if not cofre:
        raise HTTPException(
            status_code=404,
            detail="cofre não encontrado"
        )

    sal = de_b64(cofre["kdf_sal"])

    chave = derivar_chave(
        x_senha_mestra,
        sal,
        cofre["kdf_iteracoes"]
    )

    correta = senha_mestra_correta(
        chave,
        cofre["verificador_nonce"],
        cofre["verificador_criptograma"],
        cofre["verificador_etiqueta"],
        cofre_id
    )

    if not correta:
        raise HTTPException(
            status_code=401,
            detail="senha-mestra incorreta"
        )

    segredo_id = str(uuid4())

    aad = criar_aad_segredo(
        cofre_id,
        segredo_id
    )

    nonce, criptograma, etiqueta = cifrar(
        chave,
        dados.senha,
        aad
    )

    segredo = criar_segredo({
        "id": segredo_id,
        "cofre_id": cofre_id,
        "titulo": dados.titulo,
        "usuario": dados.usuario,
        "url": dados.url,
        "nonce": nonce,
        "criptograma": criptograma,
        "etiqueta": etiqueta
    })

    return {"id": segredo["id"]}

@app.get("/cofres/{cofre_id}/segredos", response_model=list[SegredoLista])
def listar_segredos_do_cofre(
    cofre_id: str,
    x_senha_mestra: str = Header(...)
):
    cofre = buscar_cofre(cofre_id)

    if not cofre:
        raise HTTPException(
            status_code=404,
            detail="cofre não encontrado"
        )

    sal = de_b64(cofre["kdf_sal"])

    chave = derivar_chave(
        x_senha_mestra,
        sal,
        cofre["kdf_iteracoes"]
    )

    correta = senha_mestra_correta(
        chave,
        cofre["verificador_nonce"],
        cofre["verificador_criptograma"],
        cofre["verificador_etiqueta"],
        cofre_id
    )

    if not correta:
        raise HTTPException(
            status_code=401,
            detail="senha-mestra incorreta"
        )

    return listar_segredos(cofre_id)

@app.get(
    "/cofres/{cofre_id}/segredos/{segredo_id}",
    response_model=SegredoResposta
)
def obter_segredo(
    cofre_id: str,
    segredo_id: str,
    x_senha_mestra: str = Header(...)
):
    cofre = buscar_cofre(cofre_id)

    if not cofre:
        raise HTTPException(
            status_code=404,
            detail="cofre não encontrado"
        )

    segredo = buscar_segredo(cofre_id, segredo_id)

    if not segredo:
        raise HTTPException(
            status_code=404,
            detail="segredo não encontrado"
        )
    sal = de_b64(cofre["kdf_sal"])

    chave = derivar_chave(
        x_senha_mestra,
        sal,
        cofre["kdf_iteracoes"]
    )

    correta = senha_mestra_correta(
    chave,
    cofre["verificador_nonce"],
    cofre["verificador_criptograma"],
    cofre["verificador_etiqueta"],
    cofre_id
    )

    if not correta:
        raise HTTPException(
            status_code=401,
            detail="senha-mestra incorreta"
        )

    aad = criar_aad_segredo(
    cofre_id,
    segredo_id
    )

    senha = decifrar(
        chave,
        segredo["nonce"],
        segredo["criptograma"],
        segredo["etiqueta"],
        aad
    )

    return {
    "id": segredo["id"],
    "titulo": segredo["titulo"],
    "usuario": segredo["usuario"],
    "url": segredo["url"],
    "senha": senha
}

@app.put(
    "/cofres/{cofre_id}/segredos/{segredo_id}",
    response_model=SegredoResposta
)
def atualizar_um_segredo(
    cofre_id: str,
    segredo_id: str,
    dados: SegredoCriar,
    x_senha_mestra: str = Header(...)
):
    cofre = buscar_cofre(cofre_id)

    if not cofre:
        raise HTTPException(
            status_code=404,
            detail="cofre não encontrado"
        )

    segredo = buscar_segredo(cofre_id, segredo_id)

    if not segredo:
        raise HTTPException(
            status_code=404,
            detail="segredo não encontrado"
        )

    sal = de_b64(cofre["kdf_sal"])

    chave = derivar_chave(
        x_senha_mestra,
        sal,
        cofre["kdf_iteracoes"]
    )

    correta = senha_mestra_correta(
    chave,
    cofre["verificador_nonce"],
    cofre["verificador_criptograma"],
    cofre["verificador_etiqueta"],
    cofre_id
    )

    if not correta:
        raise HTTPException(
            status_code=401,
            detail="senha-mestra incorreta"
        )

    aad = criar_aad_segredo(
    cofre_id,
    segredo_id
    )

    nonce, criptograma, etiqueta = cifrar(
        chave,
        dados.senha,
        aad
    )

    segredo_atualizado = atualizar_segredo(
    cofre_id,
    segredo_id,
    {
        "nonce": nonce,
        "criptograma": criptograma,
        "etiqueta": etiqueta,
        "titulo": dados.titulo,
        "usuario": dados.usuario,
        "url": dados.url
    }
    )

    return {
    "id": segredo_atualizado["id"],
    "titulo": segredo_atualizado["titulo"],
    "usuario": segredo_atualizado["usuario"],
    "url": segredo_atualizado["url"],
    "senha": dados.senha
    }

@app.delete("/cofres/{cofre_id}/segredos/{segredo_id}")
def excluir_um_segredo(
    cofre_id: str,
    segredo_id: str,
    x_senha_mestra: str = Header(...)
):
    cofre = buscar_cofre(cofre_id)

    if not cofre:
        raise HTTPException(
            status_code=404,
            detail="cofre não encontrado"
        )

    segredo = buscar_segredo(cofre_id, segredo_id)

    if not segredo:
        raise HTTPException(
            status_code=404,
            detail="segredo não encontrado"
        )

    sal = de_b64(cofre["kdf_sal"])

    chave = derivar_chave(
        x_senha_mestra,
        sal,
        cofre["kdf_iteracoes"]
    )

    correta = senha_mestra_correta(
        chave,
        cofre["verificador_nonce"],
        cofre["verificador_criptograma"],
        cofre["verificador_etiqueta"],
        cofre_id
    )

    if not correta:
        raise HTTPException(
            status_code=401,
            detail="senha-mestra incorreta"
        )

    excluir_segredo(cofre_id, segredo_id)

    return {"mensagem": "segredo excluído"}