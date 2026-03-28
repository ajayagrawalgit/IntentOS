#!/usr/bin/env python3
"""
Integration-style checks for proportional response (no live Gemini / Maps / SMTP).
Run from src/backend: cd src/backend && python verify_proportional_response.py
"""
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

import main


def test_high_medium_runs_location_and_email():
    analysis = {
        "intent": "Medical emergency",
        "severity": "high",
        "condition": "test",
        "immediate_actions": ["Call emergency services"],
        "simulated_resolutions": ["EMS notified (simulated)"],
    }
    with patch.object(main, "extract_intent", return_value=analysis), patch(
        "actions.send_emergency_email", return_value=True
    ) as send_mail, patch("actions.get_elevation", new_callable=AsyncMock) as elev:
        elev.return_value = 100.5
        client = TestClient(main.app)
        resp = client.post(
            "/process",
            data={"text": "help", "lat": "37.77", "lng": "-122.42"},
        )
        assert resp.status_code == 200
        body = resp.json()
        actions = body["executed_actions"]
        assert send_mail.called
        assert elev.called
        assert any("Real-time Location Shared" in a for a in actions)
        assert any("📧" in a for a in actions)
        assert not any("Safety Confirmed" in a for a in actions)


def test_low_skips_location_and_email():
    analysis = {
        "intent": "Routine question",
        "severity": "low",
        "condition": "Non-urgent",
        "immediate_actions": ["N/A"],
        "simulated_resolutions": ["Acknowledged"],
    }
    with patch.object(main, "extract_intent", return_value=analysis), patch(
        "actions.send_emergency_email", return_value=True
    ) as send_mail, patch("actions.get_elevation", new_callable=AsyncMock) as elev:
        elev.return_value = 50.0
        client = TestClient(main.app)
        resp = client.post(
            "/process",
            data={"text": "hello", "lat": "40.0", "lng": "-74.0"},
        )
        assert resp.status_code == 200
        body = resp.json()
        actions = body["executed_actions"]
        assert not send_mail.called
        assert not elev.called
        assert any("Safety Confirmed" in a for a in actions)
        assert not any("Real-time Location Shared" in a for a in actions)


if __name__ == "__main__":
    test_high_medium_runs_location_and_email()
    print("PASS: high severity uses location + email path")
    test_low_skips_location_and_email()
    print("PASS: low severity skips location + email, shows Safety Confirmed")
