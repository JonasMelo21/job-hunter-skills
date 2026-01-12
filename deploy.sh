#!/bin/bash

# Verificar se uma mensagem de commit foi passada como argumento
if [ -z "$1" ]; then
    echo "Por favor, digite a mensagem do commit:"
    read COMMIT_MESSAGE
else
    COMMIT_MESSAGE="$1"
fi

# Adicionar todas as mudanças
echo "📦 Adicionando arquivos..."
git add .

# Fazer o commit
echo "💾 Realizando commit..."
git commit -m "$COMMIT_MESSAGE"

# Push para o Hugging Face (origin)
echo "🤗 Enviando para o Hugging Face..."
git push origin main

# Push para o GitHub (github)
echo "🐙 Enviando para o GitHub..."
git push github main

echo "✅ Deploy concluído com sucesso!"
