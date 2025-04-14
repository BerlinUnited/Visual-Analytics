def basic_log_tests(client):
    a = client.logs.create(game=2, player_number=42)
    print()
    print(a)

    b = client.logs.get(id=a.id)
    print(b)

    c = client.logs.list(game_id=2)
    print()
    print(len(c))

    d = client.logs.update(id=a.id, player_number=13)
    print()
    print(d)

    e = client.logs.delete(id=a.id)
    print(e)
