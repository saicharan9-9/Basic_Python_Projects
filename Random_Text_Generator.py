import random
# List of Subjects
subjects = [
    "My dog",
    "A lazy cat",
    "My little brother",
    "The school bus driver",
    "A talking parrot",
    "My best friend",
    "A sleepy monkey",
    "The ice cream man",
    "A dancing cow",
    "My teacher"
]

# List of Actions
actions = [
    "ate my lunch",
    "sang a silly song",
    "fell in the mud",
    "ran into a wall",
    "forgot how to walk",
    "danced in the rain",
    "talked to a tree",
    "laughed for no reason",
    "jumped on the sofa",
    "cried over a donut"
]

# List of Objects
objects = [
    "at the park",
    "in the bathroom",
    "on my bed",
    "under the table",
    "during class",
    "in the kitchen",
    "at the zoo",
    "on the bus",
    "in front of everyone",
    "on the roof"
]
key = 1
while key == 1:
        subject = random.choice(subjects)
        action = random.choice(actions)
        objec_t = random.choice(objects)
        Funny_text = f"{subject} {action} {objec_t}"
        print(Funny_text)
        k = input("Do you want Generate again ?\n>> Type (yes/no): ").strip().lower()
        if k == "yes":
                key = 1
        else :
                key = 0
                print("Thank You !")
