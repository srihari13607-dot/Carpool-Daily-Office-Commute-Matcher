"""Optional Flask REST API for the bundled Carpool Connect demo."""
from flask import Flask, jsonify, request
from matcher.models import UserRole
from matcher.engine import CommuteMatchingEngine
from matcher.sample_data import get_sample_commuters, WORK_HUBS, HOME_HUBS

app = Flask(__name__)
engine = CommuteMatchingEngine()
commuters = get_sample_commuters()

@app.get("/api/hubs")
def get_hubs():
    return jsonify({
        "work_hubs": {k:v.to_dict() for k,v in WORK_HUBS.items()},
        "home_hubs": {k:v.to_dict() for k,v in HOME_HUBS.items()}
    })

@app.get("/api/commuters")
def list_commuters():
    role = request.args.get("role")
    company = request.args.get("company")
    result = commuters
    if role:
        result = [u for u in result if u.role.value == role]
    if company:
        result = [u for u in result if u.company.lower() == company.lower()]
    return jsonify([u.to_dict() for u in result])

@app.post("/api/match")
def run_match():
    data = request.get_json(silent=True) or {}
    user_id = data.get("user_id")
    target = next((u for u in commuters if u.id == user_id), None)
    if not target:
        return jsonify({"error":"Provide a valid sample user_id"}), 400
    score = float(data.get("min_score",40))
    if target.role in (UserRole.DRIVER,UserRole.HYBRID_ALTERNATING):
        matches = engine.find_matches_for_driver(target,commuters,score)
    else:
        matches = engine.find_matches_for_rider(target,commuters,score)
    return jsonify({"target_user":target.to_dict(),"total_matches":len(matches),
                    "matches":[m.to_dict() for m in matches]})

@app.get("/api/alternating-pairs")
def alternating_pairs():
    pairs = engine.find_alternating_pairs(commuters)
    return jsonify({"total_pairs":len(pairs),"pairs":pairs})

@app.get("/api/stats")
def stats():
    return jsonify({"active_commuters":len(commuters),
        "drivers_with_seats":sum(u.role in (UserRole.DRIVER,UserRole.HYBRID_ALTERNATING) for u in commuters),
        "riders_registered":sum(u.role in (UserRole.RIDER,UserRole.HYBRID_ALTERNATING) for u in commuters),
        "partner_companies":len(set(u.company for u in commuters))})

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )
