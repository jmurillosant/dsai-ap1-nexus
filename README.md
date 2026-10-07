# Nexus — rede social no estilo Twitter

Repositório da Atividade Prática 1 de Desenvolvimento de Software Apoiado por IA (UFPA, 2026.4).

## URL pública

> _A preencher no deploy._

## Dupla

- Jorge Murillo
- Silas Lucas

## Stack

- **Backend:** Django 5 + Django REST Framework
- **Frontend:** Templates Django + Bootstrap (server-side)
- **Banco:** SQLite em dev, PostgreSQL em produção
- **Testes:** pytest + pytest-django
- **Deploy:** Render (a confirmar)

## Ferramentas e modelos de IA usados

- **Cline** (extensão do VS Code) com **Qwen 3 27B** via Groq — implementação de código
- **Chat no navegador** (a registrar) — rascunho de specs
- Modelo e ferramenta são anotados em cada commit pelo trailer `Agent:`

## Como rodar localmente

```bash
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python src/manage.py migrate
python src/manage.py runserver