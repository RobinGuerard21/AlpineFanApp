import pandas as pd

track = pd.DataFrame({'Circuits': ['Bahrain', 'Saudi Arabia', 'Australia', 'Azerbaijan', 'Miami', 'Imola', 'Monaco', 'Spain', 'Canada', 'Austria', 'Great Britain', 'Hungary', 'Belgium', 'Dutch', 'Monza', 'Singapore', 'Japan', 'Qatar', 'Austin', 'Mexico', 'Brazil', 'Las Vegas', 'Abu Dhabi', 'France'],
                      'Name': ['Bahrain Grand Prix', 'Saudi Arabian Grand Prix', 'Australian Grand Prix', 'Azerbaijan Grand Prix', 'Miami Grand Prix', 'Emilia Romagna Grand Prix', 'Monaco Grand Prix', 'Spanish Grand Prix', 'Canadian Grand Prix', 'Austrian Grand Prix', 'British Grand Prix', 'Hungarian Grand Prix', 'Belgian Grand Prix', 'Dutch Grand Prix', 'Italian Grand Prix', 'Singapore Grand Prix', 'Japanese Grand Prix', 'Qatar Grand Prix', 'United States Grand Prix', 'Mexico City Grand Prix', 'São Paulo Grand Prix', 'Las Vegas Grand Prix', 'Abu Dhabi Grand Prix', 'French Grand Prix'],
                      'Length': [5.412, 6.174, 5.278, 6.003, 5.412, 4.909, 3.337, 4.675, 4.361, 4.318, 5.891, 4.381, 7.004, 4.259, 5.793, 5.063, 5.807, 5.38, 5.513, 4.304, 4.309, 6.12, 5.281, 5.842]})
track.to_csv("track.csv", index=False)

tyres = pd.DataFrame({'Circuits': ['Bahrain', 'Saudi Arabia', 'Australia', 'Imola', 'Miami', 'Azerbaijan', 'Monaco', 'Spain', 'Canada', 'Austria', 'Great Britain', 'France', 'Hungary', 'Belgium', 'Dutch', 'Monza', 'Singapore', 'Japan', 'Austin', 'Mexico', 'Brazil', 'Abu Dhabi'],
                      'Name': ['Bahrain Grand Prix', 'Saudi Arabian Grand Prix', 'Australian Grand Prix', 'Emilia Romagna Grand Prix', 'Miami Grand Prix', 'Azerbaijan Grand Prix', 'Monaco Grand Prix', 'Spanish Grand Prix', 'Canadian Grand Prix', 'Austrian Grand Prix', 'British Grand Prix', 'French Grand Prix', 'Hungarian Grand Prix', 'Belgian Grand Prix', 'Dutch Grand Prix', 'Italian Grand Prix', 'Singapore Grand Prix', 'Japanese Grand Prix', 'United States Grand Prix', 'Mexico City Grand Prix', 'São Paulo Grand Prix', 'Abu Dhabi Grand Prix'],
                      'Sprint': ['FP3', 'FP3', 'FP3', 'SQ', 'FP3', 'FP3', 'FP3', 'FP3', 'FP3', 'SQ', 'FP3', 'FP3', 'FP3', 'FP3', 'FP3', 'FP3', 'FP3', 'FP3', 'FP3', 'FP3', 'SQ', 'FP3'],
                      'Soft': ['C3', 'C4', 'C5', 'C4', 'C4', 'C5', 'C5', 'C3', 'C5', 'C5', 'C3', 'C4', 'C4', 'C4', 'C3', 'C4', 'C5', 'C3', 'C4', 'C4', 'C4', 'C5'],
                      'Medium': ['C2', 'C3', 'C3', 'C3', 'C3', 'C4', 'C4', 'C2', 'C4', 'C4', 'C2', 'C3', 'C3', 'C3', 'C2', 'C3', 'C4', 'C2', 'C3', 'C3', 'C3', 'C4'],
                      'Hard': ['C1', 'C2', 'C2', 'C2', 'C2', 'C3', 'C3', 'C1', 'C3', 'C3', 'C1', 'C2', 'C2', 'C2', 'C1', 'C2', 'C3', 'C1', 'C2', 'C2', 'C2', 'C3']})

tyres.to_csv("tyres.csv", index=False)
