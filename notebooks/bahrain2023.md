# Bahrein GP Analysis
## Is Red Bull really over everybody ?
## 1. The context
During the testing Red Bull seemed very strong and way above the rest of the field. And during this week-end Verstappen and Perez looked very strong. Some rumors ar even mentionning some cheating or a loophole in the rules.
```python
import Alpine.gp as f1
import Alpine.utils as utils
import plotly.express as px
import pandas as pd
import numpy as np
```
## 2. The Qualifying Performance
The Qualifying results are :
* Verstappen (1:29.708)
* Perez (+0.138s)
* Leclerc (+0.292s)
* Sainz (+0.446s)

We can see here that Red Bull have a fair advantage over Ferrari on this qualifying session.
Let's dig deeper to find out where the difference was !
```python
session = f1.get_quali(2023, 1)
fig = session.lap_comp()
selected_drivers = ["VER", "PER", "LEC", "SAI"]
for trace in fig["data"]:
        if trace["name"] not in selected_drivers:
            trace["visible"] = "legendonly"
fig.show()
```
![](assets/images/bahrain/1.png)

With those plot we are able to observe that all four cars have about the same pace around this track. Verstappen mainly did the difference in corners except in corner 10 where he lost a lot of time to the other drivers
```python
session.violin_st().show()
session.top_speed().show()
```
![](assets/images/bahrain/2.png)
![](assets/images/bahrain/3.png)

On these two plots we can see that Ferrari has a better top speed than Red Bull at the speed trap by 1kph. But they still have the 2nd best top speed of all team, which is 325kph.

## 3. The Race

For the race result it's a bit different, we have :
* Verstappen 1st in 1:33:56.736
* Perez 2nd with +11.987s
* Alonso 3rd with +38.637s
* Sainz 4th with +48.052s

Leclerc has to stop lap 39 but we can still compare their laps before his DNF.
```python
race = f1.get_race(2023, 1)
fig = race.delta_to_first()
selected_drivers = ["VER", "PER", "LEC", "SAI", "ALO"]
for trace in fig["data"]:
        if trace["name"] not in selected_drivers:
            trace["visible"] = "legendonly"
fig.show()
```
![](assets/images/bahrain/4.png)
```python
def LapCompound(driver1, driver2):
    laps.loc[~laps['IsAccurate'], 'LapTime (s)'] = np.nan
    selected_driver = driver1
    selected_data = laps[(laps['Driver'] == selected_driver)]

    gray_drivers = [driver2]
    other_data = laps[(laps['Driver'].isin(gray_drivers))]

    colors = pd.unique(selected_data.Compound).tolist()
    color_mapping = {
        'SOFT': 'red',
        'MEDIUM': 'yellow',
        'HARD': 'black'
    }

    colors = [color_mapping.get(compound, 'gray') for compound in colors]
    fig = px.line(selected_data, x='LapNumber', y='LapTime (s)', color='Compound', color_discrete_sequence=colors)
    fig.add_trace(px.line(other_data, x='LapNumber', y='LapTime (s)', color_discrete_sequence=['grey']).data[0])

    fig.update_layout(
        title=f"{selected_driver} Compound to {driver2} Pace",
        xaxis_title="Lap Number",
        yaxis_title="Lap Time (s)",
    )
    return utils.logo(fig)

laps = race.laps
utils.template
LapCompound('VER','LEC').show()
LapCompound('LEC','VER').show()
LapCompound('PER','LEC').show()
LapCompound('LEC','PER').show()
```
![](assets/images/bahrain/5.png)
![](assets/images/bahrain/6.png)
![](assets/images/bahrain/7.png)
![](assets/images/bahrain/8.png)

On those 4 plots we can get a small idea where is Ferrari’s problem. With plots 1 and 2 that show Leclerc and Verstappen’s stints we can see that Leclerc stops 1 lap earlier than Verstappen to put Hards while Verstappen pits to put Softs. The problem is that Hard should be slower but last longer, here it’s not the case Leclerc is slower but after only 6 laps Leclerc starts to have a very degradation on his tyres and as we’ve seen previously, he starts to lose a lot of time compared to Verstappen and Perez. Later he has an engine problem and has to stop.
Now let’s look at each team speed
```python
race.violin_st().show()
race.top_speed().show()
```
![](assets/images/bahrain/9.png)
![](assets/images/bahrain/10.png)

Once again Red Bull still has the 2nd highest top speed but this time it's not behind Ferrari but behind Mercedes. Ferrari is at the bottom with 324 kpm just in front of Alphatauri

Let's compare lap by lap the time of Gasly, Alonso, Leclerc, Sainz, Perez and Verstappen
```python
fig = race.lap_times()
selected_drivers = ["VER", "PER", "LEC", "SAI", "ALO", "GAS"]
for trace in fig["data"]:
        if trace["name"] not in selected_drivers:
            trace["visible"] = "legendonly"
fig.show()
race.violin_lap().show()
```
![](assets/images/bahrain/11.png)
![](assets/images/bahrain/12.png)

As we can see here Verstappen was the fastest driver on the first stint, but on the following stint other drivers had very close pace to his like Perez, Alonso and a bit further Sainz and Leclerc.
At one point in the race, Gasly who started at the end of the grid and that had to do a 3 stop strategy to not be stuck behind other drivers was about 1 second/lap faster than Verstappen this has to be relativez since Gasly was on Soft while Verstappen was on Hard. And this was the lap time difference between tyre compounds:

![](https://media.formula1.com/image/upload/content/dam/fom-website/manual/Misc/2022manual/WinterMarch/BahrainGP/Tyre%20Offset.jpg.transform/9col/image.jpg)

##  4. Conclusion

As we have seen Red Bull was very consistent during the entire week-end and that is one of the reason why they won. We have also seen that their car is very polyvalent and is a bit over the rest of the field everywhere, they are fast is straights, corners, in qualifying, in race, they have a better tyre degradation and they did not had engine problem. For the moment Red Bull is over the rest but not by far and other team can still catch up all along the year.


