import copy
import csv
import json
import math
import random
import os
from Spacecraft_Classes import Spacecraft

# github link to retrieve CargoList1.csv if necessary
github_link = ("https://github.com/stevenuva/minor-programmeren/blob/"
               "master/CargoList1.csv")

# path to the csv_file
csv_file = "./data/CargoList1.csv"

# check if user has csv at the right path
for path in [csv_file]:
    assert os.path.exists(path), (f"{path} does not exist. Please download file"
                                  f" from {github_link}")

# load csv file into a list
with open(csv_file, "r") as infile:
    reader = csv.reader(infile)
    csv_list = list(reader)

# create an empty list
cargo1_list = []

for row in csv_list[1:]:
    cargo1_dic = {"id": row[0], "mass": float(row[1]), "volume": float(row[2])}
    cargo1_dic["kg/m3"] = cargo1_dic["mass"] / cargo1_dic["volume"]
    cargo1_list.append(cargo1_dic)

# sort list on volume
cargo1_list = sorted(cargo1_list, key=lambda
                     parcel: parcel["volume"])

# slice list
leftover_list = cargo1_list[83:]
initial_list = cargo1_list[:83]

# sort list on kg/m3 ratio
initial_list = sorted(initial_list, key=lambda
                      parcel: parcel["kg/m3"])

# define properties of the spacecrafts
Cygnus = Spacecraft(2000, 18.9, 7400, 390000000, 0.73)
Progress = Spacecraft(2400, 7.6, 7020, 175000000, 0.74)
Kounotori = Spacecraft(5200, 14, 10500, 420000000, 0.71)
Dragon = Spacecraft(6000, 10, 12200, 347000000, 0.72)
TianZhou = Spacecraft(6500, 15, 13500, 412000000, 0.75)
Verne_ATV = Spacecraft(7500, 48, 20500, 1080000000, 0.72)

# create a list containing all the spaceships
spacecrafts = [Cygnus, Dragon, Kounotori, Progress]

# sort list on kg/m3 ratio
spacecrafts = sorted(spacecrafts, key=lambda
                     spacecraft: spacecraft.ratio)

remaining_list = []
starting_len = 0
temporary_len = 0
total_len = 0

# experiment: start hill climber with some cargo already pre-loaded
for parcel in initial_list:
    if parcel["kg/m3"] < (spacecrafts[0].ratio + 75):
        spacecrafts[0].add_cargo(parcel["id"], parcel["mass"], parcel["volume"])
    elif (spacecrafts[1].ratio - 15 < parcel["kg/m3"]) and (parcel["kg/m3"] < spacecrafts[1].ratio + 15):
        spacecrafts[1].add_cargo(parcel["id"], parcel["mass"], parcel["volume"])
    elif ((spacecrafts[2].ratio - 19) < parcel["kg/m3"]) and (parcel["kg/m3"] < (spacecrafts[2].ratio + 19)):
        spacecrafts[2].add_cargo(parcel["id"], parcel["mass"], parcel["volume"])
    elif ((spacecrafts[3].ratio - 100) < parcel["kg/m3"]):
        spacecrafts[3].add_cargo(parcel["id"], parcel["mass"], parcel["volume"])
    else:
        remaining_list.append(parcel)

# organize data with list
# make copy of list also for the hill climber
original_spacecrafts = spacecrafts
total_remaining_list = remaining_list + leftover_list
spacecrafts.append(total_remaining_list)
complete_list = spacecrafts[:]
previous_len = 0
number_found = 0
previous_cost = 0

""""
HILLCLIMBER
"""
total_len = 0

