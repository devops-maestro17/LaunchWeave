import requests

BASE_URL = "http://127.0.0.1:8000"

def test_neon_api():
    print("Testing /healthz...")
    resp = requests.get(f"{BASE_URL}/healthz")
    print(f"Healthz: {resp.status_code}, {resp.json()}")
    assert resp.status_code == 200

    print("\nTesting POST /tasks...")
    task_data = {"title": "Neon Task", "description": "Testing on Neon DB"}
    resp = requests.post(f"{BASE_URL}/tasks", json=task_data)
    print(f"Create: {resp.status_code}, {resp.json()}")
    assert resp.status_code == 201
    task_id = resp.json()["id"]

    print("\nTesting GET /tasks...")
    resp = requests.get(f"{BASE_URL}/tasks")
    print(f"Get: {resp.status_code}, {len(resp.json())} tasks")
    assert resp.status_code == 200
    assert any(t["id"] == task_id for t in resp.json())

    print("\nTesting PATCH /tasks/{id}...")
    update_data = {"title": "Updated Neon Task"}
    resp = requests.patch(f"{BASE_URL}/tasks/{task_id}", json=update_data)
    print(f"Update: {resp.status_code}, {resp.json()}")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Updated Neon Task"

    print("\nTesting DELETE /tasks/{id}...")
    resp = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    print(f"Delete: {resp.status_code}")
    assert resp.status_code == 204

    print("\nAll tests passed!")

if __name__ == "__main__":
    try:
        test_neon_api()
    except Exception as e:
        print(f"Test failed: {e}")
        exit(1)
