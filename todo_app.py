from flask import Flask, render_template, request, redirect, url_for, flash, session

app = Flask(__name__)
app.config["SECRET_KEY"] = "super_secret"

todo_list = ["Develop Todo web application", "Add 'add new' feature"]
users = {"levdalba": {"password": "12345", "name": "Lev"}}


def check_password(login, password):
    return login in users and users[login]["password"] == password


@app.route("/")
def index():
    if not session.get("user_login"):
        return redirect(url_for("login"))
    return render_template("index.html", todo_list=todo_list)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        if check_password(login, password):
            session["user_login"] = login
            return redirect(url_for("index"))
        else:
            flash("User doesn't exist or password is incorrect. Please try again.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_login", None)
    return redirect(url_for("login"))


@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    if request.method == "POST":
        task = request.form.get("task")
        if task:
            todo_list.append(task)
        return redirect(url_for("index"))
    return render_template("add_task.html")


@app.route("/delete_task/<int:task_id>", methods=["POST"])
def delete_task(task_id):
    if 0 <= task_id < len(todo_list):
        del todo_list[task_id]
    return redirect(url_for("index"))


@app.route("/mark_done/<int:task_id>", methods=["POST"])
def mark_done(task_id):
    if 0 <= task_id < len(todo_list):
        todo_list[task_id] = f"{todo_list[task_id]} (done)"
    return redirect(url_for("index"))


@app.route("/change_theme", methods=["POST"])
def change_theme():
    session["theme"] = "dark" if session.get("theme") == "light" else "light"
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, port=8000)
