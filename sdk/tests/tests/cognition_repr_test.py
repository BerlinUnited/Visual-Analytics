def basic_cognition_repr_tests(client):
    a = client.cognition_repr.create(
        log_id=173, frame_number=42, representation_name="dummy_representation"
    )
    print()
    print(a)

    b = client.cognition_repr.get(id=a.id)
    print(b)

    c = client.cognition_repr.list(log_id=173)
    print()
    print(c)

    d = client.cognition_repr.update(id=a.id, representation_data=dict(a="Hello World"))
    print()
    print(d)

    e = client.cognition_repr.delete(id=a.id)
    print(e)
