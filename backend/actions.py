from typing import List, Dict, Any

def execute_actions(intent_data: Dict[str, Any]) -> List[str]:
    """Simulates executable actions based on the intent data."""
    actions_raw = intent_data.get("actions", [])
    severity = intent_data.get("severity", "low")
    
    # Ensure it's a list for iteration
    if not isinstance(actions_raw, list):
        actions_raw = [actions_raw]
    
    executed = []
    
    # 1. Condition based simulated actions
    actions_str = " ".join([str(a).lower() for a in actions_raw])
    
    # Required:🚑 Ambulance called if action contains "call ambulance"
    if "call ambulance" in actions_str or severity == "high":
        executed.append("🚑 Ambulance called (simulated)")

    # Required:🍬 Give sugar immediately if action contains "give sugar"
    if "give sugar" in actions_str:
        executed.append("🍬 Give sugar immediately")

    # Required: 📍 Location shared (simulated) (ALWAYS include)
    executed.append("📍 Location shared (simulated)")

    # Handle additional actions from intent
    for action in actions_raw:
        clean_action = str(action).strip().lower()
        if "call ambulance" not in clean_action and "give sugar" not in clean_action:
            executed.append(f"✅ Action Executed: {action}")

    return executed