while total_len < 90:

    #  boolean which can turn true if the hill climber wants it to
    accept = False
    cheaper = False
    longer = False

    # copy all list incase hill climber wants to go back
    alt_Cygnus = copy.deepcopy(Cygnus.cargo_list)
    alt_Dragon = copy.deepcopy(Dragon.cargo_list)
    alt_Kounotori = copy.deepcopy(Kounotori.cargo_list)
    alt_Progress = copy.deepcopy(Progress.cargo_list)

    # choose random object
    random_object = random.choice(complete_list)
    random_object2 = random.choice(complete_list)

    # check if random object is not selected twice
    if random_object != random_object2:

        # if random object is a list, it is the list containing the remaining parcels
        # loop to load these remaining parcels into a random spacecraft
        if type(random_object) == list:

            # if random spacecraft is Cygnus, hill climber will look at remaining volume
            if random_object2 == Cygnus:

                # select random package from the list
                parcel1 = random.choice(random_object)

                # add package to the spacecraft is possible and change boolean to True to accept the change
                if (parcel1["mass"] < random_object2.remaining_mass) and (parcel1["volume"] < random_object2.remaining_volume):
                    random_object2.add_cargo(parcel1["id"], parcel1["mass"], parcel1["volume"])
                    accept = True
                    random_object.remove(parcel1)

                # swap unloaded parcel with a loaded parcel if possible
                else:
                    parcel2 = random.choice(random_object2.cargo_list)
                    random_object2.remove_cargo(parcel2["id"])

                    # if situation acceptable, accept the new situation
                    if (parcel1["mass"] < random_object2.remaining_mass) and (parcel1["volume"] < random_object2.remaining_volume):
                        random_object2.add_cargo(parcel1["id"], parcel1["mass"], parcel1["volume"])
                        if random_object2.remaining_volume > 0:
                            accept = True
                            random_object.append(parcel2)
                            random_object.remove(parcel1)

                    # else return package
                    else:
                        random_object2.add_cargo(parcel2["id"], parcel2["mass"], parcel2["volume"])

            # if random spacecraft is not Cygnus, hill climber will look at remaining mass
            else:

                # select random package from the list
                parcel1 = random.choice(random_object)

                # add package to the spacecraft is possible and change boolean to True to accept the change
                if (parcel1["mass"] < random_object2.remaining_mass) and (parcel1["volume"] < random_object2.remaining_volume):
                    random_object2.add_cargo(parcel1["id"], parcel1["mass"], parcel1["volume"])
                    accept = True
                    random_object.remove(parcel1)

                # swap unloaded parcel with a loaded parcel if possible
                else:
                    parcel2 = random.choice(random_object2.cargo_list)
                    random_object2.remove_cargo(parcel2["id"])

                    if (parcel1["mass"] < random_object2.remaining_mass) and (parcel1["volume"] < random_object2.remaining_volume):
                        random_object2.add_cargo(parcel1["id"], parcel1["mass"], parcel1["volume"])
                        if random_object2.remaining_mass > 0:
                            accept = True
                            random_object.remove(parcel1)
                            random_object.append(parcel2)

                    else:
                        random_object2.add_cargo(parcel2["id"], parcel2["mass"], parcel2["volume"])

        elif type(random_object2) == list:
            if random_object == Cygnus:
                parcel2 = random.choice(random_object2)

                if (parcel2["mass"] < random_object.remaining_mass) and (parcel2["volume"] < random_object.remaining_volume):
                    random_object.add_cargo(parcel2["id"], parcel2["mass"], parcel2["volume"])
                    accept = True
                    random_object2.remove(parcel2)

                else:
                    parcel1 = random.choice(random_object.cargo_list)
                    random_object.remove_cargo(parcel1["id"])

                    if (parcel2["mass"] < random_object.remaining_mass) and (parcel2["volume"] < random_object.remaining_volume):
                        random_object.add_cargo(parcel2["id"], parcel2["mass"], parcel2["volume"])
                        if random_object.remaining_mass > 0:
                            accept = True
                            random_object2.append(parcel1)
                            random_object2.remove(parcel2)

                    else:
                        random_object.add_cargo(parcel1["id"], parcel1["mass"], parcel1["volume"])
            else:
                parcel2 = random.choice(random_object2)

                if (parcel2["mass"] < random_object.remaining_mass) and (parcel2["volume"] < random_object.remaining_volume):
                    random_object.add_cargo(parcel2["id"], parcel2["mass"], parcel2["volume"])
                    accept = True
                    random_object2.remove(parcel2)

                else:
                    parcel1 = random.choice(random_object.cargo_list)
                    random_object.remove_cargo(parcel1["id"])

                    if (parcel2["mass"] < random_object.remaining_mass) and (parcel2["volume"] < random_object.remaining_volume):
                        random_object.add_cargo(parcel2["id"], parcel2["mass"], parcel2["volume"])
                        if random_object.remaining_volume > 0:
                            accept = True
                            random_object2.append(parcel1)
                            random_object2.remove(parcel2)

                    else:
                        random_object.add_cargo(parcel1["id"], parcel1["mass"], parcel1["volume"])

        else:
            parcel1 = random.choice(random_object.cargo_list)
            parcel2 = random.choice(random_object2.cargo_list)

            if (parcel2["mass"] < random_object.remaining_mass) and (parcel2["volume"] < random_object.remaining_volume):
                random_object.add_cargo(parcel2["id"], parcel2["mass"], parcel2["volume"])
                random_object2.remove_cargo(parcel2["id"])
                if random_object.remaining_volume > 0:
                    accept = True
                else:
                    accept = False

            if (parcel1["mass"] < random_object2.remaining_mass) and (parcel1["volume"] < random_object2.remaining_volume):
                random_object2.add_cargo(parcel1["id"], parcel1["mass"], parcel1["volume"])
                random_object.remove_cargo(parcel1["id"])
                if random_object2.remaining_volume > 0:
                    accept = True
                else:
                    accept = False

    # double-check total length cargo float and remaining weight and volume
    total_len = 0
    list_of_cargo_dict = []
    total_cost = 0
    for thespacecraft in original_spacecrafts:
        if type(thespacecraft) == list:
            continue
        # print(thespacecraft.remaining_volume)
        total_cost += thespacecraft.cost()
        total_len += len(thespacecraft.cargo_list)
        if (thespacecraft.remaining_volume < 0):
            accept = False
        if (thespacecraft.remaining_mass < 0):
            accept = False
        if thespacecraft.filled_volume > thespacecraft.volume:
            accept = False
        list_of_cargo_dict.append(thespacecraft.cargo_list)

    # if new situation is better accept new situation
    if accept == True and (total_len >= previous_len or total_cost < previous_cost):
        previous_len = total_len
        previous_cost = total_cost
        cheaper = True
        if type(random_object) != list:
            random_object.cargo_list = random_object.cargo_list
        if type(random_object2) != list:
            random_object2.cargo_list = random_object2.cargo_list
    else:
        accept == False

    # if new situation is not better return to old situation
    if (accept == False) or (total_len < previous_len):
        Cygnus.cargo_list = alt_Cygnus
        Dragon.cargo_list = alt_Dragon
        Kounotori.cargo_list = alt_Kounotori
        Progress.cargo_list = alt_Progress

    print("Length filled + unfilled: ", len(Cygnus.cargo_list) + len(Dragon.cargo_list) + len(Kounotori.cargo_list) + len(Progress.cargo_list) + len(total_remaining_list))
    print("Parecels filled: ", total_len)
    print("Parecels cost: ", total_cost)

    # send result to a textfile
    if (total_len > 82) and (accept == True) and (cheaper == True):
        with open("outputfile (" + str(number_found) + "x) (" + str(total_len) + ").txt", 'w') as output:
            number_found += 1
            json.dump(list_of_cargo_dict, output)

    # check if hill climber accepts the change
    print(accept)
    print("---------------------------")