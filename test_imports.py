"""
Test des imports pour vérifier que tout fonctionne
"""

print("1. Test import langchain_google_vertexai...")
try:
    from langchain_google_vertexai import ChatVertexAI
    print("   ✅ ChatVertexAI importé")
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    exit(1)

print("\n2. Test import config...")
try:
    from simulateur_arnaque.config.llm_config import (
        GOOGLE_PROJECT_ID,
        GOOGLE_LOCATION,
        GOOGLE_MODEL,
        GOOGLE_CREDENTIALS
    )
    print(f"   ✅ Config importée")
    print(f"   Project: {GOOGLE_PROJECT_ID}")
    print(f"   Location: {GOOGLE_LOCATION}")
    print(f"   Model: {GOOGLE_MODEL}")
    print(f"   Credentials: {GOOGLE_CREDENTIALS}")
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    exit(1)

print("\n3. Test import BaseAgent...")
try:
    from simulateur_arnaque.agents.base_agent import BaseAgent
    print("   ✅ BaseAgent importé")
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n4. Test import VictimAgent...")
try:
    from simulateur_arnaque.agents.victim_agent import VictimAgent
    print("   ✅ VictimAgent importé")
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n5. Test création VictimAgent...")
try:
    victim = VictimAgent()
    print(f"   ✅ VictimAgent créé: {victim.name}")
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n✅ TOUS LES TESTS PASSÉS!")
