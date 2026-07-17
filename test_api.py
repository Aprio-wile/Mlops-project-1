def test_api_import():
    from app import api
    assert app.api.app is not None