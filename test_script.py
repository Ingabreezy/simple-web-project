import requests

def test_homepage():
    response = requests.get('http://localhost:8000')
    assert response.status_code == 200
    assert "Welcome to the Simple Web Project" in response.text

if __name__ == "__main__":
    test_homepage()
    print("All tests passed!")
