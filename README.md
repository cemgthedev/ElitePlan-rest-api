# ElitePlan-rest-api
Projeto da disciplina de Desenvolvimento de Software para Persistência. Trata-se de uma REST API utilizando o framework FastAPI e SQLAlchemy do python consistindo em uma aplicação para persistir dados de planos de treino personalizados.

# Migrações
- Inicialize o alembic: alembic init alembic
- No arquivo alembic.ini configure o sqlalchemy.url com as informações do bd. Ex.: postgresql://postgres:12345678@localhost:5432/study
- Gere a migração: alembic revision --autogenerate -m "título da migração"
- Aplique as alterações ao banco de dados: alembic upgrade head

# Executando

- Criar um ambiente virtual com o seguinte comando: python -m venv .venv
- Rodar ambiente no prompt de comando do windows: .venv\Scripts\activate
- Instalar libs: pip install fastapi uvicorn sqlmodel psycopg2 alembic
- Entrar na pasta src: cd src
- Executar o servidor com o seguinte comando: uvicorn main:app --reload
