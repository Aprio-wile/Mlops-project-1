def test_api_import():
    from app import api
    assert api.app is not None


if __name__ == "__main__":
    test_api_import()