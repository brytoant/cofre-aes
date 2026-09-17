import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def criar_cofre(dados: dict):
    resposta = supabase.table("cofres").insert(dados).execute()
    return resposta.data[0]


def buscar_cofre(cofre_id: str):
    resposta = (
        supabase
        .table("cofres")
        .select("*")
        .eq("id", cofre_id)
        .limit(1)
        .execute()
    )

    if not resposta.data:
        return None

    return resposta.data[0]


def criar_segredo(dados: dict):
    resposta = supabase.table("segredos").insert(dados).execute()
    return resposta.data[0]


def listar_segredos(cofre_id: str):
    resposta = (
        supabase
        .table("segredos")
        .select("id, titulo, usuario, url, criado_em")
        .eq("cofre_id", cofre_id)
        .execute()
    )

    return resposta.data


def buscar_segredo(cofre_id: str, segredo_id: str):
    resposta = (
        supabase
        .table("segredos")
        .select("*")
        .eq("id", segredo_id)
        .eq("cofre_id", cofre_id)
        .limit(1)
        .execute()
    )

    if not resposta.data:
        return None

    return resposta.data[0]


def atualizar_segredo(cofre_id: str, segredo_id: str, dados: dict):
    resposta = (
        supabase
        .table("segredos")
        .update(dados)
        .eq("id", segredo_id)
        .eq("cofre_id", cofre_id)
        .execute()
    )

    if not resposta.data:
        return None

    return resposta.data[0]


def excluir_segredo(cofre_id: str, segredo_id: str):
    resposta = (
        supabase
        .table("segredos")
        .delete()
        .eq("id", segredo_id)
        .eq("cofre_id", cofre_id)
        .execute()
    )

    return bool(resposta.data)