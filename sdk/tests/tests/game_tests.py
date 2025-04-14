import datetime as dt


def basic_game_tests(client):
    a = client.games.create(
        event=1, is_testgame=True, half="half1", start_time=dt.date.today()
    )
    print(a)

    b = client.games.get(id=a.id)
    print(b)

    c = client.games.list(event_id=1)
    print(c)
    print()

    d = client.games.update(a.id, field="A")
    print(d)
    print()

    e = client.games.delete(a.id)
    print(e)
