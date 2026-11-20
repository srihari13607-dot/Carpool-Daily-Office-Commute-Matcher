from dataclasses import dataclass
from datetime import datetime
from .models import UserRole

@dataclass
class MatchResult:
    commuter: object
    score: float
    reasons: list
    def to_dict(self):
        return {
            "commuter": self.commuter.to_dict(),
            "score": round(self.score, 1),
            "reasons": self.reasons
        }

class CommuteMatchingEngine:
    @staticmethod
    def _minutes(t1, t2):
        try:
            a = datetime.strptime(t1, "%H:%M")
            b = datetime.strptime(t2, "%H:%M")
            return abs(int((a-b).total_seconds()/60))
        except Exception:
            return 999

    @staticmethod
    def _distance(a, b):
        # Approximate straight-line distance in kilometres.
        return ((a.lat-b.lat)**2 + (a.lng-b.lng)**2) ** 0.5 * 111

    def _match(self, target, candidates, min_score):
        results = []
        for person in candidates:
            if person.id == target.id:
                continue
            score, reasons = 0.0, []
            home_km = self._distance(target.home_location, person.home_location)
            work_km = self._distance(target.work_location, person.work_location)
            time_gap = self._minutes(target.schedule.morning_departure,
                                     person.schedule.morning_departure)
            common_days = set(target.schedule.days) & set(person.schedule.days)

            if work_km <= 5:
                score += 30; reasons.append("Office destinations are nearby")
            elif work_km <= 12:
                score += 18; reasons.append("Office destinations are within a reasonable area")
            if home_km <= 5:
                score += 25; reasons.append("Home locations are nearby")
            elif home_km <= 12:
                score += 15; reasons.append("Home locations are in a similar area")
            if time_gap <= 15:
                score += 25; reasons.append("Departure times are within 15 minutes")
            elif time_gap <= 30:
                score += 15; reasons.append("Departure times are within 30 minutes")
            if common_days:
                score += min(20, len(common_days)*4)
                reasons.append(f"{len(common_days)} common commute days")
            if person.role in (UserRole.DRIVER, UserRole.HYBRID_ALTERNATING):
                score += 5
                if person.vehicle:
                    reasons.append(f"Vehicle: {person.vehicle.make_model}")
            score = min(score, 100)
            if score >= min_score:
                results.append(MatchResult(person, score, reasons))
        return sorted(results, key=lambda x: x.score, reverse=True)

    def find_matches_for_rider(self, target_user, commuters, min_score=40.0):
        candidates = [u for u in commuters if u.role in (UserRole.DRIVER, UserRole.HYBRID_ALTERNATING)]
        return self._match(target_user, candidates, min_score)

    def find_matches_for_driver(self, target_user, commuters, min_score=40.0):
        candidates = [u for u in commuters if u.role in (UserRole.RIDER, UserRole.HYBRID_ALTERNATING)]
        return self._match(target_user, candidates, min_score)

    def find_alternating_pairs(self, commuters):
        drivers = [u for u in commuters if u.role == UserRole.HYBRID_ALTERNATING]
        pairs = []
        for i, a in enumerate(drivers):
            for b in drivers[i+1:]:
                score = self._distance(a.home_location,b.home_location) + self._distance(a.work_location,b.work_location)
                if score <= 20:
                    pairs.append({"commuter_1": a.name, "commuter_2": b.name,
                                  "combined_route_distance_indicator_km": round(score,1),
                                  "suggestion": "Review schedules and agree on alternating days."})
        return pairs
