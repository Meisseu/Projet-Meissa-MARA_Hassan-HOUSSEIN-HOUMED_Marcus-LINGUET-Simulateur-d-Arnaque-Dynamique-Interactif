# 📋 Instructions de Commit - Structure Initiale

## Structure créée ✅

```
Projet_arnaque/
├── simulateur_arnaque/
│   ├── __init__.py
│   ├── agents/
│   │   └── __init__.py
│   ├── tools/
│   │   └── __init__.py
│   ├── scripts/
│   │   └── __init__.py
│   └── audio/
├── tests/
│   └── __init__.py
├── logs/
├── README.md
├── .gitignore
├── .env.example
├── requirements.txt
├── DECOUPAGE_TRAVAIL.md
└── INSTRUCTIONS_COMMIT.md (ce fichier)
```

---

## 🔴 AVANT DE COMMIT - CHECKLIST CRITIQUE

- [ ] **Vérifier qu'aucun fichier `.env` n'est présent** (seulement `.env.example`)
- [ ] **Vérifier le `.gitignore`** (doit contenir `.env`)
- [ ] **README.md contient les noms des 3 membres** ✅
- [ ] **Aucune clé API dans les fichiers** ✅

---

## 📤 Commandes Git pour Commit sur Master

### Étape 1: Initialiser le repository local (si pas déjà fait)

```bash
cd "c:\Users\meissa.mara\OneDrive - SPIE BATIGNOLLES\Bureau\IPSII\IntelligenceArtificielle_ML\Projet_arnaque"

# Si premier commit
git init
git remote add origin https://github.com/Meisseu/Projet-Meissa-MARA_Hassan-HOUSSEIN-HOUMED_Marcus-LINGUET-Simulateur-d-Arnaque-Dynamique-Interactif.git

# Si repository déjà cloné
git pull origin master
```

### Étape 2: Ajouter les fichiers de structure

```bash
# Ajouter tous les fichiers de structure
git add README.md
git add .gitignore
git add .env.example
git add requirements.txt
git add DECOUPAGE_TRAVAIL.md
git add INSTRUCTIONS_COMMIT.md

# Ajouter la structure de dossiers
git add simulateur_arnaque/__init__.py
git add simulateur_arnaque/agents/__init__.py
git add simulateur_arnaque/tools/__init__.py
git add simulateur_arnaque/scripts/__init__.py
git add tests/__init__.py

# Créer un fichier .gitkeep pour les dossiers vides
# (Git ne tracke pas les dossiers vides)
```

### Étape 3: Vérifier ce qui sera commité

```bash
git status
```

**Vérifier que:**
- ✅ Tous les fichiers de structure sont en "Changes to be committed"
- ❌ Aucun fichier `.env` n'apparaît
- ❌ Aucun fichier avec des clés API

### Étape 4: Commit sur Master

```bash
git commit -m "feat: Structure initiale du projet - Infrastructure de base

- Ajout README.md avec noms des membres
- Configuration .gitignore et .env.example
- Structure de dossiers (agents/, tools/, scripts/, audio/, tests/)
- requirements.txt avec dépendances principales
- Documentation du découpage de travail"
```

### Étape 5: Push sur Master

```bash
git push origin master
```

---

## 🌿 Créer et Basculer sur la Branche Meisseu

Une fois le commit sur master effectué, créer la branche de développement:

```bash
# Créer et basculer sur la nouvelle branche
git checkout -b Meisseu

# Pousser la branche sur GitHub
git push -u origin Meisseu
```

---

## 📝 Suite du Développement sur la Branche Meisseu

### Partie 1 - À développer sur la branche:

1. **Agent Victime (victim.py)**
   - System Prompt avec personnalité Mme Dubois
   - Intégration LangChain Agent
   - Gestion de la mémoire conversationnelle

2. **Outils Audio (audio_tools.py)**
   - Implémentation des @tool decorators
   - play_dog_bark(), play_cough(), play_doorbell(), play_tv_background()
   - Gestion des fichiers audio ou marqueurs textuels

3. **Configuration (config.py)**
   - Chargement des variables d'environnement
   - Configuration du LLM
   - Paramètres de l'application

4. **Tests (test_victim.py, test_audio_tools.py)**
   - Tests unitaires des outils
   - Tests de l'agent victime
   - Validation du System Prompt

### Commandes Git pour les commits suivants:

```bash
# Sur la branche Meisseu
git add <fichiers modifiés>
git commit -m "feat: Description de la fonctionnalité"
git push origin Meisseu
```

### Quand la Partie 1 est terminée:

1. **Créer une Pull Request** sur GitHub (Meisseu → master)
2. **Review** par les autres membres
3. **Merge** après validation
4. **Mettre à jour master local:**
   ```bash
   git checkout master
   git pull origin master
   ```

---

## 🎯 Objectifs de la Partie 1

- [ ] Agent Victime fonctionnel avec personnalité cohérente
- [ ] 4 outils audio implémentés et testés
- [ ] System Prompt modulaire (avec contexte dynamique)
- [ ] Mémoire conversationnelle configurée
- [ ] Tests unitaires passants
- [ ] Documentation du code (docstrings)

---

## 🆘 En cas de problème

### Erreur: Clé API commitée par erreur

```bash
# NE JAMAIS FAIRE UN SIMPLE COMMIT POUR CORRIGER
# Il faut nettoyer l'historique Git

# Solution 1: Si pas encore pushé
git reset --soft HEAD~1
# Supprimer la clé du fichier
git add .
git commit -m "fix: Correction sans clé API"

# Solution 2: Si déjà pushé (DANGEREUX)
# Contacter immédiatement le professeur
# Révoquer la clé API immédiatement
```

### Conflit lors du merge

```bash
# Récupérer les dernières modifications
git fetch origin
git merge origin/master

# Résoudre les conflits manuellement
# Puis:
git add <fichiers résolus>
git commit -m "merge: Résolution conflits"
```

---

## ✅ Validation Finale

Avant de merger sur master, vérifier:

1. ✅ Tous les tests passent (`pytest tests/`)
2. ✅ Le code est documenté (docstrings)
3. ✅ Aucune clé API dans l'historique Git
4. ✅ Le `.gitignore` fonctionne correctement
5. ✅ Le README est à jour avec les fonctionnalités implémentées

---

**Bon développement! 🚀**
