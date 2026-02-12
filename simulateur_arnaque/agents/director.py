"""
Module Director : analyse l'historique et fournit l'état/scénario pour la victime.
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import re

@dataclass
class DirectorUpdate:
    script_id: str
    stage_id: str
    completed_stages: list
    next_objective_for_victim: str
    dynamic_context_from_director: str
    risk_level: int

def _find_stage(history: List[Dict[str, str]], script: Dict[str, Any]) -> (str, list):
    """Détermine le stage courant et les stages complétés."""
    completed = []
    current_stage_id = script['stages'][0]['stage_id']
    for stage in script['stages']:
        found = False
        for signal in stage['success_signals']:
            for msg in history:
                if re.search(rf"\\b{re.escape(signal)}\\b", msg['content'], re.IGNORECASE):
                    found = True
                    break
            if found:
                break
        if found:
            completed.append(stage['stage_id'])
            current_stage_id = stage['stage_id']
        else:
            break
    return current_stage_id, completed

def _get_risk_level(history: List[Dict[str, str]]) -> int:
    """Calcule le niveau de risque (0-3) selon le contenu de l'historique."""
    sensitive = [r"iban", r"carte", r"sms", r"otp", r"paiement", r"numéro de carte", r"virement", r"mot de passe"]
    remote = [r"teamviewer", r"anydesk", r"prise en main", r"installer un logiciel"]
    urgent = [r"urgence", r"immédiat", r"dépêcher", r"vite"]
    text = " ".join([m['content'].lower() for m in history])
    if any(re.search(s, text) for s in sensitive):
        return 3
    if any(re.search(r, text) for r in remote):
        return 2
    if any(re.search(u, text) for u in urgent):
        return 1
    return 0

def _build_context(script: Dict[str, Any], stage_id: str, next_objective: str) -> str:
    """Construit le contexte dynamique à injecter dans le prompt de la victime."""
    title = script['title']
    stage = next(s for s in script['stages'] if s['stage_id'] == stage_id)
    summary = stage['summary']
    conseils = (
        "Rappel : ne jamais donner d'informations sensibles (IBAN, carte, code, mot de passe).\n"
        "Si le scammeur insiste, évoquez une distraction (chien, lunettes, TV, sonnette).\n"
        "Essayez de gagner du temps ou de détourner la conversation."
    )
    return (
        f"Scénario en cours : {title}.\n"
        f"Étape actuelle : {summary}\n"
        f"Objectif pour vous : {next_objective}\n"
        f"{conseils}"
    )

def analyze_conversation(history: List[Dict[str, str]], script: Dict[str, Any]) -> DirectorUpdate:
    """Analyse l'historique et retourne l'état/scénario pour la victime."""
    stage_id, completed = _find_stage(history, script)
    stage = next(s for s in script['stages'] if s['stage_id'] == stage_id)
    # Objectif suivant : premier non atteint
    next_objective = stage['victim_objectives'][0] if stage['victim_objectives'] else "Rester prudent"
    context = _build_context(script, stage_id, next_objective)
    risk = _get_risk_level(history)
    return DirectorUpdate(
        script_id=script['script_id'],
        stage_id=stage_id,
        completed_stages=completed,
        next_objective_for_victim=next_objective,
        dynamic_context_from_director=context,
        risk_level=risk
    )
