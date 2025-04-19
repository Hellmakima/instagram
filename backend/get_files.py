files = [
    "app/static/login.html",
    "app/static/me.html",
    "app/auth/routes.py",
    "app/auth/utils.py",
    "app/main.py",
]

a = ""

for file in files:
    with open(file, "r") as f:
        a += file
        a += "\n"
        a += f.read()
        a += "\n"

with open("context.txt", "w") as f:
    f.write(a)