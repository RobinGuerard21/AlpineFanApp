import os
import gen.race_desc

if not os.path.exists("data"):
    os.mkdir("data")
    print(True)

if not os.path.isfile("data/races_desc.json"):
    gen.race_desc.gen_desc()