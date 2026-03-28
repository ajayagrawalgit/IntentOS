def execute_actions(intent_data):
    actions = intent_data.get("actions", [])
    
    results = []

    if "call ambulance" in str(actions).lower():
        results.append("🚑 Ambulance called (simulated)")

    if "give sugar" in str(actions).lower():
        results.append("🍬 Give sugar immediately")

    if intent_data.get("severity") == "high":
        results.append("⚠️ High priority emergency detected")

    results.append("📍 Location shared (simulated)")

    return results