import pygame
import time
import pygame.midi

# jakby nie działało zakomentować dwie linijki niżej, wyłączy funkcję grania akordów.
pygame.midi.init() # tą linijkę należy zakomentować jakby nie działało
player = pygame.midi.Output(0) # tą też

tuning_table = ["", "poniżej A0","poniżej A0","poniżej A0","poniżej A0","poniżej A0","poniżej A0","poniżej A0","poniżej A0","poniżej A0","poniżej A0",
                "poniżej A0","poniżej A0","poniżej A0","poniżej A0","poniżej A0","poniżej A0","poniżej A0","poniżej A0","poniżej A0","poniżej A0",
                "A0", "A#0", "B0", "C1", "C#1", "D1", "D#1", "E1", "F1", "F#1", "G1", "G#1",
                "A1", "A#1", "B1", "C2", "C#2", "D2", "D#2", "E2", "F2", "F#2", "G2", "G#2",
                "A2", "A#2", "B2", "C3", "C#3", "D3", "D#3", "E3", "F3", "F#3", "G3", "G#3",
                "A3", "A#3", "B3", "C4", "C#4", "D4", "D#4", "E4", "F4", "F#4", "G4", "G#4",
                "A4", "A#4", "B4", "C5", "C#5", "D5", "D#5", "E5", "F5", "F#5", "G5", "G#5",
                "A5", "A#5", "B5", "C6", "C#6", "D6", "D#6", "E6", "F6", "F#6", "G6", "G#6",
                "A6", "A#6", "B6", "C7", "C#7", "D7", "D#7", "E7", "F7", "F#7", "G7", "G#7",
                "A7", "A#7", "B7", "C8", "C#8", "D8", "D#8", "E8", "F8", "F#8", "G8", "G#8",
                "A8", "A#8", "B8", "C9", "C#9", "D9", "D#9", "E9", "F9", "F#9", "G9", "G#9"]
beat = "";

class Gitara:
    # number of strings - liczba strun
    # guitar_type - typ gitary, gdzie:
    # "classical" - klasyczna
    # "acoustic" - akustyczna
    # "electric" - elektryczna
    # "overdrive" - elektryczna z przesterem
    # tuning - strojenie dla wszystkich strun, nuty strojenia podane w formacie kodów MIDI im odpowiadających
    def __init__(self, number_of_strings=6, guitar_type="classical", tuning=[64, 59, 55, 50, 45, 40]):
        self.number_of_strings = number_of_strings
        self.guitar_type = guitar_type
        self.tuning = tuning
        self.fret_pressed = []
        self.time_between_notes = 0.04
        self.last_note_time = 0.12
        self.beat_program = []
        self.chord_program = []
        for x in range(self.number_of_strings):
            self.fret_pressed.append(0)

    def wypisz_info(self):
        print ("\nTyp gitary: "+self.guitar_type)
        print ("Ilość strun: "+str(self.number_of_strings))

    def zmien_typ(self):
        print ("\nZmieniasz typ gitary. ")
        self.guitar_type = input ("Podaj typ - classical, acoustic, electric, overdrive: ");

    def wypisz_czas(self):
        print ("\nMiędzy strunami: "+str(self.time_between_notes))
        print ("Po ostatniej strunie: "+str(self.last_note_time))

    def zmien_czas(self):
        print ("\nZmieniasz czas między strunami. ")
        self.time_between_notes = float(input("Podaj czas między strunami: "));
        self.last_note_time = float(input("Podaj czas po ostatniej strunie: "));

    def zmien_ilosc_strun(self):
        print ("\nZmieniasz ilość strun gitary. ")
        self.guitar_type = int(input ("Podaj ilość strun: "));

    def wypisz_strojenie(self):
        print ("\nStrojenie: ")
        for x in range(self.number_of_strings):
            print (tuning_table[self.tuning[x]])

    def wypisz_akord(self):
        print ("\nObecnie grany akord: ")
        for x in range(self.number_of_strings):
            print (tuning_table[self.tuning[x]+self.fret_pressed[x]])

    def zmien_strojenie(self):
        print ("\nZmieniasz strojenie gitary. ")
        for x in range(self.number_of_strings):
            print ("Struna "+str(x+1)+" jest nastrojona na nutę "+tuning_table[self.tuning[x]]+". ")
            self.tuning[x] = int(input ("Zmień strojenie struny "+str(x+1)+" (podaj kod MIDI): "));

    def zmien_akord(self):
        print ("\nZmieniasz grany akord. ")
        for x in range(self.number_of_strings):
            print ("Struna "+str(x+1)+" jest naciśnięta na "+str(self.fret_pressed[x])+" progu. ")
            self.fret_pressed[x] = int(input ("Zmień miejsce dociśnięcia struny "+str(x+1)+": "));

    def graj_akord(self, kierunek=0):
        # ustaw instrument MIDI w zależności od typu gitary.
        if self.guitar_type == "classical":
            player.set_instrument(25,1)
        if self.guitar_type == "acoustic":
            player.set_instrument(26,1)
        if self.guitar_type == "electric":
            player.set_instrument(28,1)
        if self.guitar_type == "overdrive":
            player.set_instrument(30,1)
            
        if (kierunek == 0):
            for x in range(self.number_of_strings):
                # graj nuty idąc od góry. Ostatnia struna dłużej
                player.note_on(self.tuning[x]+self.fret_pressed[x], 127,1)
                if (x == self.number_of_strings-1):
                    time.sleep(self.last_note_time)
                time.sleep(self.time_between_notes)
                player.note_off(self.tuning[x]+self.fret_pressed[x], 127,1)
        if (kierunek == 1):
            for x in reversed(range(self.number_of_strings)):
                # graj nuty idąc od dołu. Ostatnia struna dłużej
                player.note_on(self.tuning[x]+self.fret_pressed[x], 127,1)
                if (x == 0):
                    time.sleep(self.last_note_time)
                time.sleep(self.time_between_notes)
                player.note_off(self.tuning[x]+self.fret_pressed[x], 127,1)
        if (kierunek == 2):
            for x in reversed(range(self.number_of_strings)):
                # brak bicia - graj puste nuty o zerowej głośności.
                player.note_on(0, 0,1)
                if (x == 0):
                    time.sleep(self.last_note_time)
                time.sleep(self.time_between_notes)
                player.note_off(0, 0,1)

    def programuj_bicie(self):
        program_end = 0;
        position = 1;
        self.beat_program.clear()
        print ("\nObecnie programujesz nowe bicie.")
        while (program_end == 0):
            beat = input("Podaj kierunek bicia na pozycji "+str(position)+". (U - góra, D - dół, K - koniec, kreska / minus / spacja / brak inputu - brak bicia): ")
            if (beat == "U" or beat == "u"):
                self.beat_program.append(1)
                position += 1
            if (beat == "D" or beat == "d"):
                self.beat_program.append(0)
                position += 1
            if (beat == "-" or beat == " " or beat == ""):
                self.beat_program.append(2)
                position += 1
            if (beat == "K" or beat == "k"):
                program_end = 1;

    def programuj_akordy(self):
        program_end = 0;
        position = 1;
        self.chord_program.clear()
        print ("\nObecnie programujesz nowy zestaw akordów.")
        while (program_end == 0):
            chord = input("Podaj opcję na pozycji "+str(position)+". (1 - nowy akord, 2 - poprzedni akord, K - koniec): ")
            if (chord == "1"):
                self.zmien_akord()
                self.wypisz_akord()
                self.graj_akord(1)
                self.chord_program.append(str(self.fret_pressed))
                position += 1
            if (chord == "2"):
                self.chord_program.append(str(self.fret_pressed))
                position += 1
            if (chord == "K" or chord == "k"):
                program_end = 1;

    def pokaz_bicie(self):
        chord_string = ""
        for x in range(len(self.beat_program)):
            if (self.beat_program[x] == 0):
                chord_string += "⬇"
            if (self.beat_program[x] == 1):
                chord_string += "⬆"
            if (self.beat_program[x] == 2):
                chord_string += "-"
        print("\nZaprogramowane obecnie bicie to:")
        print(chord_string)
                    
    def pokaz_akordy(self):
        print("\nZaprogramowane obecnie akordy to:")
        for x in range(len(self.chord_program)):
            print(self.chord_program[x])

    def graj_piosenke(self):
        for x in range(len(self.chord_program)):
            self.fret_pressed = self.chord_program[x][1:-1].split(", ")
            for z in range(self.number_of_strings):
                self.fret_pressed[z] = int(self.fret_pressed[z])
            for y in range(len(self.beat_program)):
                self.graj_akord(self.beat_program[y])

