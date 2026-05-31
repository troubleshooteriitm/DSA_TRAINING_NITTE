"""
API Basics Practice
====================
Simulated API interactions without external dependencies.
Demonstrates: JSON processing, request/response patterns, error handling.
"""

import json
from datetime import datetime


# ============================================================
# SIMULATED API SERVER
# ============================================================

class MockAPIServer:
    """Simulates a REST API server using in-memory data."""

    def __init__(self):
        self.users = {
            1: {"id": 1, "name": "Alice", "email": "alice@example.com", "role": "admin"},
            2: {"id": 2, "name": "Bob", "email": "bob@example.com", "role": "user"},
            3: {"id": 3, "name": "Charlie", "email": "charlie@example.com", "role": "user"},
        }
        self.next_id = 4

    def _response(self, status_code, data=None, error=None):
        """Create a standardized API response."""
        resp = {
            "status_code": status_code,
            "timestamp": datetime.now().isoformat(),
        }
        if data is not None:
            resp["data"] = data
        if error:
            resp["error"] = error
        return resp

    def get(self, endpoint, params=None):
        """Simulate GET request."""
        if endpoint == "/users":
            return self._response(200, list(self.users.values()))

        if endpoint.startswith("/users/"):
            try:
                user_id = int(endpoint.split("/")[-1])
                if user_id in self.users:
                    return self._response(200, self.users[user_id])
                return self._response(404, error="User not found")
            except ValueError:
                return self._response(400, error="Invalid user ID")

        return self._response(404, error=f"Endpoint not found: {endpoint}")

    def post(self, endpoint, body=None):
        """Simulate POST request."""
        if endpoint == "/users":
            if not body or "name" not in body or "email" not in body:
                return self._response(400, error="Missing required fields: name, email")

            new_user = {
                "id": self.next_id,
                "name": body["name"],
                "email": body["email"],
                "role": body.get("role", "user"),
            }
            self.users[self.next_id] = new_user
            self.next_id += 1
            return self._response(201, new_user)

        return self._response(404, error=f"Endpoint not found: {endpoint}")

    def put(self, endpoint, body=None):
        """Simulate PUT request."""
        if endpoint.startswith("/users/"):
            try:
                user_id = int(endpoint.split("/")[-1])
                if user_id not in self.users:
                    return self._response(404, error="User not found")
                if body:
                    self.users[user_id].update(body)
                return self._response(200, self.users[user_id])
            except ValueError:
                return self._response(400, error="Invalid user ID")

        return self._response(404, error=f"Endpoint not found")

    def delete(self, endpoint):
        """Simulate DELETE request."""
        if endpoint.startswith("/users/"):
            try:
                user_id = int(endpoint.split("/")[-1])
                if user_id in self.users:
                    deleted = self.users.pop(user_id)
                    return self._response(200, {"message": f"User {deleted['name']} deleted"})
                return self._response(404, error="User not found")
            except ValueError:
                return self._response(400, error="Invalid user ID")

        return self._response(404, error="Endpoint not found")


# ============================================================
# API CLIENT
# ============================================================

class APIClient:
    """Client that interacts with the mock API."""

    def __init__(self, server):
        self.server = server

    def handle_response(self, response, operation=""):
        """Process and display API response."""
        status = response["status_code"]
        icon = "" if status < 400 else ""
        print(f"  {icon} [{status}] {operation}")

        if "data" in response:
            print(f"     Data: {json.dumps(response['data'], indent=2)[:200]}")
        if "error" in response:
            print(f"     Error: {response['error']}")
        return response


# ============================================================
# DEMO
# ============================================================

if __name__ == "__main__":
    print("=" * 55)
    print("  API BASICS -- SIMULATED REST API")
    print("=" * 55)

    server = MockAPIServer()
    client = APIClient(server)

    # GET all users
    print("\n--- GET /users ---")
    resp = server.get("/users")
    client.handle_response(resp, "GET /users")

    # GET single user
    print("\n--- GET /users/1 ---")
    resp = server.get("/users/1")
    client.handle_response(resp, "GET /users/1")

    # GET non-existent user
    print("\n--- GET /users/99 ---")
    resp = server.get("/users/99")
    client.handle_response(resp, "GET /users/99")

    # POST new user
    print("\n--- POST /users ---")
    new_user = {"name": "Diana", "email": "diana@example.com", "role": "moderator"}
    resp = server.post("/users", body=new_user)
    client.handle_response(resp, "POST /users (create Diana)")

    # POST with missing fields
    print("\n--- POST /users (invalid) ---")
    resp = server.post("/users", body={"name": "Eve"})
    client.handle_response(resp, "POST /users (missing email)")

    # PUT update user
    print("\n--- PUT /users/2 ---")
    resp = server.put("/users/2", body={"name": "Bob Updated", "role": "admin"})
    client.handle_response(resp, "PUT /users/2 (update Bob)")

    # DELETE user
    print("\n--- DELETE /users/3 ---")
    resp = server.delete("/users/3")
    client.handle_response(resp, "DELETE /users/3 (delete Charlie)")

    # Verify deletion
    print("\n--- GET /users (after changes) ---")
    resp = server.get("/users")
    client.handle_response(resp, "GET /users (final state)")

    # JSON processing demo
    print("\n--- JSON Processing ---")
    response_json = json.dumps(resp["data"], indent=2)
    print(f"  Pretty JSON:\n{response_json}")

    parsed = json.loads(response_json)
    print(f"\n  Parsed back: {len(parsed)} users")
    for user in parsed:
        print(f"    {user['id']}: {user['name']} ({user['role']})")
