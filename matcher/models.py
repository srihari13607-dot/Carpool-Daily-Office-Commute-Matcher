from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Optional

class UserRole(str, Enum):
    DRIVER = "driver"
    RIDER = "rider"
    HYBRID_ALTERNATING = "hybrid"

class FuelType(str, Enum):
    PETROL = "petrol"
    DIESEL = "diesel"
    ELECTRIC = "electric"
    CNG = "cng"

@dataclass
class Location:
    name: str
    lat: float
    lng: float
    address: str = ""
    def to_dict(self):
        return asdict(self)

@dataclass
class Vehicle:
    make_model: str = "Sedan"
    seats_available: int = 3
    fuel_type: FuelType = FuelType.PETROL
    def to_dict(self):
        d = asdict(self)
        d["fuel_type"] = self.fuel_type.value
        return d

@dataclass
class CommuteSchedule:
    days: list = field(default_factory=lambda: ["Mon","Tue","Wed","Thu","Fri"])
    morning_departure: str = "08:30"
    morning_flex_mins: int = 15
    evening_departure: str = "17:30"
    evening_flex_mins: int = 20
    def to_dict(self):
        return asdict(self)

@dataclass
class CommutePreferences:
    women_only: bool = False
    quiet_ride: bool = False
    music_allowed: bool = True
    ac_preferred: bool = True
    pets_allowed: bool = False
    non_smoking: bool = True
    max_detour_km: float = 3.5
    max_detour_mins: int = 12
    def to_dict(self):
        return asdict(self)

@dataclass
class User:
    id: str
    name: str
    email: str
    company: str
    role: UserRole
    gender: str
    home_location: Location
    work_location: Location
    schedule: CommuteSchedule
    preferences: CommutePreferences
    rating: float = 5.0
    total_trips: int = 0
    verified_corporate: bool = True
    vehicle: Optional[Vehicle] = None
    def to_dict(self):
        return {
            "id": self.id, "name": self.name, "email": self.email,
            "company": self.company, "role": self.role.value,
            "gender": self.gender, "home_location": self.home_location.to_dict(),
            "work_location": self.work_location.to_dict(),
            "schedule": self.schedule.to_dict(),
            "preferences": self.preferences.to_dict(),
            "rating": self.rating, "total_trips": self.total_trips,
            "verified_corporate": self.verified_corporate,
            "vehicle": self.vehicle.to_dict() if self.vehicle else None
        }
