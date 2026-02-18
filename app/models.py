import bcrypt
from flask_login import UserMixin
from . import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.LargeBinary(60), nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    def check_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode("utf-8"), self.password_hash)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

import secrets

class Repo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    ingest_token = db.Column(db.String(64), unique=True, nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    user = db.relationship("User", backref="repos")

    @staticmethod
    def generate_token():
        return secrets.token_hex(32)
from datetime import datetime

class Scan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    repo_id = db.Column(db.Integer, db.ForeignKey("repo.id"), nullable=False, index=True)
    tool = db.Column(db.String(50), nullable=False)  # trivy | gitleaks
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    status = db.Column(db.String(20), default="success", nullable=False)  # success|fail

    repo = db.relationship("Repo", backref="scans")


class Finding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scan_id = db.Column(db.Integer, db.ForeignKey("scan.id"), nullable=False, index=True)
    severity = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), nullable=False, default="open")
    ALLOWED_STATUSES = {"open", "fixed", "ignored"}
    title = db.Column(db.String(500), nullable=False)
    pkg = db.Column(db.String(255), nullable=True)
    installed_version = db.Column(db.String(100), nullable=True)
    fixed_version = db.Column(db.String(100), nullable=True)

    scan = db.relationship("Scan", backref="findings")