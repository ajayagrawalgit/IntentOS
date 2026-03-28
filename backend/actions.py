import httpx
import os
import logging
from typing import List, Dict, Any, Optional
from email_service import send_emergency_email, EMERGENCY_EMAIL_TO

logger = logging.getLogger("IntentOS")
MAPS_API_KEY = os.getenv("MAPS_API_KEY")

async def get_elevation(lat: float, lng: float) -> Optional[float]:
    """Calls Google Maps Elevation API to get altitude data."""
    if not lat or not lng or not MAPS_API_KEY:
        return None
    try:
        url = f"https://maps.googleapis.com/maps/api/elevation/json?locations={lat},{lng}&key={MAPS_API_KEY}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()
            if data["status"] == "OK":
                return data["results"][0]["elevation"]
    except Exception as e:
        logger.error(f"Elevation API failure: {e}")
    return None

async def execute_actions(analysis: Dict[str, Any], lat: float = None, lng: float = None, user_info: dict = None) -> List[str]:
    """Orchestrates actual and simulated actions based on AI analysis."""
    executed = []
    severity = str(analysis.get("severity", "low")).lower()
    if severity in ("none", ""):
        severity = "low"

    # High/Medium only: location, elevation, and emergency email
    is_critical = "high" in severity or "medium" in severity

    if is_critical:
        # Handle Real-World Mapping (Elevation Service)
        elevation = None
        if lat and lng:
            elevation = await get_elevation(lat, lng)
            elev_str = f" ({round(elevation, 1)}m altitude)" if elevation else ""
            executed.append(f"📍 Real-time Location Shared: {lat}, {lng}{elev_str}")
            
            # Automated Emergency Notifications (Mailing)
            location_data = {"lat": lat, "lng": lng, "elevation": elevation or "Unknown"}
            email_sent = send_emergency_email(user_info or {}, location_data, analysis)
            if email_sent:
                to_addr = EMERGENCY_EMAIL_TO or "configured recipient"
                executed.append(f"📧 Emergency notification dispatched to authorities & {to_addr}")
            else:
                executed.append("⚠️ Failed to dispatch emergency email (check credentials)")
        else:
            executed.append("📍 Simulated Location Shared (Location Access Denied)")
            executed.append("⚠️ Emergency email skipped: Missing precise location data.")
    else:
        # Low Severity Logic
        executed.append("✅ Status: Safety Confirmed (Non-Emergency)")

    # 2. Simulated System Resolutions (Always available)
    simulated = analysis.get("simulated_resolutions", [])
    if isinstance(simulated, list):
        for s in simulated:
            executed.append(f"🤖 Orchestrated: {s}")

    return executed