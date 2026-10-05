"""Register Farol's Trino connection through Superset's local API."""
import os
import time
import requests


def main():
    base = "http://127.0.0.1:8088"
    session = requests.Session()
    for attempt in range(60):
        try:
            response = session.get(base + "/health", timeout=2)
            if response.ok:
                break
        except requests.RequestException:
            pass
        time.sleep(2)
    else:
        raise RuntimeError("Superset health check timed out")
    response = session.post(base + "/api/v1/security/login", json={
        "username": "admin", "password": os.environ["SUPERSET_ADMIN_PASSWORD"],
        "provider": "db", "refresh": True,
    }, timeout=30)
    response.raise_for_status()
    session.headers["Authorization"] = "Bearer " + response.json()["access_token"]
    response = session.get(base + "/api/v1/database/", timeout=30)
    response.raise_for_status()
    if any(d["database_name"] == "Farol" for d in response.json()["result"]):
        print("Farol Trino connection already registered")
        return
    response = session.post(base + "/api/v1/database/", json={
        "database_name": "Farol", "sqlalchemy_uri": "trino://farol@trino:8080/lake",
        "expose_in_sqllab": True,
    }, timeout=30)
    response.raise_for_status()
    print("Farol Trino connection registered")


if __name__ == "__main__":
    main()
