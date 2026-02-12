"""
Test Partie 1 - Hassan
VictimAgent + Audio Tools
"""

from simulateur_arnaque.agents.victim_agent import VictimAgent

print("=" * 60)
print("TEST PARTIE 1 - Hassan")
print("=" * 60)

# Test 1: Initialisation
print("\n✅ Test 1: Initialisation VictimAgent")
victim = VictimAgent()
print(f"   Agent: {victim.name}")
print(f"   Température: {victim.temperature}")

# Test 2: Réponse simple
print("\n✅ Test 2: VictimAgent répond")
response = victim.respond(
    scammer_input="Hello, I'm from Microsoft support",
    objective="Be confused"
)
print(f"   Jeanne: {response[:100]}...")

# Test 3: Avec contrainte audience
print("\n✅ Test 3: VictimAgent avec contrainte audience")
response2 = victim.respond(
    scammer_input="Open your terminal now!",
    objective="Pretend to search but fail",
    audience_constraint="Your dog is barking loudly"
)
print(f"   Jeanne: {response2[:100]}...")

print("\n" + "=" * 60)
print("✅ TESTS PARTIE 1 - TERMINÉS!")
print("=" * 60)