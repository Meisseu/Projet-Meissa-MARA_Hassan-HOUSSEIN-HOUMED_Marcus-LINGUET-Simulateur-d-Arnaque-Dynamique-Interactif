"""
Simulateur d'Arnaque Interactif - Main Script
Partie 4 : Orchestration complète

Ce script intègre :
- Partie 1 (Hassan) : VictimAgent avec audio tools
- Partie 2 (Marcus) : DirectorAgent et scripts d'arnaque
- Partie 3 (Meissa) : Système d'audience (ModeratorAgent + AudienceInterface)

Architecture :
Scammeur (User) → DirectorAgent → [AudienceEventManager] → VictimAgent → Réponse
"""

import sys
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich import print as rprint
from colorama import init as colorama_init, Fore, Style

# Imports du projet
from simulateur_arnaque.agents.victim_agent import VictimAgent
from simulateur_arnaque.agents.moderator import ModeratorAgent
from simulateur_arnaque.agents import director
from simulateur_arnaque.scripts import script_loader
from simulateur_arnaque.audience_events import AudienceEventManager
from simulateur_arnaque.audience_interface import AudienceInterface
from simulateur_arnaque.config.llm_config import (
    GOOGLE_PROJECT_ID,
    GOOGLE_CREDENTIALS,
    AUDIENCE_VOTE_FREQUENCY
)

# Initialisation
colorama_init()
console = Console()


class ScamSimulator:
    """Orchestrateur principal du simulateur d'arnaque"""
    
    def __init__(self, script_id: str, use_audience: bool = True):
        """
        Initialiser le simulateur
        
        Args:
            script_id: ID du script d'arnaque à charger (ex: "microsoft_support")
            use_audience: Activer ou non le système d'audience
        """
        # Charger le script d'arnaque
        console.print(f"[cyan]📜 Chargement du script : {script_id}...[/cyan]")
        self.script = script_loader.load_script(script_id)
        
        # Initialiser les agents
        console.print("[cyan]🤖 Initialisation des agents...[/cyan]")
        self.victim = VictimAgent()
        
        # Initialiser le système d'audience
        self.use_audience = use_audience
        if self.use_audience:
            console.print("[cyan]👥 Activation du système d'audience...[/cyan]")
            # Créer les composants de l'audience
            moderator = ModeratorAgent()  # Utilise les credentials Google Cloud par défaut
            interface = AudienceInterface(mode="console")  # Options: "console", "simulated", "web"
            self.audience_manager = AudienceEventManager(
                moderator=moderator,
                interface=interface,
                vote_frequency=AUDIENCE_VOTE_FREQUENCY
            )
        else:
            self.audience_manager = None
        
        # État de la simulation
        self.conversation_history = []
        self.turn_count = 0
        self.current_update = None
        
        console.print("[green]✅ Simulateur initialisé avec succès ![/green]\n")
    
    def display_script_info(self):
        """Afficher les informations du script chargé"""
        console.print(Panel.fit(
            f"[bold cyan]{self.script['title']}[/bold cyan]\n\n"
            f"{self.script.get('description', 'Scénario d\'arnaque interactif')}\n\n"
            f"[yellow]Nombre d'étapes :[/yellow] {len(self.script['stages'])}",
            title="📋 Scénario",
            border_style="cyan"
        ))
    
    def display_director_update(self, update):
        """Afficher l'analyse du DirectorAgent"""
        risk_colors = ["green", "yellow", "orange", "red"]
        risk_labels = ["Faible", "Modéré", "Élevé", "CRITIQUE"]
        
        risk_color = risk_colors[min(update.risk_level, 3)]
        risk_label = risk_labels[min(update.risk_level, 3)]
        
        console.print(Panel.fit(
            f"[yellow]Étape courante :[/yellow] {update.stage_id}\n"
            f"[yellow]Étapes complétées :[/yellow] {', '.join(update.completed_stages) if update.completed_stages else 'Aucune'}\n"
            f"[yellow]Objectif pour Jeanne :[/yellow] {update.next_objective_for_victim}\n"
            f"[yellow]Niveau de risque :[/yellow] [{risk_color}]{risk_label}[/{risk_color}]",
            title="🎬 Analyse du Director",
            border_style="blue"
        ))
    
    def run_turn(self, scammer_input: str) -> str:
        """
        Exécuter un tour de conversation
        
        Args:
            scammer_input: Ce que dit le scammeur (utilisateur)
        
        Returns:
            str: Réponse de la victime
        """
        # Incrémenter le compteur de tours
        self.turn_count += 1
        
        # Ajouter à l'historique
        self.conversation_history.append({
            "role": "scammer",
            "content": scammer_input
        })
        
        # 1. Analyser avec le DirectorAgent
        self.current_update = director.analyze_conversation(
            self.conversation_history,
            self.script
        )
        
        # Afficher l'analyse du director
        if self.turn_count > 1:  # Ne pas afficher au premier tour
            self.display_director_update(self.current_update)
        
        # 2. Gérer les événements d'audience
        audience_constraint = ""
        if self.use_audience and self.audience_manager:
            # Vérifier si c'est le moment de déclencher l'audience
            if self.audience_manager.should_trigger_audience():
                # Construire le contexte de conversation pour le modérateur
                convo_context = f"Script: {self.script['title']}\n"
                convo_context += f"Étape: {self.current_update.stage_id}\n"
                convo_context += f"Dernière phrase scammeur: {scammer_input}"
                
                # Lancer l'événement d'audience
                audience_result = self.audience_manager.process_audience_round(
                    conversation_context=convo_context,
                    current_objective=self.current_update.next_objective_for_victim,
                    collect_mode="simulated",  # "console" pour vraie interaction, "simulated" pour démo
                    vote_mode="simulated"
                )
                
                if audience_result:
                    audience_constraint = audience_result
                    console.print(Panel.fit(
                        f"[magenta]{audience_constraint}[/magenta]",
                        title="👥 Événement Public",
                        border_style="magenta"
                    ))
        
        # 3. Générer la réponse de la victime
        victim_response = self.victim.respond(
            scammer_input=scammer_input,
            objective=self.current_update.next_objective_for_victim,
            audience_constraint=audience_constraint
        )
        
        # Ajouter la réponse à l'historique
        self.conversation_history.append({
            "role": "victim",
            "content": victim_response
        })
        
        return victim_response
    
    def run(self):
        """Boucle principale du simulateur"""
        # Afficher les informations du script
        self.display_script_info()
        
        # Instructions
        console.print(Panel.fit(
            "[bold]Vous jouez le rôle du SCAMMEUR[/bold]\n\n"
            "Essayez de manipuler Mme Jeanne Dubois pour obtenir des informations sensibles.\n"
            "Jeanne va essayer de résister grâce aux conseils du Director et du public.\n\n"
            "[yellow]Commandes :[/yellow]\n"
            "  - Tapez votre message pour parler à Jeanne\n"
            "  - Tapez 'quit' ou 'exit' pour quitter\n"
            "  - Tapez 'status' pour voir l'état de la simulation\n"
            "  - Tapez 'reset' pour recommencer",
            title="📖 Instructions",
            border_style="green"
        ))
        
        console.print("\n[bold cyan]═══════════════════════════════════════════════[/bold cyan]")
        console.print("[bold cyan]   🚀 DÉBUT DE LA SIMULATION[/bold cyan]")
        console.print("[bold cyan]═══════════════════════════════════════════════[/bold cyan]\n")
        
        # Boucle principale
        while True:
            try:
                # Input du scammeur
                console.print(f"\n[bold red]🎭 Scammeur (Tour {self.turn_count + 1}):[/bold red]", end=" ")
                user_input = input().strip()
                
                # Commandes spéciales
                if user_input.lower() in ['quit', 'exit', 'q']:
                    console.print("\n[yellow]👋 Fin de la simulation. À bientôt ![/yellow]")
                    break
                
                if user_input.lower() == 'status':
                    if self.current_update:
                        self.display_director_update(self.current_update)
                    console.print(f"\n[cyan]Tours joués :[/cyan] {self.turn_count}")
                    console.print(f"[cyan]Messages :[/cyan] {len(self.conversation_history)}")
                    continue
                
                if user_input.lower() == 'reset':
                    console.print("\n[yellow]🔄 Réinitialisation...[/yellow]")
                    self.victim.reset_memory()
                    self.conversation_history = []
                    self.turn_count = 0
                    self.current_update = None
                    console.print("[green]✅ Simulation réinitialisée ![/green]")
                    continue
                
                if not user_input:
                    console.print("[dim]Message vide, veuillez réessayer.[/dim]")
                    continue
                
                # Exécuter le tour
                victim_response = self.run_turn(user_input)
                
                # Afficher la réponse
                console.print(f"\n[bold green]👵 Jeanne Dubois:[/bold green]")
                console.print(Panel.fit(
                    victim_response,
                    border_style="green"
                ))
                
            except KeyboardInterrupt:
                console.print("\n\n[yellow]⚠️  Interruption détectée. Tapez 'quit' pour quitter proprement.[/yellow]")
                continue
            
            except Exception as e:
                console.print(f"\n[red]❌ Erreur : {e}[/red]")
                console.print("[yellow]La simulation continue...[/yellow]")
                continue


