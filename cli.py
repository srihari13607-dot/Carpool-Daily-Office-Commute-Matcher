from matcher.sample_data import get_sample_commuters
from matcher.engine import CommuteMatchingEngine
from matcher.models import UserRole

people = get_sample_commuters()
engine = CommuteMatchingEngine()
print("Carpool Connect CLI")
for i,u in enumerate(people,1):
    print(f"{i}. {u.name} ({u.company}) - {u.role.value}")
choice = int(input("Select commuter number: "))
target = people[choice-1]
if target.role in (UserRole.DRIVER,UserRole.HYBRID_ALTERNATING):
    matches = engine.find_matches_for_driver(target,people)
else:
    matches = engine.find_matches_for_rider(target,people)
for match in matches:
    print(f"{match.commuter.name}: {match.score:.1f}% - {', '.join(match.reasons)}")
