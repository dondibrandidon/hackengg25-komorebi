from tkinter import *
from tkinter import ttk
from model import DAYS_PER_MONTH, MONTHS_PER_YEAR, YEAR_LOWER, YEAR_UPPER, SPECIES_AGEFACTOR, Birthday, Info, Model, capitalize
from typing import Optional


model = Model()
model.add_entry(Info(
    name="Sayo, Brandon",
    birthday=Birthday(2, 7, 6),
    species="human",
    height=174,
    interests={"python","eat","sleep"},
    preferences={
        "species": {"human", "elven", "dwarf", "orc", "beastfolk", "demon", "dragonkin", "beltran"},
        "weight": {
            "species": 1,
            "interests": 2,
            "height": 3,
        }
    }
))
model.add_entry(Info(
    name="Mendoza, Martin",
    birthday=Birthday(13, 12, 4),
    species="human",
    height=170,
    interests={"python","eat","sleep", "coffee"},
    preferences={
        "species": {"human", "elven", "dwarf", "orc", "beastfolk", "demon", "dragonkin", "beltran"},
        "weight": {
            "species": 1,
            "interests": 2,
            "height": 3,
        }
    }
))

class App(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        self.title("Komorebi")
        self.geometry("677x530")
        self.resizable(False, False)

        main = Frame(self)
        main.pack(side="top", fill="both", expand=True)

        main.grid_rowconfigure(0, weight = 1)
        main.grid_columnconfigure(0, weight = 1)

        self.frames = {}

        self.frames[Database]= Database(main, self)
        self.frames[Database].grid(row=0, column=0, sticky='nsew')
        self.frames[Logger]= Logger(main, self)
        self.frames[Logger].grid(row=0, column=0, sticky='nsew')
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()
        if cont == Database:
            frame.load_table()

class Logger(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent, bg='#D9D9D9')
        
        title_label = Label(self, text="Welcome to Komorebi's Entry Logger!", background='#f2d466')
        title_label.grid(row=0, columnspan=4)
        
        Label(self).grid(row=1)
        
        fname_label = Label(self, text="First Name: ")
        fname_label.grid(row=2, column=0)
        lname_label = Label(self, text="Last Name: ")
        lname_label.grid(row=3, column=0)
        birthday_label = Label(self, text="Birthday: \n(dd/mm/yy)")
        birthday_label.grid(row=4, column=0, rowspan=2)
        species_label = Label(self, text="Species: ")
        species_label.grid(row=6, column=0)
        height_label = Label(self, text="Height: \n(cm)")
        height_label.grid(row=7, column=0)
        interests_label = Label(self, text="Interests: \n(entry, ...)")
        interests_label.grid(row=8, column=0)

        fname_entry = Entry(self)
        fname_entry.grid(row=2, column=1, columnspan=3, sticky='nsew')
        lname_entry = Entry(self)
        lname_entry.grid(row=3, column=1, columnspan=3, sticky='nsew')
        day_entry = Spinbox(self, from_=0, to=DAYS_PER_MONTH)
        month_entry = Spinbox(self, from_=0, to=MONTHS_PER_YEAR)
        year_entry = Spinbox(self, from_=YEAR_LOWER, to=YEAR_UPPER)
        day_entry.grid(row=4, column=1)
        month_entry.grid(row=4, column=2)
        year_entry.grid(row=4, column=3)
        species_combobox = ttk.Combobox(self, values=tuple(capitalize(specie) for specie in SPECIES_AGEFACTOR))
        species_combobox.grid(row=6, column=1, columnspan=3, sticky='nsew')
        height_entry = Entry(self)
        height_entry.grid(row=7, column=1, columnspan=3, sticky='nsew')
        interests_entry = Entry(self)
        interests_entry.grid(row=8, column=1, columnspan=3, sticky='nesw')

        Label(self).grid(row=9)

        preferences_label = Label(self, text="~ Preferences ~")
        preferences_label.grid(row=10, columnspan=4)

        species_label = Label(self, text="Species preferences: \n(entry, ...)")
        species_label.grid(row=11, column=0, rowspan=2)
        height_label = Label(self, text="Height preference: \n(cm)")
        height_label.grid(row=13, column=0, rowspan=2)
        weight_label = Label(self, text="What are you priorities? (with 1 as the highest and 3 as the lowest)")
        weight_label.grid(row=15, column=1, columnspan=3)
        species_weight_label = Label(self, text="Species")
        species_weight_label.grid(row=16, column=1)
        interests_weight_label = Label(self, text="Interests")
        interests_weight_label.grid(row=16, column=2)
        height_weight_label = Label(self, text="Height")
        height_weight_label.grid(row=16, column=3)

        species_preference_entry = Entry(self)
        species_preference_entry.grid(row=11, column=1, columnspan=3, sticky='nesw')
        height_preference_entry = Entry(self)
        height_preference_entry.grid(row=13, column=1, columnspan=3, sticky='nesw')
        species_weight_entry = Spinbox(self, from_=1, to=3, value=1)
        species_weight_entry.grid(row=17, column=1)
        interests_weight_entry = Spinbox(self, from_=1, to=3, value=2)
        interests_weight_entry.grid(row=17, column=2)
        height_weight_entry = Spinbox(self, from_=1, to=3, value=3)
        height_weight_entry.grid(row=17, column=3)

        Label(self).grid(row=18)

        create_button = Button(self, text="Create entry", command=lambda:
            self.update_model(
                fname_entry.get(),
                lname_entry.get(),
                day_entry.get(),
                month_entry.get(),
                year_entry.get(),
                species_combobox.get(),
                height_entry.get(),
                interests_entry.get(),
                species_preference_entry.get(),
                height_preference_entry.get(),
                species_weight_entry.get(),
                height_weight_entry.get(),
                interests_weight_entry.get(),
        ))
        create_button.grid(row=19, columnspan=4, sticky='nsew')

        self._warning_text = Label(self, text='')
        self._warning_text.grid(row=20, columnspan=4)
        Label(self).grid(row=21)

        database_button = Button(self, text="Go to database", command=lambda:controller.show_frame(Database))
        database_button.grid(row=22, columnspan=4)

    def _validate_info(self,
    fname: str,
    lname: str,
    day: str,
    month: str,
    year: str,
    species: str,
    height: str,
    interests: str,
    species_preference: str,
    height_preference: str,
    species_weight: str,
    height_weight: str,
    interests_weight: str,
    ):
        if species and species.lower() not in SPECIES_AGEFACTOR:
            raise ValueError("Error: Invalid species!")
        elif (int(day)+int(month)*DAYS_PER_MONTH+YEAR_UPPER-int(year)*MONTHS_PER_YEAR*DAYS_PER_MONTH)*SPECIES_AGEFACTOR[species.lower()]//SPECIES_AGEFACTOR["human"] < 18:
            raise ValueError("Error: Invalid age!")
        elif not year or not (YEAR_LOWER <= int(year) <= YEAR_UPPER):
            raise ValueError("Error: Invalid birth year!")
        elif not month or not (0 <= int(month) <= MONTHS_PER_YEAR):
            raise ValueError("Error: Invalid birth month!")
        elif not day or not (0 <= int(day) <= DAYS_PER_MONTH):
            raise ValueError("Error: Invalid birth day!")
        elif not (fname or lname):
            raise ValueError("Error: Invalid name!")
        elif not height or not int(height) >= 0:
            raise ValueError("Error: Invalid height!")
        elif (min({int(species_weight), int(height_weight), int(interests_weight)}) <= 0
        or max({int(species_weight), int(height_weight), int(interests_weight)}) > 3
        or len({int(species_weight), int(height_weight), int(interests_weight)}) != 3):
            raise ValueError("Error: Invalid weighted preferences!")
        else:
            return Info(
                name=f"{lname + ', ' + fname if lname and fname else lname + fname}",
                birthday=Birthday(
                    day=int(day),
                    month=int(month),
                    year=int(year),
                ),
                species=species.lower(),
                height=int(height),
                interests=set(interest.strip() for interest in interests.split(',')),
                preferences={
                    "species": set(specie.strip() for specie in species_preference.split(',')),
                    "height": int(height_preference) if height_preference else None,
                    "weight": {
                        "species": int(species_weight),
                        "height": int(height_weight),
                        "interests": int(interests_weight),
                    },
                },
            )

    def update_model(self,
    fname: str,
    lname: str,
    day: str,
    month: str,
    year: str,
    species: str,
    height: str,
    interests: str,
    species_preference: str,
    height_preference: str,
    species_weight: str,
    height_weight: str,
    interests_weight: str,
    ):
        try:
            model.add_entry(self._validate_info(fname, lname, day, month, year, species, height, interests,
            species_preference, height_preference, species_weight, height_weight, interests_weight))
            self._warning_text['text'] = 'Entry successfully created!'
        except Exception as e:
            self._warning_text['text'] = str(e)
            if str(e) == '':
                self._warning_text['text'] = "Error: Invalid input!"


class Database(Frame):
    def __init__(self, parent, controller):
        self._controller = controller

        Frame.__init__(self, parent, bg='#D9D9D9')
        
        title_label = Label(self, text="Welcome to Komorebi's Database!", background='#f2d466')
        title_label.pack()
        # title_label.grid(row=0, columnspan=7, sticky='nsew')
        
        Label(self).pack()
        #Label(self).grid(row=1)

        self._table_frame = Frame(self)
        self.load_table()
        
        #database_button.grid(row=5+self._last_id, columnspan=7)

    def load_table(self, selected_id: Optional[int]=None):
        self._table_frame.destroy()
        self._table_frame = Frame(self)

        id_header = Label(self._table_frame, text="ID#")
        id_header.grid(row=2, column=0, padx=20)
        name_header = Label(self._table_frame, text="Name")
        name_header.grid(row=2, column=1, padx=30)
        birthday_header = Label(self._table_frame, text="Birthday")
        birthday_header.grid(row=2, column=2, padx=20)
        species_header = Label(self._table_frame, text="Species")
        species_header.grid(row=2, column=3, padx=20)
        height_header = Label(self._table_frame, text="Height (cm)")
        height_header.grid(row=2, column=4, padx=10)
        # interests_header = Label(self._table_frame, text="Interests")
        # interests_header.grid(row=2, column=5)
        # match_header = Label(self._table_frame, text="Match?")
        # match_header.grid(row=2, column=5)
        score_header = Label(self._table_frame, text="Score")
        score_header.grid(row=2, column=5, padx=20)

        for id in model.data:
            info = model.get_entry_by_id(id)

            id_data = Label(self._table_frame, text=id)
            id_data.grid(row=2+id, column=0)
            name_data = Label(self._table_frame, text=info.name)
            name_data.grid(row=2+id, column=1)
            birthday_data = Label(self._table_frame, text=info.str_birthday)
            birthday_data.grid(row=2+id, column=2)
            species_data = Label(self._table_frame, text=capitalize(info.species))
            species_data.grid(row=2+id, column=3)
            height_data = Label(self._table_frame, text=info.height)
            height_data.grid(row=2+id, column=4)
            # interests_data = ttk.Combobox(self._table_frame, values=tuple(str(deet) for deet in info.interests))
            # interests_data.grid(row=2+id, column=5)
            # match_check = Checkbutton(self._table_frame, variable=match_checked)
            # print(match_checked.get())
            # if match_check.get():
            #     break
            # match_check.grid(row=2+id, column=5)
            # if self._selected_id and self._selected_id != id:
            #     match_check.config(state=DISABLED)
            # else:
            #     match_check.config(state=NORMAL)
            score_header = Label(self._table_frame, text=f"{model.compute_compatibility(selected_id, id) if selected_id and selected_id != id else '~'}")
            score_header.grid(row=2+id, column=5)

        
        #self._table_frame.grid(row=3, columnspan=7)

        Label(self._table_frame).grid(row=3+id)
        id_label = Label(self._table_frame, text="Matchmake? (ID#)")
        id_label.grid(row=4+id, column=2, columnspan=2)
        id_entry = Entry(self._table_frame)
        id_entry.grid(row=5+id, column=2, columnspan=2)
        id_button = Button(self._table_frame, text='✓', command=lambda:self.load_table(int(id_entry.get())))
        id_button.grid(row=5+id, column=4)

        Label(self._table_frame).grid(row=6+id)
        Label(self._table_frame).grid(row=7+id)
        #Label(self).grid(row=4+self._last_id)

        database_button = Button(self._table_frame, text="Go to entry logger", command=lambda:self._controller.show_frame(Logger))
        database_button.grid(row=8+id, columnspan=7)

        self._table_frame.pack()
    


def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()