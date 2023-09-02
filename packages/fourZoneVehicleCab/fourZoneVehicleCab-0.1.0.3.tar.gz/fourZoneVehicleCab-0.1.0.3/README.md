# fourZoneVehicleCab
Four zone vehicle cabin with incompressible air        
Explicit First order discretized for energy solver included for each control volume.
Thermal loads included from HVAC, heat exchange to the internal components, exterior air flow, solar loads and energy exchange between zones (based on Poovendran IEEE-2020).                 
Heat transfer to external air is computed based on velocity
Heat transfer to interal air is computed based on air velocity and temperature difference. The solver switches between forced, natural and mixed convection correlations

# Installation
The package can be installed using pip
```
pip install fourZoneVehicleCab
```

# Requirements

* python3
* numpy
* pandas
* matplotlib
* pythermalcomfort
* jos3

# Example
## Imports
```
import numpy as np
import fourZoneVehicleCab
import matplotlib.pyplot as plt
```
## Build model
```
cabDimensions = np.array([2.5,1.4,0.85])
massComp = 250
cpComp = 1000
internalArea = 20
externalArea = 4
nPassengers = 0

cab = fourZoneVehicleCab.fourZoneVehicleCab(cabDimensions,massComp,cpComp,internalArea,externalArea,nPassengers)
```

## Setup initial and boundary conditions
```
vehVel = 50
tempAmb = -7
solidTemp = -7
massFlow = 0.04 
massIn = np.array([0.24,0.27,0.25,0.24])
RHAmb = 50
CO2Amb = 420

tempIn = np.array([45,43,39,38])
humidityBo = cab.computeHumidity(tempAmb,RHAmb)
co2Bo = np.ones((4,))*CO2Amb

totalTime = 2400
dt = 0.2

```
## Simulate 
```
cab.simulate(dt,totalTime,vehVel,tempAmb,tempAmb,solidTemp,RHAmb,massIn,tempIn,humidityBo,co2Bo)
```
## 

