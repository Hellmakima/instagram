Got it — if each service is its own repo with its own Docker image, the clean way is to add a **deployment repo** that only holds infra (nginx + docker-compose). Then you pull images for each service.

Example:

```
deployment/
├── docker-compose.yml
└── nginx/
    └── nginx.conf
```

Each service stays in its own repo, and the deployment repo pulls the images.

```
auth-service/        # repo 1
├── Dockerfile
├── requirements.txt
└── app/...

user-service/        # repo 2
├── Dockerfile
└── app/...

payment-service/     # repo 3
├── Dockerfile
└── app/...

frontend/            # repo 4
├── Dockerfile
├── package.json
└── src/...
```

- **deployment repo** = just Compose + nginx config.
- **service repos** = own `Dockerfile`, build, and push image to registry.
- `docker-compose.yml` in `deployment/` references images like `myorg/auth-service:latest`.

Want me to draft that `docker-compose.yml` so you see how the images plug together?

Yes — as long as they’re on the **same Docker network**, containers can communicate using each other’s **service name or container name** as the hostname.

- With **docker-compose**, this happens automatically: each service is on a default network named after your project.
- Example: from `nginx` container, you can reach `auth-service` at `http://auth-service:8000`.
- No need for IPs; Docker’s internal DNS handles it.
