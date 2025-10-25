import os
import sys

def setup_project():
    """Setup centralizado do projeto"""
    # Encontra a raiz do projeto (2 níveis acima: src -> raiz)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

setup_project()