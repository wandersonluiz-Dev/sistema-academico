#!/usr/bin/env bash
# Executa todos os testes automatizados.
set -e
cd "$(dirname "$0")/.."
python3 -m unittest discover -s tests -t . -v
