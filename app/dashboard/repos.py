from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from ..models import Repo
from .. import db

repos_bp = Blueprint("repos", __name__, url_prefix="/repos")


@repos_bp.route("/add", methods=["GET", "POST"])
@login_required
def add_repo():
    if request.method == "POST":
        name = request.form.get("name")
        url = request.form.get("url")

        token = Repo.generate_token()

        repo = Repo(
            name=name,
            url=url,
            ingest_token=token,
            user_id=current_user.id
        )

        db.session.add(repo)
        db.session.commit()

        return redirect(url_for("dashboard.home"))

    return render_template("add_repo.html")
