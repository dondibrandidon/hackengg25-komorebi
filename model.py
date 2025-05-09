from dataclasses import dataclass

DAYS_PER_MONTH = 28
MONTHS_PER_YEAR = 12
YEAR_LOWER = -5000
YEAR_UPPER = 100

SPECIES_AGEFACTOR = {
    "human": 100,
    "elven": 560,
    "dwarf": 140,
    "orc": 67,
    "beastfolk": 89,
    "demon": 280,
    "dragonkin": 420,
    "beltran": 100,
    "animalkin": 14,
}


@dataclass(frozen=True)
class Birthday:
    day: int
    month: int
    year: int


type Preferences = dict[
    Literal["species"]: Optional[set[str]],
    Literal["height"]: Optional[int],
    Literal["weight"]: dict[
        Literal["species"]: int,
        Literal["height"]: int,
        Literal["interests"]: int,
    ]
]


@dataclass(frozen=True)
class Info:
    name: str
    birthday: Birthday
    species: str
    height: int
    interests: set[str]
    preferences: Preferences

    @property
    def str_birthday(self):
        str_year = str(abs(self.birthday.year))
        if abs(self.birthday.year) < 10:
            str_year = "000" + str_year
        elif abs(self.birthday.year) < 100:
            str_year = "00" + str_year
        elif abs(self.birthday.year) < 1000:
            str_year = "0" + str_year
        if abs(self.birthday.year) < 0:
            str_year = '-' + str_year
        return f"{"0"+str(self.birthday.day) if abs(self.birthday.day) < 10 else self.birthday.day}/{"0"+str(self.birthday.month) if abs(self.birthday.month) < 10 else self.birthday.month}/{str_year}"


@dataclass(frozen=True)
class TaggedInfo(Info):
    id: int


class Model:
    def __init__(self):
        self._info_collection: dict[int, TaggedInfo] = {}
        self._last_id = 0
        self._unused_ids: set[int] = set()
    
    @property
    def data(self):
        return self._info_collection

    def get_entry_by_id(self, id: int):
        try:
            return self._info_collection[id]
        except:
            raise IndexError(f"No logged info exists for id: {id}.")

    def add_entry(self, entry: Info):
        print(entry)
        if self._unused_ids:
            unused_id = min(self._unused_ids)
            self._info_collection[unused_id] = (TaggedInfo(entry.name, entry.birthday, entry.species, entry.height, entry.interests, entry.preferences, unused_id))
            self._unused_ids.remove(unused_id)
        else:
            self._last_id += 1
            self._info_collection[self._last_id] = (TaggedInfo(entry.name, entry.birthday, entry.species, entry.height, entry.interests, entry.preferences, self._last_id))
    
    def remove_entry(self, id: int):
        try:
            popped_info = self._info_collection.pop(id)
            self._unused_ids.add(id)
            return popped_info
        except:
            raise IndexError(f"No logged info exists for id: {id}.")

    def compute_compatibility(self, id: int, candidate_id: int):
        if ((self.get_entry_by_id(id).species != self.get_entry_by_id(candidate_id).species)
            and (self.get_entry_by_id(id).species == "animalkin"
            or self.get_entry_by_id(candidate_id).species == "animalkin")):
            return '~'
        elif id and candidate_id:
            try:
                species_score = int(self.get_entry_by_id(candidate_id).species in self.get_entry_by_id(id).preferences["species"])
            except:
                species_score = 0
            try:
                height_score = self.get_entry_by_id(id).preferences["height"]//abs(self.get_entry_by_id(candidate_id).height - self.get_entry_by_id(id).preferences["height"]) if self.get_entry_by_id(id).preferences["height"] else 0
            except:
                height_score = 0
            try:
                interest_score = len(self.get_entry_by_id(candidate_id).interests | self.get_entry_by_id(id).interests)
            except:
                interest_score = 0
            return (
                (species_score*self.get_entry_by_id(id).preferences["weight"]["species"] + height_score*self.get_entry_by_id(id).preferences["weight"]["height"] + interest_score*self.get_entry_by_id(id).preferences["weight"]["interests"]) //
                (self.get_entry_by_id(id).preferences["weight"]["species"] + self.get_entry_by_id(id).preferences["weight"]["height"] + self.get_entry_by_id(id).preferences["weight"]["interests"])
            )


def capitalize(noun: str):
    assert(noun)
    return noun[0].upper() + noun[1:].lower()