def menu():
    program_end = 0;
    position = 1;
    print ("\nGuitar Simulator by KitsuneFox")
    while (program_end == 0):
        print ("\nWybierz opcję.")
        print ("1. Wypisz info o gitarze")
        print ("2. Zmień typ gitary")
        print ("3. Zmień ilość strun w gitarze")
        print ("4. Pokaż strojenie gitary")
        print ("5. Zmień strojenie gitary")
        print ("6. Pokaż grany akord")
        print ("7. Zmień grany akord")
        print ("8. Zmień bicie")
        print ("9. Zmień akordy")
        print ("10. Pokaż czas między strunami")
        print ("11. Zmień czas między strunami")
        print ("12. Graj piosenkę")
        print ("K. Zakończ")
        menusel = input("Wybierz opcję: ")
        if (menusel == "1"):
            gitara.wypisz_info()
        if (menusel == "2"):
            gitara.zmien_typ()
        if (menusel == "3"):
            gitara.zmien_ilosc_strun()
        if (menusel == "4"):
            gitara.wypisz_strojenie()
        if (menusel == "5"):
            gitara.zmien_strojenie()
        if (menusel == "6"):
            gitara.wypisz_akord()
            gitara.graj_akord(1)
        if (menusel == "7"):
            gitara.zmien_akord()
        if (menusel == "8"):
            gitara.programuj_bicie()
            gitara.pokaz_bicie()
        if (menusel == "9"):
            gitara.programuj_akordy()
            gitara.pokaz_akordy()
        if (menusel == "10"):
            gitara.wypisz_czas()
        if (menusel == "11"):
            gitara.zmien_czas()
        if (menusel == "12"):
            gitara.pokaz_bicie()
            gitara.pokaz_akordy()
            gitara.graj_piosenke()
        if (menusel == "K" or menusel == "k"):
            program_end = 1;
    print ("Dziękuję za używanie")

    
gitara = Gitara()
menu()
