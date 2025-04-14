def basic_motion_repr_tests(client):
    a = client.motion_repr.create(
        log_id=173, sensor_frame_number=42, representation_name="dummy_representation"
    )
    print()
    print(a)

    b = client.motion_repr.get(id=a.id)
    print(b)

    c = client.motion_repr.list(log_id=2)
    print()
    print(c)

    d = client.motion_repr.update(id=a.id, representation_data=dict(a="Hello World"))
    print()
    print(d)

    e = client.motion_repr.delete(id=a.id)
    print(e)
