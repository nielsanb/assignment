#Yakclass
class Yakbarn():
    def __init__(self, name="Nielsbarn", milk_stock=0, wool_stock=0, herd=[]):
        self.name = name.lower()
        self.milk_stock = milk_stock
        self.wool_stock = wool_stock
        self.herd = herd
        self.current_time = 0
        self.graveyard = []

    def __repr__(self):
        return f"This is a Yakbarn. Its name is {self.name}. It currently has {len(self.herd)} yaks, and a stock of {self.milk_stock} milk and {self.wool_stock} wool." 

    def next_day(self):
        self.current_time += 1
        self.check_dead_yaks()
        for i in self.herd:
            i.grow_a_day_older()
        for i in self.herd:
            self.milk_stock = self.milk_stock + i.produce_milk()
        for i in self.herd:
            self.wool_stock = self.wool_stock + i.try_to_shave()

    def add_yak(self, name, age_in_years=0):
        self.herd.append(Yak(name=name, age_in_years=age_in_years))

    def check_dead_yaks(self):
        #perhaps should use enumarate() and pop(index).
        dead_indices = []
        for i in self.herd:
            if i.age_in_years >= 10:
                dead_indices.append(self.herd.index(i))
        for j in sorted(dead_indices, reverse=True):
            self.graveyard.append(self.herd[j])
            del self.herd[j]

    def check_herd_for_wool(self):
        for i in self.herd:
            print(f"{i.name}: {i.time_since_shave}")

    def sell_wool(self, wool_sold=0):
        self.wool_stock = self.wool_stock - wool_sold

    def sell_milk(self, milk_sold=0):
        self.milk_stock = self.milk_stock - milk_sold

#Yaks 
class Yak():
    def __init__(self, name, age_in_years=0, time_since_shave=0):
        #still need to insert sex="f"
        self.name = name
        self.age_in_years = age_in_years
        self.age_in_days = age_in_years * 100
        self.time_since_shave = time_since_shave
        self.tribe = "LabYaks"

    def __repr__(self):
        return f"{self.name} of {self.age_in_years} years old"

    def grow_a_day_older(self):
        self.age_in_days += 1
        self.age_in_years = self.age_in_days / 100

    def another_day_no_wool(self):
        self.time_since_shave + 1

    def try_to_shave(self):
        if self.time_since_shave > (8 + (self.age_in_days * 0.01)) and self.age_in_days >= 100:
            wool_produced = 1
            self.time_since_shave = -1
        else:
            wool_produced = 0
            self.time_since_shave += 1
        return wool_produced

    def produce_milk(self):
        milk_produced = 50 - (self.age_in_days * 0.03)
        return milk_produced

class Yakwebshop():
    pass
