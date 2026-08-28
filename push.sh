#!/usr/bin/env bash
# Sobe este repositório para o seu fork no GitHub.
# Uso:  ./push.sh            (usa JULIA-ALVESROCHA como dono do fork)
#       ./push.sh OUTRO-USER
set -e
OWNER="${1:-JULIA-ALVESROCHA}"
REPO="jovens-talentos-2026-hackathon-data"

echo "==> 1/3  criando o fork (precisa do gh autenticado: gh auth login)"
gh repo fork "seazone-tech/$REPO" --clone=false --remote=false 2>/dev/null || \
  echo "    fork já existe ou gh indisponível — seguindo"

echo "==> 2/3  apontando o remote"
git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$OWNER/$REPO.git"

echo "==> 3/3  enviando"
git push -u origin main --force

echo
echo "Pronto: https://github.com/$OWNER/$REPO"
echo "Não esqueça de trocar COLE-AQUI-O-LINK-DO-GOOGLE-DRIVE na primeira linha do README.md."
