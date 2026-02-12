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
│   │   ├── base_agent.py
│   │   ├── victim_agent.py
│   │   ├── victim_prompt.py
│   │   ├── director.py
│   │   └── moderator.py
│   ├── tools/                   # Outils audio et fonctions MCP
│   │   └── audio_tools.py
│   ├── scripts/                 # Scripts d'arnaque prédéfinis
│   │   ├── script_loader.py
│   │   ├── microsoft_support.json
│   │   └── bank_fraud.json
│   ├── config/                  # Configuration centralisée
│   │   └── llm_config.py
│   ├── audio/                   # Fichiers audio pour effets sonores
│   ├── audience_events.py       # Gestion des événements audience
│   ├── audience_interface.py    # Interface d'audience
│   └── __init__.py
├── tests/                       # Tests unitaires et d'intégration
│   ├── test_victim_agent.py
│   ├── test_audio_tools.py
│   ├── test_director.py
│   ├── test_imports.py
│   ├── test_audience_system.py
│   └── test_integration_p1_p3.py
├── logs/                        # Logs des conversations
├── main.py                      # Point d'entrée principal
├── test_hassan_part1.py         # Test Partie 1 (Hassan)
├── .env.example                 # Template variables d'environnement
├── .gitignore                   # Fichiers à ignorer
├── requirements.txt             # Dépendances Python
├── DECOUPAGE_TRAVAIL.md         # Documentation du découpage
├── INSTRUCTIONS_COMMIT.md       # Workflow Git
└── README.md                    # Ce fichier

```

---

## 🚀 Installation

### Prérequis
- Python 3.10 ou supérieur
- Compte OpenAI avec clé API (ou Google Vertex AI)

### Étapes d'installation

1. **Cloner le repository :**
```bash
git clone https://github.com/Meisseu/Projet-Meissa-MARA_Hassan-HOUSSEIN-HOUMED_Marcus-LINGUET-Simulateur-d-Arnaque-Dynamique-Interactif.git
cd Projet-Meissa-MARA_Hassan-HOUSSEIN-HOUMED_Marcus-LINGUET-Simulateur-d-Arnaque-Dynamique-Interactif
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
# Éditer .env et ajouter votre clé API (OpenAI ou Google Vertex AI)
```

---

## 🎮 Utilisation

### Lancement du simulateur

```bash
python main.py
```

Le simulateur vous proposera :
1. **Choix du scénario** :
   - Faux support technique Microsoft
   - Arnaque bancaire - Faux conseiller

2. **Activation du système d'audience** (optionnel) :
   - Mode "Oui" : Active les événements perturbateurs du public
   - Mode "Non" : Conversation directe sans interruptions

### Commandes pendant la simulation

- Tapez votre message pour interagir avec Jeanne
- `status` : Voir l'état actuel de la simulation
- `reset` : Recommencer la simulation
- `quit` ou `exit` : Quitter

### Modes disponibles

1. **Mode Arnaqueur Humain :** Vous jouez le rôle de l'arnaqueur ✓
2. **Mode Audience Interactif :** Le public peut créer des événements perturbateurs ✓
3. **Mode Simulation Complète :** Intégration Director + Victim + Audience ✓

---

## 🛠️ Fonctionnalités

### ✅ Partie 1 - Infrastructure & Agent Victime (Hassan)

**Status:** ✅ COMPLÈTE

#### Composants Implémentés
- [x] **VictimAgent** : Agent Jeanne Dubois avec mémoire conversationnelle
- [x] **BaseAgent** : Classe abstraite pour l'héritage LangChain
- [x] **Victim Prompt** : Persona Jeanne Dubois (78 ans, résistante, réponses françaises)
- [x] **Audio Tools** : 6 outils (@tool decorators) - dog_bark, cough, doorbell, tv_background, phone_ring, cat_meow
- [x] **LLM Config** : Configuration centralisée (variables d'env, températures)
- [x] **Unit Tests** : Tests VictimAgent et Audio Tools
- [x] **Documentation** : Docstrings et .gitignore sécurisé (exclusion *.json)

---

### ✅ Partie 2 - Agent Directeur & Scripts (Marcus)

**Status:** ✅ COMPLÈTE

#### Composants Implémentés
- [x] **Agent Directeur** : Analyste invisible du scénario
- [x] **Script Loader** : Chargeur de scripts JSON
- [x] **Scripts d'arnaque** :
  - Support Technique Microsoft (5 étapes)
  - Arnaque Bancaire (3 étapes)
- [x] **Détection d'étapes** : Reconnaissance keywords
- [x] **Adaptation stratégie** : Objectifs dynamiques pour Jeanne

---

### ✅ Partie 3 - Système d'Audience Interactif (Meissa)

**Status:** ✅ COMPLÈTE

#### Composants Implémentés
- [x] **Agent Modérateur** : Filtre et sélectionne propositions
- [x] **Interface Audience** : Console pour suggestions
- [x] **Système de Vote** : Vote simulé ou réel
- [x] **Event Manager** : Gestion événements perturbateurs
- [x] **Integration** : Contraintes injectables dans VictimAgent

---

### ✅ Partie 4 - Orchestration Complète (Collaboration)

**Status:** ✅ COMPLÈTE

#### Composants Implémentés
- [x] **Main Loop** (`main.py`) : Boucle principale orchestrée
- [x] **Integration** : Liaison des 3 agents
- [x] **Menu Scénario** : Choix du type d'arnaque
- [x] **Audience Activation** : Toggle du système d'audience
- [x] **Rich Output** : Affichage formaté avec colors
- [x] **Error Handling** : Gestion des erreurs robuste
- [x] **Logging** : Enregistrement des conversations

---

## 🧪 Tests

### Lancer tous les tests

```bash
pytest tests/
```

### Tester une partie spécifique

```bash
# Partie 1 (Hassan)
pytest tests/test_victim_agent.py
pytest tests/test_audio_tools.py

