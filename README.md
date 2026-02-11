# Simulateur d'Arnaque Dynamique & Interactif

## 📋 À propos du projet

Ce projet est un simulateur éducatif et divertissant d'arnaque téléphonique utilisant des agents LLM orchestrés. Le système simule une conversation entre un arnaqueur et une "victime" virtuelle (Mme Jeanne Dubois) qui résiste de manière subtile et humoristique aux tentatives d'escroquerie.

### 🎭 Le Concept

Le simulateur met en scène trois agents intelligents :
- **L'Agent Victime (Mme Jeanne Dubois)** : Une dame de 78 ans qui joue le rôle de la victime potentielle
- **L'Agent Directeur** : Superviseur invisible qui orchestre le scénario
- **L'Agent Modérateur Audience** : Gère l'interaction avec l'audience pour créer des événements perturbateurs

---

## 👥 Membres du Groupe

- **Meissa MARA**
- **Hassan HOUSSEIN-HOUMED**
- **Marcus LINGUET**

---

## 🏗️ Architecture du Projet

```
Projet_arnaque/
├── simulateur_arnaque/          # Package principal
│   ├── agents/                  # Agents LLM (Victime, Directeur, Modérateur)
│   ├── tools/                   # Outils audio et fonctions MCP
│   ├── scripts/                 # Scripts d'arnaque prédéfinis
│   ├── audio/                   # Fichiers audio pour effets sonores
│   └── __init__.py
├── tests/                       # Tests unitaires et d'intégration
├── logs/                        # Logs des conversations
├── .env.example                 # Template variables d'environnement
├── .gitignore                   # Fichiers à ignorer
├── requirements.txt             # Dépendances Python
└── README.md                    # Ce fichier
```

---

## 🚀 Installation

### Prérequis
- Python 3.9 ou supérieur
- Compte OpenAI avec clé API (ou autre fournisseur LLM)

### Étapes d'installation

1. **Cloner le repository :**
```bash
git clone https://github.com/Meisseu/Projet-Meissa-MARA_Hassan-HOUSSEIN-HOUMED_Marcus-LINGUET-Simulateur-d-Arnaque-Dynamique-Interactif.git
cd Projet-Meissa-MARA_Hassan-HOUSSEIN-HOUMED_Marcus-LINGUET-Simulateur-d-Arnaque-Dynamique-Interactif/Projet_arnaque
```

2. **Créer un environnement virtuel :**
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. **Installer les dépendances :**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement :**
```bash
cp .env.example .env
# Éditer .env et ajouter votre clé API OpenAI
```

---

## 🎮 Utilisation

### Lancement du simulateur

```bash
python -m simulateur_arnaque.main
```

### Modes disponibles

1. **Mode Arnaqueur Humain :** Vous jouez le rôle de l'arnaqueur
2. **Mode Arnaqueur Bot :** Un LLM joue l'arnaqueur automatiquement
3. **Mode Démo :** Conversation pré-scriptée pour démonstration

---

## 🛠️ Fonctionnalités

### ✅ Implémentées
- [ ] Agent Victime (Mme Jeanne Dubois) avec personnalité cohérente
- [ ] Système de bruitages contextuels (aboiements, toux, sonnette)
- [ ] Agent Directeur pour orchestrer le scénario
- [ ] Scripts d'arnaque prédéfinis (Support Technique, Arnaque Bancaire)
- [ ] Système d'audience interactif avec votes
- [ ] Boucle principale d'exécution

### 🔄 En cours de développement
- Configuration et structure de base ✓
- Implémentation des agents
- Tests d'intégration

### 🎯 À venir
- Interface web avec Streamlit
- Support audio réel (TTS/STT)
- Plus de scénarios d'arnaque
- Statistiques de résistance

---

## 📊 Scénarios Disponibles

### 1. Support Technique Microsoft
Arnaque classique où l'escroc prétend travailler pour Microsoft et signale un problème sur l'ordinateur de la victime.

### 2. Arnaque Bancaire
L'arnaqueur se fait passer pour un conseiller bancaire alertant d'une fraude sur le compte.

---

## 🧪 Tests

Pour exécuter les tests :
```bash
pytest tests/
```

---

## 📝 Documentation Technique

### Technologies utilisées
- **LangChain** : Framework pour orchestrer les agents LLM
- **OpenAI API** : Modèle de langage principal
- **Python-dotenv** : Gestion des variables d'environnement
- **Pytest** : Framework de tests

### Points d'attention
- Les clés API ne doivent **JAMAIS** être commitées
- Le fichier `.env` est dans `.gitignore`
- Utiliser `.env.example` comme template

---

## 🎓 Contexte Académique

Ce projet est réalisé dans le cadre du Master 2 Intelligence Artificielle. Il a pour objectifs :
- Maîtriser l'orchestration de multiples agents LLM
- Comprendre le prompt engineering avancé
- Implémenter des outils (Tools/MCP) pour LLM
- Créer une expérience interactive et ludique

---

## 📸 Screenshots

_Les captures d'écran seront ajoutées au fur et à mesure du développement_

---

## 🤝 Contribution

Ce projet est en développement actif. Les branches de travail sont :
- `master` : Version stable
- `Meisseu` : Développement Partie 1 (Infrastructure & Agent Victime)
- `Hassan` : Développement Partie 2 (Directeur & Scripts)
- `Marcus` : Développement Partie 3 (Audience Interactive)

---

## 📜 Licence

Projet académique - Master 2 IA - 2026

---

## ⚠️ Avertissement

Ce simulateur est à but **strictement éducatif et préventif**. Il vise à sensibiliser aux techniques d'arnaque téléphonique. Aucune utilisation malveillante n'est autorisée ou encouragée.

---

## 📞 Contact

Pour toute question sur le projet, contactez les membres du groupe via GitHub.
