import ast
import argparse
import re
from pathlib import Path
import numpy as np
from typing import Dict, Any, List, Tuple


class FeatureVisitor(ast.NodeVisitor):
    def __init__(self):
        self.ast_nodes = 0
        self.ast_depth_max = 0
        self.loop_count = 0
        self.if_count = 0
        self.function_calls = 0
        self.nesting_max = 0
        self.vars = set()
        self.funcs = set()
        self._current_depth = 0

    def _enter_node(self, node):
        self.ast_nodes += 1
        self._current_depth += 1
        self.ast_depth_max = max(self.ast_depth_max, self._current_depth)

        # Nesting: on considère seulement certaines structures pour l'imbrication
        if isinstance(node, (ast.If, ast.For, ast.While, ast.With, ast.Try)):
            self.nesting_max = max(self.nesting_max, self._current_depth)

    def _exit_node(self, node):
        self._current_depth -= 1

    def generic_visit(self, node):
        self._enter_node(node)
        super().generic_visit(node)
        self._exit_node(node)

    def visit_If(self, node):
        self._enter_node(node)
        self.if_count += 1
        self.generic_visit(node)  # visite enfants
        self._exit_node(node)

    def visit_For(self, node):
        self._enter_node(node)
        self.loop_count += 1
        self.generic_visit(node)
        self._exit_node(node)

    def visit_While(self, node):
        self._enter_node(node)
        self.loop_count += 1
        self.generic_visit(node)
        self._exit_node(node)

    def visit_Call(self, node):
        self.function_calls += 1
        # Essayer d'extraire le nom de la fonction appelée
        if isinstance(node.func, ast.Name):
            self.funcs.add(node.func.id)
        elif isinstance(node.func, ast.Attribute):
            # ex: obj.method()
            self.funcs.add(node.func.attr)
        self.generic_visit(node)

    def visit_Name(self, node):
        # Variables utilisées (lecture ou écriture)
        self.vars.add(node.id)
        self.generic_visit(node)


def extract_features(code: str) -> Dict[str, Any]:
    """
    Extrait les features d'un code Python et retourne un dictionnaire.
    """
    tree = ast.parse(code)
    visitor = FeatureVisitor()
    visitor.visit(tree)

    features = {
        "ast_nodes": visitor.ast_nodes,
        "ast_depth_max": visitor.ast_depth_max,
        "loop_count": visitor.loop_count,
        "if_count": visitor.if_count,
        "function_calls": visitor.function_calls,
        "nesting_max": visitor.nesting_max,
        "distinct_vars": len(visitor.vars),
        "distinct_funcs": len(visitor.funcs),
    }
    return features


def features_to_vector(features: Dict[str, Any],
                       keys: List[str] | None = None) -> np.ndarray:
    """
    Convertit le dict de features en vecteur numpy dans l'ordre donné par `keys`.
    Si keys est None, utilise un ordre par défaut.
    """
    if keys is None:
        keys = [
            "ast_nodes",
            "ast_depth_max",
            "loop_count",
            "if_count",
            "function_calls",
            "nesting_max",
            "distinct_vars",
            "distinct_funcs",
        ]
    return np.array([features[k] for k in keys], dtype=float)


def ordre_fichier(chemin: Path) -> tuple[int | float, str]:
    """Trie les fichiers numérotés dans l'ordre numérique."""
    correspondance = re.match(r"\D*(\d+)", chemin.name)
    return (int(correspondance.group(1)) if correspondance else float("inf"), chemin.name)


def vecteurs_dossier(dossier: str | Path) -> list[tuple[Path, np.ndarray]]:
    """Extrait un vecteur de features pour chaque fichier Python du dossier."""
    fichiers = sorted(Path(dossier).glob("*.py"), key=ordre_fichier)
    return [
        (fichier, features_to_vector(extract_features(fichier.read_text(encoding="utf-8"))))
        for fichier in fichiers
    ]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calcule les vecteurs AST d'un dossier Python.")
    parser.add_argument("dossier", help="Dossier contenant les fichiers Python")
    arguments = parser.parse_args()

    for fichier, vecteur in vecteurs_dossier(arguments.dossier):
        print(f"{fichier.name}: {vecteur.tolist()}")