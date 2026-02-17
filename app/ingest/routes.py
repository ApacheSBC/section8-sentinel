from flask import Blueprint, request, jsonify
from ..models import Repo, Scan, Finding
from .. import db

ingest_bp = Blueprint("ingest", __name__, url_prefix="/api/ingest")


def get_repo_from_token():
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        return None
    token = auth.replace("Bearer ", "", 1).strip()
    return Repo.query.filter_by(ingest_token=token).first()


@ingest_bp.route("/trivy", methods=["POST"])
def ingest_trivy():
    repo = get_repo_from_token()
    if not repo:
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "invalid json"}), 400

    scan = Scan(repo_id=repo.id, tool="trivy", status="success")
    db.session.add(scan)
    db.session.flush()

    results = data.get("Results", [])
    count = 0

    for r in results:
        vulns = r.get("Vulnerabilities") or []
        for v in vulns:
            finding = Finding(
                scan_id=scan.id,
                severity=v.get("Severity"),
                title=v.get("Title") or v.get("VulnerabilityID") or "Trivy Finding",
                pkg=v.get("PkgName"),
                installed_version=v.get("InstalledVersion"),
                fixed_version=v.get("FixedVersion"),
            )
            db.session.add(finding)
            count += 1

    db.session.commit()
    return jsonify({"ok": True, "repo": repo.name, "tool": "trivy", "findings": count}), 200

@ingest_bp.route("/gitleaks", methods=["POST"])
def ingest_gitleaks():
    repo = get_repo_from_token()
    if not repo:
        return jsonify({"error": "unauthorized"}), 401

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "invalid json"}), 400

    scan = Scan(repo_id=repo.id, tool="gitleaks", status="success")
    db.session.add(scan)
    db.session.flush()

    findings = data if isinstance(data, list) else data.get("findings") or []
    count = 0

    for f in findings:
        rule = f.get("RuleID") or f.get("Rule") or "Gitleaks"
        file_ = f.get("File") or ""
        line = f.get("StartLine") or f.get("Line") or ""
        desc = f.get("Description") or ""

        db.session.add(Finding(
            scan_id=scan.id,
            severity="HIGH",
            title=f"Secret detected: {rule} {('- ' + desc) if desc else ''}".strip(),
            pkg=file_,
            installed_version=str(line) if line != "" else None,
            fixed_version=None,
        ))
        count += 1

    db.session.commit()
    return jsonify({"ok": True, "repo": repo.name, "tool": "gitleaks", "findings": count}), 200
