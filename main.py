"""
main.py - Script temporaire pour tester l'intégration VictimAgent
"""

from agents.victim_agent import VictimAgent


def test_victim_agent():
    """Test simple: une conversation avec Jeanne"""
    
    print("=" * 60)
    print("🎭 VICTIM AGENT - TEST D'INTÉGRATION")
    print("=" * 60)
    
    # Initialiser l'agent
    print("\n✅ Initialisation de Jeanne Dubois...")
    victim = VictimAgent()
    print(f"Agent: {victim.name}")
    print(f"Température: {victim.temperature}")
    
    # Afficher l'état
    print("\n📊 État courant:")
    state = victim.get_state()
    for key, value in state.items():
        print(f"  - {key}: {value}")
    
    # Test 1: Message simple
    print("\n" + "=" * 60)
    print("TEST 1: Message d'introduction")
    print("=" * 60)
    
    scammer_input_1 = "Hello, is this Jeanne Dubois? I'm calling from Microsoft."
    print(f"\n📞 Arnaqueur: {scammer_input_1}")
    
    try:
        response_1 = victim.respond(
            scammer_input=scammer_input_1,
            objective="Feign belief but ask silly questions"
        )
        print(f"👵 Jeanne: {response_1}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test 2: Deuxième message
    print("\n" + "=" * 60)
    print("TEST 2: Demande de terminal")
    print("=" * 60)
    
    scammer_input_2 = "Can you open your terminal or command prompt?"
    print(f"\n📞 Arnaqueur: {scammer_input_2}")
    
    try:
        response_2 = victim.respond(
            scammer_input=scammer_input_2,
            objective="Pretend to search for terminal but cannot find it"
        )
        print(f"👵 Jeanne: {response_2}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test 3: Avec contrainte audience
    print("\n" + "=" * 60)
    print("TEST 3: Avec contrainte audience")
    print("=" * 60)
    
    scammer_input_3 = "This is urgent! We need to act now!"
    print(f"\n📞 Arnaqueur: {scammer_input_3}")
    
    try:
        response_3 = victim.respond(
            scammer_input=scammer_input_3,
            objective="Resist and create distractions",
            audience_constraint="Your dog Scooty starts barking"
        )
        print(f"👵 Jeanne: {response_3}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Résumé final
    print("\n" + "=" * 60)
    print("✅ TEST TERMINÉ")
    print("=" * 60)
    
    final_state = victim.get_state()
    print(f"\n📊 État final:")
    for key, value in final_state.items():
        print(f"  - {key}: {value}")
    
    print("\n✅ VictimAgent fonctionne correctement!")
    print("=" * 60)


if __name__ == "__main__":
    test_victim_agent()