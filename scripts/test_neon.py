"""
Manual verification script for LaunchWeave API.
Run against a running local or remote server:
    python scripts/test_neon.py http://127.0.0.1:8000
"""

import sys
import requests

BASE_URL = sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8000"

def test_neon_api():
    print(f"Testing LaunchWeave API at {BASE_URL}...")
    
    print("Testing /healthz...")
    resp = requests.get(f"{BASE_URL}/healthz", timeout=10)
    print(f"  Healthz: {resp.status_code}, {resp.json()}")
    assert resp.status_code == 200

    print("Testing /readyz...")
    resp = requests.get(f"{BASE_URL}/readyz", timeout=10)
    print(f"  Readyz: {resp.status_code}, {resp.json()}")
    assert resp.status_code == 200

    print("\nTesting POST /tasks...")
    task_data = {"title": "Neon Verification Task", "description": "Testing against database"}
    resp = requests.post(f"{BASE_URL}/tasks", json=task_data, timeout=10)
    print(f"  Create: {resp.status_code}, {resp.json()}")
    assert resp.status_code == 201
    task_id = resp.json()["id"]

    print("\nTesting GET /tasks...")
    resp = requests.get(f"{BASE_URL}/tasks", timeout=10)
    print(f"  Get: {resp.status_code}, {len(resp.json())} tasks found")
    assert resp.status_code == 200
    assert any(t["id"] == task_id for t in resp.json())

    print(f"\nTesting PATCH /tasks/{task_id}...")
    update_data = {"title": "Updated Verification Task", "completed": True}
    resp = requests.patch(f"{BASE_URL}/tasks/{task_id}", json=update_data, timeout=10)
    print(f"  Update: {resp.status_code}, {resp.json()}")
    assert resp.status_code == 200
    assert resp.json()["completed"] is True

    print(f"\nTesting DELETE /tasks/{task_id}...")
    resp = requests.delete(f"{BASE_URL}/tasks/{task_id}", timeout=10)
    print(f"  Delete status: {resp.status_code}")
    assert resp.status_code == 204

    print("\nAll integration verification checks passed successfully!")

if __name__ == "__main__":
    try:
        test_neon_api()
    except Exception as e:
        print(f"\nTest failed with error: {e}")
        sys.exit(1)
