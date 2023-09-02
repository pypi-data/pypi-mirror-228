import fourZoneVehicleCab 
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
if __name__=='__main__':
	cabDimensions = np.array([2.5,1.4,0.85])
	massComp = 250
	cpComp = 1000
	internalArea = 20
	externalArea = 4
	recirc = 0. #np.linspace(0,1,11)

	totalTime = 2400
	dt = 0.2
	vehVel = 50
	tempAmb = -7
	solidTemp = -7
	massFlow = 0.04 #np.linspace(0.02,0.12,11)
	RHAmb = 50
	CO2Amb = 420

	cab = fourZoneVehicleCab.fourZoneVehicleCab(cabDimensions,massComp,cpComp,internalArea,externalArea,0)
	massIn = np.array([0.381,0.389,0.11,0.12])*massFlow

	#PI controller
	Kp = -7
	Ki = -0.5
	errorSum=0
	energyCons = 0
	#

	co2Bo = np.ones((4,))*CO2Amb
	humidityBo = np.ones((4,))*cab.computeHumidity(tempAmb, RHAmb)

	nSteps = int(totalTime/dt)

	tempIn = np.ones((4,))*tempAmb

	## Dynamics of case    
	tempInHist = np.zeros((nSteps))
	heaterHist = np.zeros((nSteps))

	#Simulate
	for i in range(nSteps):
		cab.simulate(dt,dt,vehVel,tempAmb,tempAmb,solidTemp,RHAmb,massIn,tempIn,humidityBo,co2Bo)        
		
		#PI control for temperature inlet
		error = np.mean(cab.meanCabTemp[-1])-cab.setPoint
		errorSum += error*dt
		heaterRate = error*Kp+errorSum*Ki                
		
		energyCons+=heaterRate*dt
		tempBo = recirc*cab.meanCabTemp[-1]+(1-recirc)*tempAmb
		tempAtInlet = tempBo+heaterRate/sum(massIn)/cab.cp_a 
		
		if tempAtInlet>60:
		    tempAtInlet = 60
		    heaterRate = sum(massIn)*cab.cp_a*(tempAtInlet-tempBo)
		    errorSum = (heaterRate-Kp*error)/Ki
		elif tempAtInlet<2:
		    tempAtInlet = 2
		    heaterRate = sum(massIn)*cab.cp_a*(tempAtInlet-tempBo)
		    errorSum = (heaterRate-Kp*error)/Ki
		tempIn = np.ones((4,))*tempAtInlet
		tempInHist[i] = tempAtInlet   
		heaterHist[i] = heaterRate
		co2Bo = recirc*cab.co2[-1,:]+(1-recirc)*CO2Amb
		humidityBo = recirc*cab.humidity[-1,:]+(1-recirc)*cab.computeHumidity(tempAmb, RHAmb)
		print('time: ',i*dt, 'heaterRate: ',heaterRate, 'meanCabTemp: ',cab.meanCabTemp[-1])
