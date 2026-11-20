from .models import *

HOME_HUBS = {
    "Gandhipuram": Location("Gandhipuram", 11.0183, 76.9665, "Coimbatore"),
    "Peelamedu": Location("Peelamedu", 11.0240, 77.0020, "Coimbatore"),
    "Singanallur": Location("Singanallur", 11.0000, 77.0280, "Coimbatore"),
    "Saravanampatti": Location("Saravanampatti", 11.0800, 76.9950, "Coimbatore"),
}
WORK_HUBS = {
    "TIDEL Park": Location("TIDEL Park", 11.0250, 77.0360, "Coimbatore"),
    "KG Tech Park": Location("KG Tech Park", 11.0180, 77.0100, "Coimbatore"),
    "Codissia": Location("Codissia", 11.0370, 77.0430, "Coimbatore"),
}

def get_sample_commuters():
    people = [
        ("u1","Arun","TechCorp",UserRole.DRIVER,"Gandhipuram","TIDEL Park","08:30","Sedan",3),
        ("u2","Priya","TechCorp",UserRole.RIDER,"Peelamedu","TIDEL Park","08:35",None,0),
        ("u3","Karthik","InnoSoft",UserRole.DRIVER,"Singanallur","KG Tech Park","08:20","Hatchback",2),
        ("u4","Divya","TechCorp",UserRole.RIDER,"Gandhipuram","TIDEL Park","08:25",None,0),
        ("u5","Naveen","InnoSoft",UserRole.HYBRID_ALTERNATING,"Saravanampatti","Codissia","08:40","SUV",3),
        ("u6","Meena","TechCorp",UserRole.DRIVER,"Peelamedu","TIDEL Park","08:32","Sedan",2),
    ]
    result = []
    for uid,name,company,role,home,work,time,model,seats in people:
        vehicle = Vehicle(model, seats, FuelType.PETROL) if model else None
        result.append(User(
            uid,name,f"{name.lower()}@example.com",company,role,"Female" if name in ("Priya","Divya","Meena") else "Male",
            HOME_HUBS[home],WORK_HUBS[work],
            CommuteSchedule(morning_departure=time),
            CommutePreferences(women_only=False),
            rating=4.7,total_trips=12,verified_corporate=True,vehicle=vehicle
        ))
    return result
