from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user

from app.models import Repo, Scan, Finding, db
from . import dashboard_bp


@dashboard_bp.route("/")
@login_required
def home():
    repos = Repo.query.filter_by(user_id=current_user.id).all()

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


@dashboard_bp.post("/findings/<int:finding_id>/status")
@login_required
def update_finding_status(finding_id):
    new_status = (request.form.get("status") or "").strip().lower()

    if new_status not in Finding.ALLOWED_STATUSES:
        flash("Invalid status selected.", "error")
        return redirect(url_for("dashboard.home"))

    finding = Finding.query.get_or_404(finding_id)

    # Ownership check: ensure finding belongs to current user
    is_owner = (
        db.session.query(Repo.id)
        .join(Scan, Scan.repo_id == Repo.id)
        .join(Finding, Finding.scan_id == Scan.id)
        .filter(Finding.id == finding_id, Repo.user_id == current_user.id)
        .first()
    )
    if not is_owner:
        abort(403)

    finding.status = new_status
    db.session.commit()

    flash("Finding status updated.", "success")
    return redirect(url_for("dashboard.home"))
