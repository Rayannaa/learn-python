# import module
import math

# set global constants
CONVERT_UNIT = 3.28
ROCKET_DENSITY = 1.225
MASS_LIMIT_LOW = 80000
MASS_LIMIT_HIGH = 350000
BURN_SPEED_LOW = 768
BURN_SPEED_MED = 1314
BURN_SPEED_HIGH = 1542
COST_MATERIAL = 4.5
COST_FUEL = 7.331
TAX_RATIO = 0.14975
WEIGHT_RATIO = 0.04
VOLUME_RATIO = 0.6
WEIGHT_BOUND_LOW = 10
WEIGHT_BOUND_HIGH = 512
VOLUME_BOUND = 0.5
HEIGHT_INITIAL = 0.0
A_GRAVITY = 9.81
HEIGHT_MIN = 0

# intermediate functions
def feet_to_meter(length):
    """ (float) -> (float)
    Convert from feet to meters and round to 2 decimals
    
    >>> feet_to_meter(5.0)
    1.52
    >>> feet_to_meter(12345)
    3763.72
    >>> feet_to_meter(201.21)
    61.34    
    """
    length = round(length / CONVERT_UNIT, 2)
    return length


def rocket_volume(radius, height_cone, height_cyl):
    """ (float, float, float) -> (float)
    calculate the volume of a rocket
    
    >>> rocket_volume(2.0, 7.0, 3.0)
    67.02
    >>> rocket_volume(10.39, 47.1, 2.7)
    6240.2
    >>> rocket_volume(1022.394, 283.131, 488.712)
    1914790682.32
    """
    volume_cone = math.pi * radius ** 2 * height_cone / 3
    volume_cyl = math.pi * radius ** 2 * height_cyl
    volume = round(volume_cone + volume_cyl, 2)
    return volume


def rocket_area(radius, height_cone, height_cyl):
    """ (float, float, float) -> (float)
    calculate the surface area of a rocket
    
    >>> rocket_area(2.0, 7.0, 3.0)
    96.01
    >>> rocket_area(10.39, 47.1, 2.7)
    2089.76
    >>> rocket_area(1022.394, 283.131, 488.712)
    9830774.34
    """
    area_cone = math.pi * radius * \
                (radius + math.sqrt(height_cone ** 2 + radius ** 2))
    area_cyl = 2 * math.pi * radius * (height_cyl + radius)
    area_circle = math.pi * radius ** 2
    area = round(area_cone + area_cyl - 2 * area_circle, 2)
    return area


def rocket_mass(radius, height_cone, height_cyl):
    """ (float, float, float) -> (float)
    calculate the mass of the rocket
    
    >>> rocket_mass(2.0, 7.0, 3.0)
    82.1
    >>> rocket_mass(10.39, 47.1, 2.7)
    7644.24
    >>> rocket_mass(1022.394, 283.131, 488.712)
    2345618585.84
    """
    volume = rocket_volume(radius, height_cone, height_cyl)
    mass = round(volume * ROCKET_DENSITY, 2)
    return mass


def rocket_fuel(radius, height_cone, height_cyl, \
                velocity_e, velocity_i, time):
    """(float, float, float, float, float, float) -> (float)
    calculate the amount of fuel the rocket needs
    
    >>> rocket_fuel(2.0, 3.0, 4.0, 250.0, 1000.0, 1.0)
    4893.45
    >>> rocket_fuel(10.39, 47.1, 2.7, 460.0, 700.0, 3.0)
    29671.78
    >>> rocket_fuel(1022.394, 283.131, 488.712, 80.0, 1200.0, 10)
    7667865560701253.0
    """
    # calculate the fuel used to exit a planet’s atmosphere
    mass = rocket_mass(radius, height_cone, height_cyl)
    fuel_exit = mass * (math.e ** (velocity_i / velocity_e) - 1)
    # calculate the fuel needed for the rest of the trip
    if mass < MASS_LIMIT_LOW:
        burn_speed = BURN_SPEED_LOW
    elif mass < MASS_LIMIT_HIGH:
        burn_speed = BURN_SPEED_MED
    else:
        burn_speed = BURN_SPEED_HIGH
    fuel_rest = time * burn_speed
    # calculate the total fuel
    fuel = round(fuel_exit + fuel_rest, 2)
    return fuel


