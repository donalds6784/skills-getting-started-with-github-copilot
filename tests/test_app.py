from fastapi.testclient import TestClient
import uuid

from src.app import app


client = TestClient(app)


def test_get_activities():
    resp = client.get('/activities')
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    # Expect some known activity keys are present
    assert 'Chess Club' in data


def test_signup_and_unregister_flow():
    # Use a unique email so repeated test runs don't conflict
    unique_email = f"test.user+{uuid.uuid4().hex}@example.com"
    activity = 'Chess Club'

    # Get initial participants
    resp = client.get('/activities')
    assert resp.status_code == 200
    before = resp.json()
    before_participants = list(before[activity]['participants'])

    # Sign up
    signup_resp = client.post(
        f"/activities/{activity}/signup", params={"email": unique_email})
    assert signup_resp.status_code == 200
    signup_data = signup_resp.json()
    assert 'Signed up' in signup_data.get('message', '')

    # Verify participant is present
    resp_after = client.get('/activities')
    assert resp_after.status_code == 200
    after = resp_after.json()
    assert unique_email in after[activity]['participants']

    # Unregister
    unregister_resp = client.post(
        f"/activities/{activity}/unregister", params={"email": unique_email})
    assert unregister_resp.status_code == 200
    unregister_data = unregister_resp.json()
    assert 'Unregistered' in unregister_data.get('message', '')

    # Verify participant removed
    resp_final = client.get('/activities')
    assert resp_final.status_code == 200
    final = resp_final.json()
    assert unique_email not in final[activity]['participants']
