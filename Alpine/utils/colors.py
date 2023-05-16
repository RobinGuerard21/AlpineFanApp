# TODO: not sure it's useful now that the api was actualized with the new drivers and their colors
import warnings

drivers_list = ['PER', 'VER', 'ALO', 'RUS', 'HAM', 'SAI', 'LEC', 'OCO', 'GAS', 'MAG', 'TSU', 'HUL', 'ZHO', 'DEV', 'PIA', 'SAR', 'NOR', 'BOT', 'ALB', 'STR']

drivers_colors = {'ALB': '#005aff', 'SAI': '#ff8181', 'LEC': '#dc0000', 'OCO': '#70c2ff', 'DRU': '#2f9b90', 'ALO': '#006f62',
                'RUS': '#24ffff', 'MAG': '#000000', 'STR': '#25a617', 'NOR': '#eeb370', 'HAM': '#00d2be', 'SAR': '#012564',
                'VER': '#0600ef', 'HUL': '#373737', 'DEV': '#2b4562', 'PIA': '#ff8700', 'GAS': '#0090ff', 'PER': '#716de2',
                'BOT': '#900000', 'TSU': '#356cac', 'ZHO': '#500000'}

teams_list = ['Red Bull Racing', 'Aston Martin', 'Mercedes', 'Ferrari', 'Alpine', 'Haas F1 Team', 'AlphaTauri',
              'Alfa Romeo', 'McLaren', 'Williams']

teams_colors = {'Alfa Romeo': '#900000', 'AlphaTauri': '#2b4562', 'Alpine': '#0090ff', 'Aston Martin': '#006f62',
                'Ferrari': '#dc0000', 'Haas F1 Team': '#000000', 'McLaren': '#ff8700', 'Mercedes': '#00d2be',
                'Red Bull Racing': '#0600ef', 'Williams': '#005aff'}

def _driver_colors(drivers):
    if isinstance(drivers, list):
        colors = []
        for i in drivers:
            if i in drivers_list:
                colors.append(drivers_colors[i])
            else:
                warnings.warn(f"The driver {i} is not supported by the system. If you are using older years please use the team colors!",
                              Warning, stacklevel=2)
                colors.append("#34495e")
    elif isinstance(drivers, str):
        if drivers in drivers_list:
            colors = drivers_colors[drivers]
        else:
            warnings.warn(
                f"The driver {drivers} is not supported by the system. If you are using older years please use the team colors!",
                Warning, stacklevel=2)
            colors = "#34495e"
    return colors


def _team_colors(teams):
    if isinstance(teams, list):
        colors = []
        for i in teams:
            if i in teams_list:
                colors.append(teams_colors[i])
            else:
                warnings.warn(f"The team {i} is not supported by the system !",
                              Warning, stacklevel=2)
                colors.append("#34495e")
    elif isinstance(teams, str):
        if teams in teams_list:
            colors = teams_colors[teams]
        else:
            warnings.warn(
                f"The team {teams} is not supported by the system !",
                Warning, stacklevel=2)
            colors = "#34495e"
    return colors