def calculate_cost(radius, height_cone, height_cyl, \
                   velocity_e, velocity_i, time, tax):
    """(float, float, float, float, float, float, boolean) -> (float)
    calculates the approximate cost of building and launching this rocket
    
    >>> calculate cost(2.0, 3.0, 4.0, 250.0, 1000.0, 1.0, True)
    41688.31
    >>> calculate cost(22.7, 52.2, 68.1, 323.3, 1029.9, 0.8, False)
    28891245.55
    >>> calculate cost(233.1, 211.2, 33.0, 2322.0, 9888.9, 1.6, True)
    12709263675.7
    """
    # calculate the cost of materials
    area = rocket_area(radius, height_cone, height_cyl)
    cost_material = area * COST_MATERIAL
    # calculate the cost of fuels
    fuel = rocket_fuel(radius, height_cone, height_cyl, \
                       velocity_e, velocity_i, time)
    cost_fuel = fuel * COST_FUEL
    # calculate the taxes
    if tax:
        cost_tax = TAX_RATIO * (cost_material + cost_fuel)
    else:
        cost_tax = 0
    # calculate the total cost
    cost = round(cost_material + cost_fuel + cost_tax, 2)
    return cost


def compute_storage_space(radius, height_cyl):
    """ (float, float) -> (float, float, float)
    calculate the dimensions of the rectangular storage box
    in the rocket cylinder
    
    >>> compute_storage_space(5.0, 10.0)
    (7.07, 7.07, 5.0)
    >>> compute_storage_space(82.4, 21.7)
    (116.53, 116.53, 10.85)
    >>> compute_storage_space(1293.6, 2034.3)
    (1829.43, 1829.43, 1017.15)
    """
    storage_width = round(2 ** (1 / 2) * radius, 2)
    storage_length = storage_width
    storage_height = round(height_cyl / 2, 2)
    return storage_width, storage_length, storage_height


def load_rocket(initial_weight, radius, height_cyl):
    """ (float, float, float) -> (float)
    simulate loading items and return the new weight
    
    >>> load_rocket(249.0, 100.0, 100.0)
    No more items can be added
    249.0
    >>> load_rocket(10302.0, 3120.0, 1102.0)
    Please enter the weight of the next item (type "Done" when you \
    are done filling the rocket): 999
    Enter item width: 3
    Enter item length: 4
    Enter item height: 5
    Item could not be added... please try again...
    Please enter the weight of the next item (type "Done" when you \
    are done filling the rocket): 333
    Enter item width: 3
    Enter item length: 3
    Enter item height: 3
    Please enter the weight of the next item (type "Done" when you \
    are done filling the rocket): Done
    10635.0
    >>>load_rocket(298.62, 333.88, 111.12)
    Please enter the weight of the next item (type "Done" when you \
    are done filling the rocket): 10
    Enter item width: 2
    Enter item length: 1
    Enter item height: 2
    No more items can be added
    308.62
    """
    # calculate the storage space and the limits of weight and volume
    storage_width, storage_length, storage_height \
                   = compute_storage_space(radius, height_cyl)
    storage = storage_width * storage_length * storage_height
    max_weight = WEIGHT_RATIO * initial_weight
    max_volume = VOLUME_RATIO * storage
    rocket_weight = initial_weight
    # verify if allowing at least one small box
    if WEIGHT_BOUND_LOW > max_weight or VOLUME_BOUND > max_volume:
        print("No more items can be added")
        return round(rocket_weight, 2)
    else:
        # broad items
        item_weight = 0
        item_volume = 0
        while item_weight <= max_weight and item_volume <= max_volume:
            # verify if allowing at least one small box
            if max_weight - item_weight < WEIGHT_BOUND_LOW or \
               max_volume - item_volume < VOLUME_BOUND:
                print("No more items can be added")
                return round(rocket_weight, 2)
            # get inputs of items
            new_weight = input("Please enter the weight of the next item \
(type \"Done\" when you are done filling the rocket): ")
            # check continue or not
            if new_weight == "Done":
                return round(rocket_weight, 2)
            else:
                new_weight = float(new_weight)
            new_width = float(input("Enter item width: "))
            new_length = float(input("Enter item length: "))
            new_height = float(input("Enter item height: "))
            new_volume = new_width * new_length * new_height
            # check if adding item satisfy weight and volume requirement
            if new_weight < WEIGHT_BOUND_LOW \
               or new_weight > WEIGHT_BOUND_HIGH \
               or item_weight + new_weight > max_weight \
               or new_volume < VOLUME_BOUND \
               or item_volume + new_volume > max_volume:
                print("Item could not be added... please try again...")
            else:
                # renew the weight & volume
                item_weight += new_weight
                item_volume += new_volume
                rocket_weight += new_weight         
        print("No more item can be added")
        return round(rocket_weight, 2)


