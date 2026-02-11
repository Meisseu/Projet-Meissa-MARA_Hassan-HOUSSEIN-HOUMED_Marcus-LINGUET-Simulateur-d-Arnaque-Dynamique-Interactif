# Guide d'Utilisation - Système d'Audience (Partie 3)

## 📋 Vue d'ensemble

Le système d'audience permet à des spectateurs de proposer et voter pour des événements perturbateurs qui aident Mme Jeanne Dubois à gagner du temps contre l'arnaqueur.

## 🏗️ Architecture

Le système est composé de 3 modules principaux:

### 1. **ModeratorAgent** (`agents/moderator.py`)
- Reçoit les suggestions de l'audience
- Filtre les propositions inappropriées
- Sélectionne les 3 meilleures options cohérentes avec le contexte

### 2. **AudienceInterface** (`audience_interface.py`)
- Collecte les suggestions (console, web, ou simulé)
- Gère le système de vote
- Enregistre l'historique des événements

### 3. **AudienceEventManager** (`audience_events.py`)
- Coordonne les deux modules précédents
- Gère la fréquence d'activation (tous les X tours)
- Convertit les événements en contraintes pour l'agent victime

---

## 🚀 Utilisation Rapide

### Exemple 1: Mode Console (Interaction Réelle)

```python
from simulateur_arnaque.audience_events import create_audience_manager

# Créer le gestionnaire (nécessite une clé API OpenAI)
manager = create_audience_manager(
    api_key="votre_clé_openai",
    interface_mode="console",
    vote_frequency=5  # Événement tous les 5 tours
)

# Dans la boucle principale du simulateur
turn = 0
while conversation_active:
    turn += 1
    
    # Vérifier si c'est le moment pour un événement audience
    if manager.should_trigger_audience():
        constraint = manager.process_audience_round(
            conversation_context="Résumé de la conversation jusqu'ici...",
            current_objective="Objectif actuel de Jeanne",
            collect_mode="console",  # L'utilisateur tape des suggestions
            vote_mode="console"      # L'utilisateur vote
        )
        
        # La contrainte peut maintenant être injectée dans le prompt de Jeanne
        print(f"Contrainte active: {constraint}")
```

### Exemple 2: Mode Simulé (Pour Tests/Démos)

```python
from simulateur_arnaque.audience_events import create_audience_manager

# Mode simulé: pas besoin d'interaction utilisateur
manager = create_audience_manager(
    api_key="votre_clé_openai",
    interface_mode="simulated",
    vote_frequency=3
)

# Simulation automatique
for turn in range(1, 11):
    if manager.should_trigger_audience():
        constraint = manager.process_audience_round(
            conversation_context=f"Tour {turn}: Discussion en cours...",
            collect_mode="simulated",  # Suggestions pré-définies
            vote_mode="simulated"      # Vote aléatoire automatique
        )
        
        print(f"\n[Tour {turn}] Événement activé!")
        print(constraint)
```

---

## 📖 Utilisation Détaillée

### Créer un Agent Modérateur Seul

```python
from simulateur_arnaque.agents.moderator import ModeratorAgent

moderator = ModeratorAgent(
    api_key="votre_clé_openai",
    model="gpt-4-turbo-preview"
)

# Filtrer et sélectionner des suggestions
suggestions = [
    "Le chien aboie comme un fou",
    "La maison explose",  # Sera rejeté
    "Jeanne doit aller aux toilettes",
    "Alien invasion"  # Sera rejeté
]

selected = moderator.filter_and_select(
    suggestions=suggestions,
    conversation_context="L'arnaqueur demande l'accès TeamViewer",
    current_objective="Gagner du temps sans donner accès"
)

# Afficher les 3 événements sélectionnés
for event in selected:
    print(f"- {event['event']}: {event['description']}")
```

### Créer une Interface Audience Seule

```python
from simulateur_arnaque.audience_interface import AudienceInterface

# Mode console
interface = AudienceInterface(mode="console")

# Collecter des suggestions
suggestions = interface.collect_suggestions(max_suggestions=5)
print(f"Collecté: {suggestions}")

# Afficher des options et voter
events = [
    {'event': 'Le chien aboie', 'description': 'Poupoune veut sortir'},
    {'event': 'La sonnette', 'description': 'Facteur à la porte'},
    {'event': 'Quinte de toux', 'description': 'Jeanne doit boire'}
]

winner = interface.conduct_vote(events, mode="console")
print(f"Gagnant: {winner['event']}")

# Générer la contrainte
constraint = interface.get_event_constraint(winner)
print(constraint)
```

---

## 🎯 Intégration dans la Boucle Principale

Voici comment intégrer le système d'audience dans votre simulateur complet:

```python
from simulateur_arnaque.audience_events import create_audience_manager
# Importez aussi vos autres agents (Victime, Directeur)

# Configuration
api_key = os.getenv("OPENAI_API_KEY")
audience_manager = create_audience_manager(
    api_key=api_key,
    interface_mode="console",  # ou "simulated" pour démo
    vote_frequency=5
)

# Boucle principale
conversation_history = []
current_objective = "Répondre poliment mais lentement"

while True:
    # 1. L'arnaqueur parle
    scammer_input = input("Arnaqueur: ")
    
    # 2. Vérifier si événement audience
    audience_constraint = None
    if audience_manager.should_trigger_audience():
        audience_constraint = audience_manager.process_audience_round(
            conversation_context="\n".join(conversation_history[-5:]),
            current_objective=current_objective,
            collect_mode="console",
            vote_mode="console"
        )
    
    # 3. L'agent Victime répond (en tenant compte de la contrainte)
    victim_prompt = f"""
{base_victim_prompt}

Objectif actuel: {current_objective}

{audience_constraint if audience_constraint else ""}

Conversation:
{conversation_history}

Arnaqueur: {scammer_input}
Jeanne:
"""
    
    victim_response = victim_agent.generate(victim_prompt)
    print(f"Jeanne: {victim_response}")
    
    # 4. Mise à jour historique
    conversation_history.append(f"Arnaqueur: {scammer_input}")
    conversation_history.append(f"Jeanne: {victim_response}")
    
    # 5. Effacer la contrainte après utilisation
    if audience_constraint:
        audience_manager.clear_constraint()
```

