from flask import Blueprint, render_template
from flask_login import login_required, current_user
from ..models import Repo, Scan, Finding

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/")
@login_required
def home():
    repos = Repo.query.filter_by(user_id=current_user.id).all()

    # Latest 25 findings for this user (across all repos)
    findings = (
        Finding.query
        .join(Scan, Finding.scan_id == Scan.id)
        .join(Repo, Scan.repo_id == Repo.id)
        .filter(Repo.user_id == current_user.id)
        .order_by(Finding.id.desc())
        .limit(25)
        .all()
    )

    return render_template("dashboard.html", user=current_user, repos=repos, findings=findings)
