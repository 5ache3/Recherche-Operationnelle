# Recherche Opérationnelle – README

## Présentation du projet

Ce projet regroupe plusieurs modules et scripts liés à la Recherche Opérationnelle, notamment la résolution graphique et par le simplexe de programmes linéaires, ainsi que des algorithmes pour le problème du voyageur de commerce (TSP). Il contient également des outils pour la génération de documents et de visualisations.

---

## Structure du projet

- **PL/**
  - `M_graphique/`
    - `code.py` : Script Python pour la résolution graphique de programmes linéaires, avec visualisation via Manim.
  - `M_simplex/`
    - `code.py` : Script Python pour la méthode du simplexe, avec visualisation via Manim.
    - `simplex.pdf` : Document PDF expliquant ou illustrant la méthode du simplexe.
    - `simplex.mp4` : Animation vidéo de la méthode du simplexe.
  - `toPDF/`
    - `main.py` : Génère un document Typst à partir d'un programme linéaire, en utilisant les modules graphiques et simplexe.
    - `Plot.py` : Fonctions de visualisation graphique (utilise Manim).
    - `simplex.py` : Génère des tableaux du simplexe au format Typst.
  - `Recherche Operationnelle.pdf` : Document principal du cours ou du projet.

- **TSP/**
  - `code/`
    - `main.py` : Implémentation de plusieurs algorithmes pour le TSP (Christofides, nearest neighbor, 2-opt, 3-opt...).
    - `visualisation/`
      - `2_opt_sqap.py` : Visualisation de l'algorithme 2-opt pour le TSP avec Manim.
      - `PrimMst.py` : Visualisation de l'algorithme de Prim (arbre couvrant minimal) avec Manim.
  - `tsp.pdf` : Document PDF sur le TSP.

---

## Dépendances et installation

### 1. Python

Le projet nécessite **Python 3.8+**.

### 2. Installation des dépendances Python

Vous pouvez installer toutes les dépendances Python nécessaires avec le fichier `requirements.txt` suivant :

```txt
manim
networkx
numpy
```

Pour installer ces dépendances :
```bash
pip install -r requirements.txt
```

### 3. Installation de Typst

Certaines parties du projet (génération de documents .typ) nécessitent [Typst](https://typst.app/), un système de composition de documents moderne.

Pour installer Typst :
- **Via le site officiel :**
  - Rendez-vous sur https://typst.app et suivez les instructions pour télécharger et installer Typst sur votre système.
- **Via le gestionnaire de paquets (Linux) :**
  ```bash
  curl --proto '=https' --tlsv1.2 -sSf https://typst.app/install.sh | sh
  ```
- **Via Scoop (Windows) :**
  ```bash
  scoop install typst
  ```

Après installation, la commande `typst` doit être accessible dans votre terminal.

---

## Utilisation des scripts

### Résolution graphique et simplexe

- Les scripts de `PL/M_graphique/` et `PL/M_simplex/` permettent de visualiser la résolution de programmes linéaires.
- Lancer les scripts avec Manim pour générer des animations :
  ```bash
  manim code.py Graphique
  manim code.py SimplexVideo
  ```

### Génération de documents Typst

- `PL/toPDF/main.py` génère un fichier Typst à partir d'un programme linéaire, en utilisant les modules graphiques et simplexe.
- Les images sont générées dans `PL/toPDF/images/`.

### TSP (Problème du voyageur de commerce)

- `TSP/code/main.py` contient plusieurs algorithmes pour résoudre le TSP.
- Les visualisations (2-opt, Prim) sont dans `TSP/code/visualisation/` et utilisent Manim.

---

## Conseils d'installation

1. **Créer un environnement virtuel (recommandé) :**
   ```bash
   python -m venv venv
   source venv/bin/activate  # ou venv\Scripts\activate sous Windows
   ```

2. **Installer les dépendances :**
   ```bash
   pip install manim networkx numpy
   ```

3. **Pour utiliser Manim, il peut être nécessaire d'installer aussi ffmpeg et LaTeX.**
   - Sous Windows : télécharger ffmpeg et l'ajouter au PATH.
   - Installer une distribution LaTeX (ex : MikTeX ou TeX Live).

---

## Remarques

- Les fichiers PDF et MP4 sont des supports de cours ou des résultats d'exécution.
- Les scripts sont principalement destinés à l'enseignement ou à la démonstration de méthodes de Recherche Opérationnelle.

---

**N'hésitez pas à adapter ce README selon vos besoins spécifiques ou à demander une version plus détaillée pour chaque module !** 