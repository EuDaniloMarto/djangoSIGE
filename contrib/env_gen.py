#!/usr/bin/env python


"""
Gerador de arquivo .env para projetos Django.
Cria um novo SECRET_KEY seguro e adiciona configurações iniciais.
Requer que a biblioteca Django esteja instalada.
"""
import os
import sys

from django.utils.crypto import get_random_string


def generate_secret_key():
    """Gera uma string aleatória segura para o SECRET_KEY."""
    # Caracteres usados, incluindo letras, números e uma ampla gama de símbolos
    chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()_+-=[]{};:.,<>/?|"
    return get_random_string(50, chars)


def create_env_file():
    """Cria o arquivo .env com a configuração inicial, incluindo um novo SECRET_KEY."""
    env_filepath = ".env"

    # Verifica se o arquivo .env já existe
    if os.path.exists(env_filepath):
        print(f"ERRO: O arquivo '{env_filepath}' já existe.")
        print("Criei o arquivo .env.new para que você possa copiar a chave.")
        env_filepath = ".env.new"

    # 1. Gera a chave secreta
    secret_key = generate_secret_key()

    # 2. Define o template de configuração usando f-string
    config_content = f"""
# Configurações do ambiente para Django
# ------------------------------------------------------------------------------

# GENERAL
# ------------------------------------------------------------------------------
# ATENÇÃO: Mude DEBUG para False em produção!
DEBUG=True
SECRET_KEY={secret_key}
ALLOWED_HOSTS=127.0.0.1, localhost, 0.0.0.0, .seu-dominio.com

# DATABASES
# ------------------------------------------------------------------------------
# Exemplo para SQLite:
DATABASE_URL=sqlite:///db.sqlite3

# Exemplo para PostgreSQL (descomente se usar):
# DATABASE_URL=postgres://user:password@host:port/name

# EMAIL
# ------------------------------------------------------------------------------
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_TIMEOUT=500
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_HOST_PASSWORD=
EMAIL_HOST_USER=
EMAIL_USE_TLS=True
EMAIL_USE_SSL=False

# OUTROS SERVIÇOS
# ------------------------------------------------------------------------------
# Exemplo de configuração de armazenamento na nuvem (AWS S3)
# AWS_ACCESS_KEY_ID=
# AWS_SECRET_ACCESS_KEY=
# AWS_STORAGE_BUCKET_NAME=
"""
    # Remove espaços em branco extras no início e fim
    config_content = config_content.strip()

    # 3. Escreve o conteúdo no arquivo
    try:
        with open(env_filepath, "w", encoding="utf-8") as configfile:
            configfile.write(config_content)
        print(f"Arquivo '{env_filepath}' gerado com sucesso.")
        print("Lembre-se de instalar 'python-decouple' ou 'django-environ' para ler essas variáveis.")
    except IOError as e:
        print(f"Erro ao escrever o arquivo: {e}")
        sys.exit(1)


if __name__ == "__main__":
    create_env_file()
