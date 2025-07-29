def test_signup(client):
    response = client.post("/api/users/signup", json={
        "username": "testuser",
        "password": "password123"
    })
    data = response.get_json()
    assert response.status_code == 201
    assert data["message"] == "Usuário cadastrado com sucesso!"


def test_login(client):
    # cria usuário
    client.post("/api/users/signup", json={
        "username": "testuser2",
        "password": "password123"
    })

    # faz login
    response = client.post("/api/users/login", json={
        "username": "testuser2",
        "password": "password123"
    })

    assert response.status_code == 200
    data = response.get_json()
    assert "token" in data
