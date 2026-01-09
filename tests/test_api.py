import copy
import urllib.parse

from fastapi.testclient import TestClient

from src.app import app, activities


original_activities = copy.deepcopy(activities)


def reset_activities():
    activities.clear()
    activities.update(copy.deepcopy(original_activities))


def test_get_activities():
    reset_activities()
    client = TestClient(app)
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_and_unregister_flow():
    reset_activities()
    client = TestClient(app)

    activity = "Chess Club"
    email = "tester@example.com"

    # Sign up
    path = f"/activities/{urllib.parse.quote(activity)}/signup"
    resp = client.post(path, params={"email": email})
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]

    # Signing up again returns 400
    resp2 = client.post(path, params={"email": email})
    assert resp2.status_code == 400

    # Unregister
    del_path = f"/activities/{urllib.parse.quote(activity)}/unregister"
    resp3 = client.delete(del_path, params={"email": email})
    assert resp3.status_code == 200
    assert email not in activities[activity]["participants"]


def test_unregister_nonexistent_student():
    reset_activities()
    client = TestClient(app)

    activity = "Programming Class"
    email = "not-registered@example.com"

    del_path = f"/activities/{urllib.parse.quote(activity)}/unregister"
    resp = client.delete(del_path, params={"email": email})
    assert resp.status_code == 400