# Partie 2 (Marcus)
pytest tests/test_director.py

# Partie 3 (Meissa)
pytest tests/test_audience_system.py

# Integration
pytest tests/test_integration_p1_p3.py
```

---

## 📝 Documentation Technique

### Technologies utilisées
- **LangChain** (v0.1.6) : Framework pour orchestrer les agents LLM
- **OpenAI API** (v1.12.0) : Modèle GPT-4 principal
- **Google Vertex AI** : Support LLM alternatif
- **Python-dotenv** (v1.0.0) : Gestion des variables d'environnement
- **Rich** (v13.7.0) : Affichage console formaté
- **Pytest** (v7.4.4) : Framework de tests

### Points d'attention

**SÉCURITÉ - ZÉ RO TOLÉRANCE :**
- Les clés API ne doivent **JAMAIS** être commitées
- Le fichier `.env` est dans `.gitignore`
- Les fichiers `*.json` (credentials) sont exclus
- Utiliser `.env.example` comme template
- Vérifier l'historique Git avant push

**CODE QUALITY :**
- Docstrings complets pour chaque classe/fonction
- Type hints pour clarté
- Gestion d'erreurs robuste
- Imports relatifs (`.` au lieu de noms absolus)
- Logging des erreurs

**PERFORMANCE :**
- Mémoire conversationnelle limitable
- Requêtes API optimisées
- Cache local pour scripts

---

## 🎓 Contexte Académique

Ce projet est réalisé dans le cadre du Master 2 Intelligence Artificielle. Il a pour objectifs :
- ✅ Maîtriser l'orchestration de multiples agents LLM
- ✅ Comprendre le prompt engineering avancé
- ✅ Implémenter des outils (Tools/MCP) pour LLM
- ✅ Créer une expérience interactive et ludique
- ✅ Gérer un projet collaboratif multi-personnes
- ✅ Utiliser Git efficacement avec branches et commits

---

## 📸 Screenshots

_Les captures d'écran seront ajoutées après tests complets_

---

## 🤝 Contribution

Ce projet est en développement complété. Le workflow Git utilisé :

### Branches

- **`main`** : Version stable intégrée (production)
- **`Hassan`** : Développement Partie 1 ✅ MERGÉE
- **`Marcus`** : Développement Partie 2 ✅ MERGÉE
- **`Meissa`** : Développement Partie 3 ✅ MERGÉE

### Workflow

1. Chaque membre travaille sur sa branche dédiée
2. Commits réguliers avec messages descriptifs et clairs
3. Pull Request vers `main` une fois la partie terminée
4. Review croisée obligatoire avant merge
5. Partie 4 développée collaborativement sur `main`

### Commits Best Practices

```
Format: <type>: <description courte>

Types:
- feat: Nouvelle fonctionnalité
- fix: Correction de bug
- test: Ajout de tests
- docs: Documentation
- chore: Tâche administrative
- merge: Fusion de branches
```

Exemple :
```
feat: Implement VictimAgent with memory management

- Classe VictimAgent héritage BaseAgent
- Mémoire conversationnelle ConversationBufferMemory
- Méthode respond() avec objectifs modulables
- Integration LangChain complète
```

---

## 📜 Licence

Projet académique - Master 2 IA - IPSII - 2026

---

## ⚠️ Avertissement

Ce simulateur est à but **strictement éducatif et préventif**. Il vise à sensibiliser aux techniques d'arnaque téléphonique. Aucune utilisation malveillante n'est autorisée ou encouragée.

---

## 📞 Contact & Questions

Pour toute question sur le projet :

- **Hassan HOUSSEIN-HOUMED** : Partie 1 (VictimAgent + Audio Tools)
- **Marcus LINGUET** : Partie 2 (DirectorAgent + Scripts)
- **Meissa MARA** : Partie 3 (AudienceSystem) + Coordination

Contactez via GitHub ou réunion d'équipe.

---