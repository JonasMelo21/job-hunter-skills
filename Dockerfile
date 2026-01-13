# Usa Python 3.11-slim (base mais leve)
FROM python:3.11-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# 1. Instala Chrome e dependências do sistema
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    chromium \
    chromium-driver \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 2. Configura variáveis de ambiente do Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_PATH=/usr/bin/chromedriver

# Set workdir
WORKDIR /app

# 3. Copia arquivos de configuração do UV
COPY pyproject.toml .
COPY requirements.txt .

# 4. Instala dependências com UV
# O system flag instala no python do sistema (não cria venv)
RUN uv pip install --system -r requirements.txt || uv sync --frozen --no-cache

# 5. Copia o resto do código
COPY . .

# 6. Cria usuário não-root (Segurança do Hugging Face)
RUN useradd -m -u 1000 user
USER user

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
ENV PATH="/home/user/.local/bin:$PATH"

# 4. Configura pasta de trabalho
WORKDIR /app

# 5. Instala bibliotecas Python
COPY --chown=user requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 6. Copia TODO o código (Site + Scraper + CSV)
COPY --chown=user . .

# 7. COMANDO FINAL: Roda APENAS o Site (app.py)
# O scraper (apply.py) fica lá guardado, mas não roda automático
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]