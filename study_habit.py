# declaring constants
WEIGHT_STUDY = 0.55 # weight constants to calculate the probability
WEIGHT_ATTENDANCE = 0.3
WEIGHT_PRACTICE = 0.7
WEIGHT_WELLNESS = 0.25
WEIGHT_HELP = 0.2

FOCUS_TRUE = 1 # to give value to focus/help factors
FOCUS_FALSE = 0.8
HELP_TRUE = 1
HELP_FALSE = 0

FOCUS_WELL = 1 # for comparison and design recommendations
SLEEP_WELL = 6
FOCUS_HOUR_WELL = 3
ATTENDANCE_WELL = 3
CODE_WELL = 4

# ask for inputs
attendance = int(input("How many hours out of 10 do you spend on attending class? "))
code = float(input("How many hours do you practice coding and review concepts each week? (out of 10): "))
focus_hour = float(input("How many deep hours per week on average do you spend studying without distractions: "))
sleep = float(input("How many hours of sleep do you have per night on average? (out of 24)" ))
exercise = float(input("How many hours do you spend on exercise and/or hobbies and/or time socializing with friends or family per week ? (out of 10):" ))
ask_for_help = input("Do you ask for help when stuck? (yes/no): ")

# Give value for the focus factor
if sleep >= SLEEP_WELL and focus_hour >= FOCUS_HOUR_WELL:
    focus = FOCUS_TRUE
else:
    # if at least one of the two conditions is not met
    focus = FOCUS_FALSE

# Give value for the help factor
if ask_for_help == "yes":
    ask_for_help = HELP_TRUE
else:
    ask_for_help = HELP_FALSE

# calculate the success probability
probability = round(WEIGHT_STUDY * focus * ((attendance / 10 * \
WEIGHT_ATTENDANCE) + (code / 10 * WEIGHT_PRACTICE)) + \
WEIGHT_WELLNESS * exercise / 10 + WEIGHT_HELP * ask_for_help, 2)

# display the probability score and the corresponding message
print("Your success score is: ", probability)

if probability >= 0.7:
    print("You're on track to do well in your class!")
else:
    print("Your success score is low. Below are suggestions to improve score:")
    
    # design and display recommendations (only if score under 0.7)
    if focus < FOCUS_WELL:
        print("    * Consider improving your sleep and focus habits:")
        # display further recommendation (only if focus under 1)
        if sleep < SLEEP_WELL:
            print("        + try sleeping for more than 6 hours")
        if focus_hour < FOCUS_HOUR_WELL:
            print("        + make sure to get at least 3 hours of deep focus without any distractions.")

    if attendance < ATTENDANCE_WELL:
        print("    * Consider attending more classes.")

    if code <= CODE_WELL:
        print("    * Consider practicing coding more.")

    if ask_for_help == HELP_FALSE:
        print("    * Consider asking for help when stuck.")