from locust import HttpUser, task, between


class LoginUser(HttpUser):
    wait_time = between(1, 3)  # delay between requests
    host = "http://localhost:5000"  # Define host here for easier management

    def on_start(self):
        """on_start is called when a Locust user starts running"""
        self.access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDk5NjAzNDQsInN1YiI6ImpzaGJmdXliIiwidHlwZSI6IkJlYXJlciJ9.8JOG55YieVTUN0TGguTfgpL03KqwMYKknWlVRBdqE90"
        self.login()  # Call login once at the start

    @task
    def access_me_html(self):
        if self.access_token:
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Content-Type": "text/html",  # Or whatever content type me.html serves
            }
            self.client.get(
                "/static/test/me.html", headers=headers, name="/me.html [authenticated]"
            )
        else:
            print("No access token available. Login might have failed.")
            # You might want to re-attempt login or log this as a failure

    def login(self):
        response = self.client.post(
            "/auth/login",
            data={
                "username": "jshbfuyb",
                "password": "klksbiurE3",
                "grant_type": "password",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            name="/auth/login",
        )
        # self.client.get("/static/index.html")

        if response.status_code == 202:
            try:
                # Assuming your login endpoint returns JSON with an access_token
                self.access_token = response.json().get("access_token")
                print(
                    f"Login successful. Access Token: {self.access_token[:10]}..."
                )  # Print first 10 chars
            except Exception as e:
                print(f"Failed to parse login response or get access token: {e}")
                self.access_token = None
        else:
            print(f"Login failed with status code: {response.status_code}")
            self.access_token = None


if __name__ == "__main__":
    print(
        "run:`locust -f .\test\locust_test.py --host=http://localhost:5000` in new terminal"
    )
    print("or:`locust -f .\test\locust_test.py")
    print("visit http://localhost:8089 to see the results")
