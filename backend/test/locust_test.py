from locust import HttpUser, task, between

class LoginUser(HttpUser):
    wait_time = between(1, 3)  # delay between requests

    @task
    def login(self):
        self.client.post(
            "/auth/login",
            data={
                "username": "tim",
                "password": "Hello123",
                "grant_type": "password"
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        # self.client.get("/static/index.html")

if __name__ == "__main__":
    print("run:`locust -f .\test\locust_test.py --host=http://localhost:5000` in new terminal")
    print("visit http://localhost:8089 to see the results")