def projectile_sim(simulation_time, interval, v0, angle):
    """ (int, int, float, float) -> ()
    print the rocket height of each sample point
    
    >>>projectile sim(10, 2, 100.0, 0.79)
    0.0
    122.45
    205.66
    249.63
    254.36
    219.85
    >>>projectile sim(400, 72, 6722.0, 0.31)
    0.0
    122215.98
    193576.92
    214082.82
    183733.68
    102529.5
    >>>projectile sim(80, 6, 173.0, 0.5)
    0.0
    321.06
    288.97
    """
    height = HEIGHT_INITIAL
    print(height)
    total_data_point = simulation_time // interval
    # print the height for every valid sample point
    for data_point in range(1, total_data_point + 1):
        time = data_point * interval
        height = (-1/2) * A_GRAVITY * (time ** 2) + \
                 v0 * math.sin(angle) * time
        if height > 0:
            print(round(height, 2))


def rocket_main():
    """() -> ()
    Ask the user for information, then calculate the cost,
    load the rocket, and simulate the trip
    
    >>>rocket_main()
    Welcome to the Rocket Simulation!
    Enter the rocket radius in feet: 55
    Enter the rocket cone height in feet: 55
    Enter the rocket cylinder height in feet: 55
    Enter the exhaust velocity for the upcoming trip: 5555
    Enter the initial velocity for the upcoming trip: 555
    Enter the angle of launch for the upcoming trip: 0.7
    Enter the length of the upcoming trip: 55
    Would you like to factor in tax? 1 for yes, 0 for no: 1
    This trip will cost $397644.19
    Now loading the rocket:
    Please enter the weight of the next item (type "Done" when you \
    are done filling the rocket): 55
    Enter item width: 5
    Enter item length: 5
    Enter item height: 5
    Please enter the weight of the next item (type "Done" when you \
    are done filling the rocket): Done
    The rocket and its equipment will weight 24255.48 kg
    Enter the simulation total time: 55
    Enter the simulation interval:5
    Now simulating the rocket trajectory:
    0.0
    1665.08
    3084.91
    4259.49
    5188.82
    5872.9
    6311.72
    6505.3
    6453.63
    6156.71
    5614.54
    4827.12
    """
    print("Welcome to the Rocket Simulation!")
    # ask for inputs
    radius = feet_to_meter(float(input("Enter the rocket radius in feet: ")))
    height_cone = feet_to_meter(float(input("Enter \
the rocket cone height in feet: ")))
    height_cyl = feet_to_meter(float(input("Enter the rocket cylinder \
height in feet: ")))
    velocity_e = float(input("Enter the exhaust velocity \
for the upcoming trip: "))
    velocity_i = float(input("Enter the initial velocity \
for the upcoming trip: "))
    angle = float(input("Enter the angle of launch for the upcoming trip: "))
    time = float(input("Enter the length of the upcoming trip: "))
    tax_determine = input("Would you like to factor in tax? \
1 for yes, 0 for no: ")
    # calculate and display the cost
    if tax_determine == "1":
        tax = True
    else:
        tax = False
    cost = calculate_cost(radius, height_cone, height_cyl, \
                          velocity_e, velocity_i, time, tax)
    print("This trip will cost $" + str(cost))
    # load the rocket and display the updated weight
    print("Now loading the rocket:")
    initial_weight = rocket_mass(radius, height_cone, height_cyl)
    weight = load_rocket(initial_weight, radius, height_cyl)
    print("The rocket and its equipment will weigh", weight, "kg")
    # simulate and display the heights
    simulation_time = int(input("Enter the simulation total time: "))
    interval = int(input("Enter the simulation interval: "))
    print("Now simulating the rocket trajectory:")
    projectile_sim(simulation_time, interval, velocity_i, angle)


rocket_main()