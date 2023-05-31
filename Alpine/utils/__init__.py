from . import colors, template, time
import warnings
import logging


__all__ = ['driver_color', 'team_color', 'error']


def driver_color(driver):
    """
    This function is made to return the driver's Hex code to be able to use his color wherever you need it.
    Be careful the only drivers accepted are the drivers from 2021 to 2023.

    Parameters
    ----------
    driver : str or list
        You can either enter a driver or a list of driver.
        The driver name is made by his lastname's 3 first letters in capital case.

    year : int, optional
        By default 2023. Since the api was made in 2023 any other int given will give you the results for the drivers for 2022.

    show_driver : bool, optional
        By default set to False. If True, the driver and its Hex code will be printed in the console.

    See Also
    --------
    team_color(team, show_driver) : This function is made to return the teams' Hex code to be able to use their color wherever you need it.
        Be careful the only teams accepted are the teams from 2021 to 2023.

    Examples
    --------
    >>> from Alpine import utils
    >>> print(utils.driver_color("OCO"))
    #70c2ff
    >>> print(driver_color(['NOR', 'RUS', 'SAI', 'HAM', 'DRU', 'OCO']))
    ['#eeb370', '#24ffff', '#ff8181', '#00d2be', '#25a617', '#70c2ff']
    >>> driver_color("OCO", show_driver=True)
    The color for OCO is #70c2ff.

    Returns
    -------
    Hex : str or list
        The driver's Hex code of the driver if you passed a string.
        The drivers' Hex code in the same order as the drivers in a list.
    show_driver : bool
        True if `show_driver` is set to True.
    Hex : str or list
        The driver's Hex code of the driver if you passed a string.
        The drivers' Hex code in the same order as the drivers in a list.
    """

    if isinstance(driver, (str, list)):
        return colors._driver_colors(driver)
    else:
        warnings.warn(f"Only list or strings are accepted by this variable",
                      Warning, stacklevel=2)


def team_color(teams):
    if isinstance(teams, (str, list)):
        return colors._team_colors(teams)
    else:
        warnings.warn(f"Only list or strings are accepted by this variable",
                      Warning, stacklevel=2)


def logo(fig, rows=1):
    for i in range(1, rows+1):
        fig.add_layout_image(
            dict(
                # source="https://cdn.cookielaw.org/logos/1058e0b9-ee95-4d43-8292-3dae40ce5c3c/b4f83c83-bbed-4615-94dd-e1db19ab289e/d93ec308-72e0-452b-aa87-506f7e2a88e1/Alpine_logo_name.png",
                source="https://raw.githubusercontent.com/RobinGuerard21/AlpineFanApp/a099c24536929e6f5b3930eff59a5b0d8098d3be/F1Dashboard-main/assets/images/logo_dark.png",
                xref="x domain",
                yref="y domain",
                x=0.5,
                y=0.5,
                sizex=0.5,
                sizey=0.5,
                xanchor="center",
                yanchor="middle",
                opacity=0.4
            ), row=i, col=1
        )
    return fig


def error(issue):
    logger = logging.getLogger(__name__)

    file_handler = logging.FileHandler('logs/warnings.log')
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.warning(issue)