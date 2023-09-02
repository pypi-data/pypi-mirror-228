# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 10:11:03 2023

@author: anandhr
"""


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


try:
    import jos3
    import pythermalcomfort
except ImportError:
    print('Install JOS3 and pythermalcomfort packages')
        

class fourZoneVehicleCab:
    def __init__(self,cabDimensions,massComp,cpComp,internalArea,externalArea,nPassengers = 0) -> None:
        """Four zone vehicle cabin with incompressible air        
        Explicit First order discretized for energy solver included for each control volume.
        Thermal loads included from HVAC, heat exchange to the internal components, exterior air flow, solar loads and energy exchange between zones (based on Poovendran IEEE-2020).                 
        Heat transfer to external air is computed based on velocity
        Heat transfer to interal air is computed based on air velocity and temperature difference. The solver switches between forced, natural and mixed convection correlations
        
        Args:
            cabDimensions (np.array((3,))):length,width,height
            massComp (float): mass of all components inside the cabin; equally distributed to the zones
            cpComp (float): specific heat of components
            internalArea (float): Total internal area of cabin air in contact with the components in the cabin (excluding glass components)
            externalArea (float): Total area of cabin in contact with the glass components 
        """
        # cabin definition                
        self.vehLength = cabDimensions[0] #m
        self.vehWidth = cabDimensions[1] #m        
        self.vehHeight = cabDimensions[2] #m
        self.cabVolume = self.vehLength*self.vehHeight*self.vehWidth
        
        # Reference areas and lengths
        self.zoneArea = np.array([0.5,0.5,0.5,0.5])*self.cabVolume/self.vehLength
        self.zoneLength = np.array([0.5,0.5,0.5,0.5])*self.vehLength
        self.zone1_2Area = self.cabVolume/self.vehWidth/2
        self.internalArea = np.array([0.3,0.3,0.2,0.2])*internalArea
        self.externalArea = np.array([0.25,0.25,0.25,0.25])*externalArea

        # Mass of components in the cabin and specific heat
        self.massComp = np.array([0.3,0.3,0.2,0.2])*massComp
        self.cpComp = np.array([1,1,1,1])*cpComp
        
        # Number of passengers
        self.nPassenger = nPassengers
        
        # Air properties and other physics
        self.Pr = 0.73   # Prandtl number
        self.nu=1.46e-5 # Kinematic viscosity        
        self.kAir = 0.021    # thermal conductivity
        self.cp_a = 1.004e3  #J/kg
        self.density=101325/287/288.15   #density
        self.g = 9.81 #gravity            
        
        self.massZones = np.array([0.25,0.25,0.25,0.25])*self.cabVolume*self.density
        self.Rth = 0.005/0.6 # thermal resistance of glass    (t/k) 

        #Init
        self.tempZone=[]
        self.tempComp = []
        self.tempInHist = []
        self.qHVAC = []
        self.qExt=[]
        self.qInt = []
        self.qSolar = []
        self.qExch = []
        self.tempEq = []
        self.EDT = []
        self.meanCabTemp = []
        self.humidity = []
        
        
        self.passengers = []
        for i in range(self.nPassenger):
            self.passengers.append(jos3.JOS3(height=1.7,weight=75))
        
        
        self.soakTime = 1 ##s
    
    #Heat losses
    def QSolar(self,solar):
        """Solar flux on solids

        Args:
            solar (np.array((4,))): area,flux,trasmissivity, angle

        Returns:
            _type_: total solar flux on the solid components
        """
        return solar[0]*solar[1]*solar[2]*np.cos(solar[3]*np.pi/180)

    def QExt(self,vehVel,tempAmb,massFlow,tempZone):
        """Heat lost to the external ambient from the cabin

        Args:
            vehVel (float): vehicle velocity
            tempAmb (float): ambient temperature
            massFlow (np.array((4,))): mass flow through each zone
            tempZone (np.array((4,))): temperature at each zone

        Returns:
            _type_: np.array((4,)): Heat lost to ambient
        """
        # External HTC
        hExt=1.163*(4+10*np.sqrt(abs(vehVel)/3.6))
        
        zoneVelocity = massFlow/self.density/self.zoneArea
        #refLen = np.sqrt(self.zoneArea)
        refLen = self.vehHeight/2
        #Internal HTC: Mixed convection from 11.4.8
        A = (0.339*self.Pr**(1/3)*(1+(0.0468/self.Pr)**(2/3))**-0.25)*2
        B = (0.75*self.Pr**0.5*(2.5*(1+2*np.sqrt(self.Pr)+2*self.Pr)**(2/3))**-0.25)*4/3
            
        Re = (zoneVelocity)*refLen/self.nu     
        Gr = abs(self.g*1/273.15*(tempZone-self.tempComp[-1,:])*refLen**3/self.nu**2)
        Bo = Gr/Re**2
        
        
        if all(Bo<10) and all(Bo>0.1):
            Nu = A/Re**-0.5*(1+(B/A*Bo**0.25)**3 )**1/3        
        elif all(Bo<0.1):        
            Nu=A*Re**0.5           
        else:
            Nu = B*Gr**0.25  
        
        hInt = Nu*self.kAir/(refLen)
        
        totalR = 1/(hExt*self.externalArea)+self.Rth/self.externalArea+1/(hInt*self.externalArea)
        qExt = (tempZone-tempAmb)/totalR
        
        return qExt
        
    def QInt(self,tempZone,tempComp,massFlow):
        """Heat lost to the internal components

        Args:
            tempZone (np.array((4,))): temperature at each zone
            tempComp (np.array((4,))): temperature of components in each zone
            massFlow (np.array((4,))): mass flow through each zone

        Returns:
            _type_: Heat lost to the internal components
        """
        #Internal HTC: Mixed convection from 11.4.8
        A = (0.339*self.Pr**(1/3)*(1+(0.0468/self.Pr)**(2/3))**-0.25)*2
        B = (0.75*self.Pr**0.5*(2.5*(1+2*np.sqrt(self.Pr)+2*self.Pr)**(2/3))**-0.25)*4/3
            
        zoneVelocity = massFlow/self.density/self.zoneArea
        refLen = np.sqrt(self.zoneArea)
        #refLen = self.zoneArea/((self.vehHeight+0.5*self.vehWidth)*2)
        Re = (zoneVelocity)*refLen/self.nu     
        Gr = abs(self.g*1/273.15*(tempZone-tempComp)*refLen**3/self.nu**2)
        Bo = Gr/Re**2
        
        if all(Bo<10) and all(Bo>0.1):
            Nu = A/Re**-0.5*(1+(B/A*Bo**0.25)**3 )**1/3        
        elif all(Bo<0.1):        
            Nu=A*Re**0.5           
        else:
            Nu = B*Gr**0.25  
        hInt = Nu*self.kAir/(refLen)
        
        
        qInt = hInt*self.internalArea*(tempZone-tempComp)
        return qInt

    def QExch(self,massFlow,tempZone):
        """Heat exchange across zones

        Args:
            massFlow (np.array((4,))): mass flow through each zone
            tempZone (np.array((4,))): temperature at each zone

        Returns:
            (np.array((4,))): Heat exchange across zones
        """
        mLU = np.array([0.,0.02,0.04,0.06,0.08,0.1,0.12])
        h1 = np.array([19,22,24.5,26,26,27.5,29])
        h2 = np.array([24.7,27.5,30.5,32.5,34.5,35.5,36.5])
        
        # from 1-2 & 1-3
        h1_2 = np.interp(massFlow[0],mLU,h1)
        h1_3 = np.interp(massFlow[2],mLU,h2)
        
        # from 2-1 & 2-3
        #h2_1 = np.interp(massFlow[1],mLU,h1)
        h2_4 = np.interp(massFlow[3],mLU,h2)
        
        # from 3-2
        h3_4 = np.interp(massFlow[2],mLU,h1)
            
        QExch1_2 = h1_2*self.zone1_2Area*(tempZone[1]-tempZone[0])
        #QExch2_1 = h2_1*zone1_2Area*(tempZone[0]-tempZone[1])
        QExch1_3 = h1_3*self.zoneArea[0]*(tempZone[2]-tempZone[0])
        
        QExch2_4 = h2_4*self.zoneArea[1]*(tempZone[3]-tempZone[1])
        QExch3_4 = h3_4*self.zone1_2Area*(tempZone[3]-tempZone[2])
        
        qExch = np.array([QExch1_2+QExch1_3,-QExch1_2+QExch2_4,-QExch1_3+QExch3_4,-QExch2_4-QExch3_4])
        
        return qExch
            
    def QHVAC(self,massFlow,tempIn,tempZone):
        """Heat transfer from HVAC

        Args:
            massFlow (np.array((4,))): mass flow through each zone
            tempIn (np.array((4,))): temperature Into each zone
            tempZone (np.array((4,))): temperature at each zone

        Returns:
            np.array((4,)): Heat transfer from HVAC
        """
        qHVAC = np.zeros([4,])
        qHVAC[0] = massFlow[0]*self.cp_a*(tempIn[0]-tempZone[0])
        qHVAC[1] = massFlow[1]*self.cp_a*(tempIn[1]-tempZone[1])
        qHVAC[2] = massFlow[2]*self.cp_a*tempIn[2]+massFlow[0]*self.cp_a*tempZone[0] - np.sum([massFlow[0],massFlow[2]])*self.cp_a*tempZone[2]
        qHVAC[3] = massFlow[3]*self.cp_a*tempIn[3]+massFlow[1]*self.cp_a*tempZone[1] - np.sum([massFlow[1],massFlow[3]])*self.cp_a*tempZone[3] 
        
        return qHVAC

    def QPassenger(self):
        names = jos3.BODY_NAMES
        qPassengers = np.zeros((4,))
        sensibleHeatProduction = 0
        for i in range(self.nPassenger):
            df = pd.DataFrame(self.passengers[i].dict_results())
            sensibleHeatProduction = np.sum([df['SHLsk'+names[i]].iloc[-1] for i in range(len(names))])
            qPassengers[i] = sensibleHeatProduction+df['RESsh'].iloc[-1]
        
        return qPassengers

    def Co2In(self,massFlow,co2Bo,co2Zone):
        co2In = np.zeros((4,))
        
        co2In[0] = massFlow[0]*(co2Bo[0]-co2Zone[0])
        co2In[1] = massFlow[1]*(co2Bo[1]-co2Zone[1])
        co2In[2] = massFlow[2]*co2Bo[2] + massFlow[0]*co2Zone[0] - np.sum([massFlow[0],massFlow[2]])*co2Zone[2]
        co2In[3] = massFlow[3]*co2Bo[3] + massFlow[1]*co2Zone[1] - np.sum([massFlow[1],massFlow[3]])*co2Zone[3]
        
        return co2In
            
    def Co2Source(self):
        breathRate = 1.5e-4*self.density
        sourceCo2 = 4e4
        co2Source = np.zeros((4,))
        for i in range(self.nPassenger):
            co2Source[i] = breathRate*sourceCo2
        return co2Source
    
    def HumiditySource(self):
        breathRate = 1.5e-4*self.density
        names = jos3.BODY_NAMES
        humiditySource = np.zeros((4,))
        latentHeatProduction = 0
        for i in range(self.nPassenger):
            df = pd.DataFrame(self.passengers[i].dict_results())
            latentHeatProduction = np.sum([df['LHLsk'+names[i]].iloc[-1] for i in range(len(names))])
            massFromSkin = latentHeatProduction/2.4e6
            humidityFromSkin = massFromSkin*self.computeHumidity(df.TskMean.iloc[-1],100)
            humidityFromBreath = breathRate*self.computeHumidity(df.TcrHead.iloc[-1],70)
            humiditySource[i] = humidityFromBreath+humidityFromSkin
        return humiditySource
        
    def Icl(self,Ta):
        if Ta < 10:
            """head = 0.2
            shirt = 1.5
            pant = 1.5
            shoe = 0.2
            hand = 0.2"""
            head = 0.05
            shirt = 1.2
            pant = 1
            shoe = 0.15
            hand = 0.15
        elif Ta>30:
            head = 0.
            shirt = 0.1
            pant = 0.1
            shoe = 0.05
            hand = 0.
        else:
            head = 0.
            shirt = 0.7
            pant = 0.4
            shoe = 0.13
            hand = 0.
        
        icl = [head,shirt,shirt,shirt,shirt+pant,shirt,shirt,hand,shirt,shirt,hand,pant,pant,shoe,pant,pant,shoe]  #clo
        
        
        return icl
    
    def Tetans(self,Ta):
        if Ta<0:
            saturationPressure = 0.61078*np.exp(21.875*Ta/(Ta+265.5))*1000
        else:
            saturationPressure = 0.61078*np.exp(17.27*Ta/(Ta+237.3))*1000
        
        return saturationPressure
    
    def Antoine(self,t):
        a = 11.949
        b=3978.205
        c=-39.801
        p = 101325*np.exp(a-b/(t+273-39.801))
        return p
    
    def computeRH(self,Ta,humidity):
        saturationPressure = self.Antoine(Ta)
        RH = humidity*101325/((0.622+humidity)*saturationPressure)
        return RH*100
    
    def computeHumidity(self,Ta,RH):
        saturationPressure =self.Antoine(Ta)
        humidity = 0.622*RH/100*saturationPressure/(101325-RH/100*saturationPressure)
        return humidity
        
    def simulate(self,dt,totalTime,vehVel,tempAmb,airTemp,solidTemp,RHAmb,massIn,tempIn,humidityBo=np.ones((4,))*0.001,co2Bo=np.ones((4,))*420,solar=np.array([0,0,0,0])):
        """Simulate cabin model

        Args:
            dt (float): times step
            totalTime (float): total simulation time
            vehVel (float): vehicle velocity
            tempAmb (float): ambient temperature
            airTemp (float): initial air temperature
            solidTemp (float): initial solid temperature
            massIn (np.array((4,))): massflow into each zone
            tempIn (np.array((4,))): temperature into each each zone
            solar (np.array((4,)), optional): exposed area, flux, transmissivity, angle. Defaults to np.array([0,0,0,0]).
        """
        nZones = 4
        self.setPoint=22
        #time = np.linspace(0,totalTime,nSteps)
        if np.size(self.tempZone)==0:   ## New simulation
            nSteps = int(totalTime/dt+1)
            ## Create matrices
            # temperatures
            self.tempZone = np.zeros((nSteps,nZones))
            self.tempComp = np.zeros((nSteps,nZones))            
            
            # humidity
            self.humidity = np.zeros((nSteps,nZones))
            self.humidityIn = np.zeros((nSteps,nZones))
            self.RH = np.zeros((nSteps,nZones))
            # CO2
            self.co2In = np.zeros((nSteps,nZones))
            self.co2 = np.zeros((nSteps,nZones))                        
            
            # other metrics
            self.tempEq = np.zeros((nSteps,nZones))
            self.EDT = np.zeros((nSteps,nZones))
            self.meanCabTemp = np.zeros((nSteps,))
            
            # Assign init conditions
            self.tempZone[0,:] = airTemp
            self.tempComp[0,:] = solidTemp
            self.tempEq[0,:] = (airTemp+solidTemp)/2
            self.EDT[0,:] = (airTemp-self.setPoint)+0.1276*0.15
            self.meanCabTemp[0] = np.mean(np.array(airTemp))
            self.co2[0,:] = 420
            self.humidity[0,:] = self.computeHumidity(airTemp, RHAmb)
            
            self.qExt = np.zeros((nSteps,nZones))
            self.qInt = np.zeros((nSteps,nZones))
            self.qExch = np.zeros((nSteps,nZones))
            self.qHVAC = np.zeros((nSteps,nZones))
            
            self.co2Exch = np.zeros((nSteps,nZones))
            self.humidityExch = np.zeros((nSteps,nZones))
            startIndex = 1
            self.qPassenger = np.zeros((4,))
            self.humiditySource = np.zeros((4,))
            ## Initialize human model
            for i in range(len(self.passengers)):
                self.passengers[i].Ta = self.tempZone[0,i]
                self.passengers[i].Tr = (self.tempComp[0,i]*1.1+self.tempZone[0,i]*0.9)/2
                self.passengers[i].Icl = self.Icl(self.tempZone[0,0])
                self.passengers[i].RH = RHAmb
                if i ==0:
                    self.passengers[i].PAR = 1.6
                else:
                    self.passengers[i].PAR = 1.2
                self.passengers[i].simulate(1,self.soakTime)
                
        else: # Update existing solution
            nSteps=int(totalTime/dt)+1
            startIndex = self.tempZone.shape[0]    
            #Append matrices
            # temperatures            
            self.tempZone = np.concatenate((self.tempZone,np.zeros((nSteps-1,nZones))))
            self.tempComp = np.concatenate((self.tempComp,np.zeros((nSteps-1,nZones))))     
            
            # humidity
            self.humidity = np.concatenate((self.humidity,np.zeros((nSteps-1,nZones))))   
            self.humidityIn = np.concatenate((self.humidityIn,np.zeros((nSteps-1,nZones))))   
            
            # co2
            self.co2In = np.concatenate((self.co2In,np.zeros((nSteps-1,nZones))))   
            self.co2 = np.concatenate((self.co2,np.zeros((nSteps-1,nZones))))   
              
            # other metrics       
            self.tempEq = np.concatenate((self.tempEq,np.zeros((nSteps-1,nZones))))
            self.EDT = np.concatenate((self.EDT,np.zeros((nSteps-1,nZones))))            
            self.meanCabTemp = np.concatenate((self.meanCabTemp,np.zeros((nSteps-1))))
            
            self.qExt = np.concatenate((self.qExt,np.zeros((nSteps-1,nZones))))
            self.qInt = np.concatenate((self.qInt,np.zeros((nSteps-1,nZones))))
            self.qExch = np.concatenate((self.qExch,np.zeros((nSteps-1,nZones))))
            self.qHVAC = np.concatenate((self.qHVAC,np.zeros((nSteps-1,nZones))))            
            
            self.co2Exch = np.concatenate((self.co2Exch,np.zeros((nSteps-1,nZones))))
            self.humidityExch = np.concatenate((self.humidityExch,np.zeros((nSteps-1,nZones))))
            
            
            
            
        self.qSolar = self.QSolar(solar)
        
        
        self.co2Source = self.Co2Source()
        massFlow = np.array([massIn[0],massIn[1],massIn[0]+massIn[2],massIn[1]+massIn[3]])
        if len(self.meanCabTemp)%5==1:
                for j in range(len(self.passengers)):
                    self.passengers[j].Ta = self.tempZone[-2,j]
                    self.passengers[j].Tr = (self.tempComp[-2,j]*1.1+self.tempZone[-2,j]*0.9)/2
                    self.passengers[j].RH = self.computeRH(self.tempZone[-2,j], self.humidity[-2,j])             
                    self.passengers[j].Va = massFlow[j]/self.density/self.zoneArea[j]
                    self.passengers[j].simulate(1,5*dt)
                    self.qPassenger = self.QPassenger() #heat from humans
                    self.humiditySource = self.HumiditySource() #humidity from humans
        
        
        
        for i in range(startIndex,startIndex+nSteps-1):        
            # temperature                
            # solids
            self.tempComp[i,:]=self.tempComp[i-1,:]+dt/self.massComp/self.cpComp*(self.qInt[i-1,:]+self.qSolar)
            
            # air
            self.tempZone[i,:]=self.tempZone[i-1,:]+dt/self.massZones/self.cp_a*(self.qHVAC[i-1,:]+self.qPassenger-self.qExt[i-1,:]-self.qInt[i-1,:])
                                    
            # co2          
            dampingFactor = min(1.25,np.abs(1.25/(1.2*9.8*1/(273.15+(tempAmb+self.setPoint)/2)*(37-np.mean(self.tempZone[i-1,:])))))
            self.co2[i,:] = self.co2[i-1,:]+dt/self.massZones*(self.co2In[i-1,:]+self.co2Source/dampingFactor+self.co2Exch[i-1,:])
            
            # update human every nth timeStep
            
                    
            #humidity
            self.humidity[i,:] = self.humidity[i-1,:]+dt/self.massZones*(self.humidityIn[i-1,:]+self.humiditySource+self.humidityExch[i-1,:])
            
            ## humidity sources and sinks
            
            self.humidityIn[i,:] = self.Co2In(massIn,humidityBo,self.humidity[i,:])
            #self.humidityExch[i,:] = self.QExch(massFlow,self.humidity[i,:])/250
            
            #co2 sources and sinks
            self.co2In[i,:] =  self.Co2In(massIn,co2Bo,self.co2[i,:])  
            self.co2Exch[i,:] = self.QExch(massFlow,self.co2[i,:])/250
            
            #self.co2Exch[i,:] = np.zeros(4,)
            # heat sources and sinks    
            # heat to ambient                                 
            self.qExt[i,:] = self.QExt(vehVel,tempAmb,massFlow,self.tempZone[i,:])
            
            #heat to interior
            self.qInt[i,:] = self.QInt(self.tempZone[i,:],self.tempComp[i,:],massFlow)
            
            #heat exch between zones
            self.qExch[i,:] = self.QExch(massFlow,self.tempZone[i,:])
            
            #heat from HVAC
            self.qHVAC[i,:] = self.QHVAC(massIn,tempIn,self.tempZone[i,:])
            
                        
            
            # Other parameters - comfort computation
            self.tempEq[i,:] = (self.tempZone[i,:]+self.tempComp[i,:])/2        
            velocity = massFlow/self.density/self.zoneArea            
            for j in range(nZones):
                if velocity[j]>0.1:
                    self.tempEq[i,j] = 0.55*self.tempZone[i,j]*0.45*self.tempComp[i,j]+(0.24-0.75*np.sqrt(velocity[j]))/(1+self.iClothing)*(36-5-self.tempZone[i,j])
            
            self.EDT[i,:] = (self.tempZone[i,:]-self.setPoint)-0.1276*(velocity-0.15)
            self.meanCabTemp[i] = sum(self.tempZone[i,:]*self.zoneArea*self.zoneLength)/self.cabVolume
            #self.RH[i,:] = self.computeRH(self.tempZone[i,:],self.humidity[i,:])
            
    def Update(self,dt,totalTime,vehVel,tempAmb,airTemp,solidTemp,massIn,tempIn,reCirc,heaterSum,heaterRate,PID,solar=np.array([0,0,0,0])):
        heater = 0.                
        errorSum = heaterSum
        errorOld = 0.
        outSum = 0.
        tempIn = np.ones((4,))*tempIn
        Kp = PID[0]
        Ki = PID[1]
        Kd = PID[2]
        nSteps = int(totalTime/dt)
        self.tempInHist = np.ones((nSteps,))
        for i in range(nSteps):
            self.simulate(dt,dt,vehVel,tempAmb,airTemp,solidTemp,massIn,tempIn,solar=np.array([0,0,0,0]))
            #PI control for temperature inlet
            error = np.mean(self.tempEq[i-1,:])-self.setPoint
            errorSum += error*dt
            
            errorDiff = (error-errorOld)/dt
            out = error*Kp+errorSum*Ki+errorDiff*Kd
            errorOld = error
            if out<-heaterRate:
                out=-heaterRate
            elif out>heaterRate:
                out=heaterRate
            #outSum+=out*dt
            tempBo = reCirc*self.meanCabTemp[-1]+(1-reCirc)*tempAmb
            tempAtInlet = tempBo+out/sum(massIn)/self.cp_a 
            tempIn = np.ones((4,))*tempAtInlet
            self.tempInHist[i] = tempAtInlet
        return errorSum,out  
    
    def to_csv(self,fileName):
        columns=['meanCabTemp','meanCompTemp','CO2','humidity','tempZone1',
                 'tempZone2','tempZone3','tempZone4','tempComp1','tempComp2',
                 'tempComp3','tempComp4']
        df = pd.DataFrame({columns[0]:self.meanCabTemp,
                           columns[1]:np.mean(self.tempComp,axis=1),
                           columns[2]:np.mean(self.co2,axis=1),
                           columns[3]:np.mean(self.humidity,axis=1),
                           columns[4]:self.tempZone[:,0],
                           columns[5]:self.tempZone[:,1],
                           columns[6]:self.tempZone[:,2],
                           columns[7]:self.tempZone[:,3],
                           columns[8]:self.tempComp[:,0],
                           columns[9]:self.tempComp[:,1],
                           columns[10]:self.tempComp[:,2],
                           columns[11]:self.tempComp[:,3]})
        df.to_csv(fileName+'.csv')
        for i in range(self.nPassenger):
            out = pd.DataFrame(self.passengers[i].dict_results())
            out.to_csv(fileName+'Passenger_'+str(i)+'.csv')
            
    def GetPMVPPD(self):
        Ta = self.tempZone
        Tr = (self.tempComp*1.1+self.tempZone*0.9)/2
        zoneVelocity = 0.1
        RH = self.computeRH(Ta,self.humidity)
        clo = np.mean(self.Icl(Ta[0,0]))        
        pmv = pythermalcomfort.pmv_ppd(Ta,Tr,zoneVelocity,RH,1.5,clo)
        return pmv    



if __name__=='__main__':
    ## Test simulation
    #cabDimensions = np.array([1.9,1.433,1.2])
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
    
    cab = fourZoneVehicleCab(cabDimensions,massComp,cpComp,internalArea,externalArea,0)
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
    
    time = np.arange(0,totalTime+dt,dt)
    plt.figure()
    plt.plot(time,cab.meanCabTemp)
    plt.xlabel('time (s)')
    plt.ylabel(r'Mean cabin temperature ($^\circ C$)')
    
    
    plt.figure()
    plt.plot(time[:-1],tempInHist)
    plt.xlabel('time (s)')
    plt.ylabel(r'Inlet temperature ($^\circ C$)')
    
    plt.figure()
    plt.plot(time[:-1],heaterHist)
    plt.xlabel('time (s)')
    plt.ylabel(r'Heater rate ($W$)')
    
    plt.figure()
    plt.plot(time,cab.tempZone[:,0],label='Zone-1')
    plt.plot(time,cab.tempZone[:,1],label='Zone-2')
    plt.plot(time,cab.tempZone[:,2],label='Zone-3')
    plt.plot(time,cab.tempZone[:,3],label='Zone-4')
    plt.legend()
    plt.xlabel('time (s)')
    plt.ylabel(r'Cabin temperature ($^\circ C$)')
    