---

## 🎨 Personnalisation

### Changer la Fréquence d'Événements

```python
# Événement tous les 3 tours
manager = create_audience_manager(api_key=api_key, vote_frequency=3)

# Événement tous les 10 tours
manager = create_audience_manager(api_key=api_key, vote_frequency=10)
```

### Créer des Événements Personnalisés

```python
from simulateur_arnaque.audience_events import DEFAULT_EVENTS

# Ajouter vos propres événements
custom_events = [
    {
        'event': "Le four fait un bruit bizarre",
        'description': "Jeanne craint que le gâteau brûle"
    },
    {
        'event': "Le petit-fils appelle sur Skype",
        'description': "Un vrai membre de la famille arrive"
    }
]

DEFAULT_EVENTS.extend(custom_events)
```

### Modifier le Prompt du Modérateur

```python
moderator = ModeratorAgent(api_key=api_key)

# Personnaliser le prompt système
moderator.system_prompt += """

RÈGLE SUPPLÉMENTAIRE:
Privilégier les événements qui impliquent la technologie moderne
pour créer de la confusion chez Jeanne.
"""
```

---

## 📊 Statistiques et Historique

```python
# Obtenir des statistiques
stats = audience_manager.get_statistics()
print(f"Tours totaux: {stats['total_turns']}")
print(f"Suggestions collectées: {stats['total_suggestions']}")
print(f"Événements activés: {stats['total_events']}")
print(f"Dernier événement: {stats['last_event']}")

# Sauvegarder l'historique
audience_manager.interface.save_history("logs/session_audience.json")
```

---

## 🧪 Tests

Pour tester le système:

```bash
# Tests unitaires
pytest tests/test_audience_system.py -v

# Test spécifique
pytest tests/test_audience_system.py::TestModeratorAgent::test_parse_response_valid_format -v
```

---

## 🐛 Résolution de Problèmes

### Problème: Le modérateur rejette toutes les suggestions

**Solution**: Les suggestions sont peut-être trop extrêmes. Le modérateur filtre:
- Violence
- Vulgarité
- Événements impossibles
- Fin brutale de la conversation

Essayez des suggestions plus réalistes comme:
- "Le chien aboie"
- "La sonnette retentit"
- "Jeanne cherche ses lunettes"

### Problème: Le LLM ne répond pas au bon format

**Solution**: Le parsing est robuste mais si le problème persiste:
```python
# Activer le mode debug
import logging
logging.basicConfig(level=logging.DEBUG)

# Ou utiliser les événements par défaut
selected = moderator._get_default_events()
```

### Problème: L'interface console ne capture pas les suggestions

**Solution**: Vérifiez que vous êtes bien en mode interactif:
```python
# Tester avec mode simulé d'abord
manager = create_audience_manager(
    api_key=api_key,
    interface_mode="simulated"  # Pas d'interaction nécessaire
)
```

---

## 📝 Checklist de Validation

- [ ] Le ModeratorAgent filtre correctement les suggestions inappropriées
- [ ] L'interface collecte et affiche les suggestions
- [ ] Le système de vote fonctionne (console ou simulé)
- [ ] Les événements sont convertis en contraintes textuelles
- [ ] La fréquence d'activation est respectée (tous les X tours)
- [ ] L'historique est sauvegardé correctement
- [ ] Les tests unitaires passent

---

## 🎓 Exemples de Flux Complets

### Exemple: Session Démo Complète

```python
from simulateur_arnaque.audience_events import create_audience_manager
import os

# Configuration
os.environ['OPENAI_API_KEY'] = 'votre_clé'
manager = create_audience_manager(
    api_key=os.getenv('OPENAI_API_KEY'),
    interface_mode="simulated",
    vote_frequency=2
)

# Simulation de 6 tours
contexts = [
    "L'arnaqueur se présente comme support Microsoft",
    "Il demande l'accès à l'ordinateur",
    "Il veut installer TeamViewer",
    "Il demande les informations bancaires",
    "Il devient insistant",
    "Il menace de couper l'ordinateur"
]

for turn, context in enumerate(contexts, 1):
    print(f"\n{'='*60}")
    print(f"TOUR {turn}")
    print(f"{'='*60}")
    print(f"Contexte: {context}")
    
    if manager.should_trigger_audience():
        constraint = manager.process_audience_round(
            conversation_context=context,
            current_objective="Résister sans raccrocher",
            collect_mode="simulated",
            vote_mode="simulated"
        )
        print(f"\n🎭 ÉVÉNEMENT ACTIVÉ!")
        print(f"Contrainte générée pour Jeanne:\n{constraint}")
    else:
        print("\n[Pas d'événement audience ce tour]")

# Statistiques finales
print(f"\n{'='*60}")
print("STATISTIQUES FINALES")
print(f"{'='*60}")
stats = manager.get_statistics()
for key, value in stats.items():
    print(f"{key}: {value}")
```

---

**Partie 3 complète! 🎉**

Pour toute question, consultez le code source avec les docstrings détaillées.
