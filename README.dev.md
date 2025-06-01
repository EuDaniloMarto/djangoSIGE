# 📘 DjangoSIGE - Guia para Desenvolvedores

Este guia tem como objetivo facilitar o entendimento, manutenção e evolução do projeto **DjangoSIGE** por desenvolvedores.

## 🔧 Requisitos

- Python 3.8.16 (compatível)
- [Pipenv](https://pipenv.pypa.io/)
- SQLite
- Linux/macOS recomendado (testado no Fedora 42)

> O objetivo futuro é compatibilidade com **Python 3.12+** e **Django 5.2+**

---

## 🚀 Primeiros Passos

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/djangoSIGE.git && cd djangoSIGE
```

### 2. Configure o ambiente Python com Pipenv

```bash
pipenv install --dev
```

> Se preferir, instale via e `requirements-dev.txt`:

```bash
pip install -r requirements-dev.txt
```

### 3. Configure o ambiente

Crie um arquivo `.env` com base no `.env.example`:

```bash
cp .env.example .env
```

Ajuste as variáveis conforme seu ambiente local (ex: `DATABASE_URL`, `DEBUG`, etc.).

---

## 🧪 Executando Testes

```bash
coverage run --source='djangosige' manage.py test && coverage report
```

---

## 🧹 Padrões de Código

### Formatadores e linters configurados:

* [`black`](https://black.readthedocs.io/)
* [`isort`](https://pycqa.github.io/isort/)
* [`flake8`](https://flake8.pycqa.org/)
* [`djlint`](https://www.djlint.com/) (para templates)
* `.editorconfig` para padronização em IDEs

### Comandos úteis

```bash
# Formatar código Python
black .
isort .

# Verificar problemas de estilo
flake8 .

# Verificar templates
djlint djangosige/ --lint
```

---

## 🔄 Migração entre versões do Django

O projeto está atualmente em **Django 3.1.14**. O plano de atualização é:

1. [ ] Django 3.2 (LTS)
2. [ ] Django 4.2 (LTS)
3. [ ] Django 5.2+

As migrações serão feitas de forma incremental, com testes entre etapas.

---

## 🤝 Contribuindo

1. Crie sua branch a partir de `dev`
2. Use commits descritivos
3. Rode os testes e linters antes de abrir PR

---

## 🧠 Dúvidas?

Este projeto ainda não possui documentação técnica formal. Para orientação:

* Explore os apps no diretório `djangosige/`
* Pergunte no repositório original
* Fale comigo (programador responsável)

---
