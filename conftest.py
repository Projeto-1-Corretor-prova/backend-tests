"""Conftest - Configuração global dos testes"""
import pytest
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path para importações
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tests.fixtures.api_fixtures import *  # noqa: F401, F403