def main():
    """Point d'entrée principal"""
    console.print("""
[bold cyan]
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║     🎭 SIMULATEUR D'ARNAQUE INTERACTIF 🎭                    ║
║                                                               ║
║     Projet collaboratif :                                    ║
║     - Hassan HOUSSEIN HOUMED (Partie 1)                     ║
║     - Marcus LINGUET (Partie 2)                              ║
║     - Meissa MARA (Partie 3)                                 ║
║                                                               ║
║     IPSII - Intelligence Artificielle & ML                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
[/bold cyan]
""")
    
    # Vérifier la configuration Google Cloud
    import os
    if not os.path.exists(GOOGLE_CREDENTIALS):
        console.print("[red]❌ Erreur : Fichier de credentials Google Cloud introuvable ![/red]")
        console.print(f"[yellow]Fichier attendu : {GOOGLE_CREDENTIALS}[/yellow]")
        console.print("[yellow]Assurez-vous que google-credentials.json est présent.[/yellow]")
        sys.exit(1)
    
    console.print(f"[green]✅ Credentials Google Cloud détectés (Projet: {GOOGLE_PROJECT_ID})[/green]")
    
    # Menu de sélection du scénario
    console.print("\n[bold]📜 Choisissez un scénario :[/bold]")
    console.print("  [cyan]1.[/cyan] Faux support technique Microsoft")
    console.print("  [cyan]2.[/cyan] Arnaque bancaire - Faux conseiller")
    
    choice = input("\n[bold]Votre choix (1-2) :[/bold] ").strip()
    
    script_map = {
        "1": "microsoft_support",
        "2": "bank_fraud"
    }
    
    script_id = script_map.get(choice, "microsoft_support")
    
    # Demander si on active l'audience
    audience_input = input("\n[bold]Activer le système d'audience ? (o/N) :[/bold] ").strip().lower()
    use_audience = audience_input in ['o', 'oui', 'y', 'yes']
    
    # Lancer le simulateur
    console.print("\n")
    simulator = ScamSimulator(script_id=script_id, use_audience=use_audience)
    simulator.run()


if __name__ == "__main__":
    main()
