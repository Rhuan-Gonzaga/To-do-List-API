def test_create_task(client, auth_token):
    response = client.post("/api/tasks/create", 
        json={"title": "Tarefa 1"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 201
    assert b"Tarefa criada com sucesso" in response.data

def test_get_tasks(client, auth_token):
    # cria tarefa
    client.post("/api/tasks/create", 
        json={"title": "Tarefa para listar"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    # lista tarefas
    response = client.get("/api/tasks/", headers={"Authorization": f"Bearer {auth_token}"})
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) >= 1
