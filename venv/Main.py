from matplotlib import pyplot as plt
import pyabf
import numpy as np
#Setup
abf = pyabf.ABF("2019 10 04_Cell 1_Rheo_0013.abf")
abf.setSweep(1)
plt.title("Analysis of 1 Action Potential")
plt.ylabel("mV")
plt.xlabel("ms")
abf.setSweep(sweepNumber=1, channel=0)
plt.plot(abf.sweepX*1000, abf.sweepY, label = "Original Graph")
arrayX = np.array(abf.sweepX).tolist()
arrayY = np.array(abf.sweepY).tolist()
arrayX = np.delete(arrayX,19999)
dvdt = np.diff(abf.sweepY)
abf.setSweep(sweepNumber=1, channel=0)
#plt.plot(arrayX*1000, dvdt*10, label="Derivative Graph")
updatedvdt = dvdt*10
updatedvdtlist = np.array(updatedvdt).tolist()

#Threshold
tempDiff = 100
thresholdIndex = 0
for index in range(0,len(updatedvdtlist)):
  if (updatedvdtlist.__getitem__(index)) >= 20:
      thresholdIndex = index
      break
plt.axvline(x = arrayX.__getitem__(thresholdIndex)*1000, linewidth = 1, color = "r", linestyle = "dashed",label = "Threshold Point (20 V/s)")
plt.text(arrayX.__getitem__(thresholdIndex)*1000-0.2,arrayY.__getitem__(thresholdIndex),(str)((round)(arrayY.__getitem__(thresholdIndex),2))+"mV",rotation = 90)


#Max Rise Rate
tempMax = 0
maxRateIndex = 0
for i in range(0,len(updatedvdtlist)):
    if(updatedvdtlist.__getitem__(i) > tempMax):
        tempMax = updatedvdtlist.__getitem__(i)
        maxRateIndex = i
plt.axvline(x = arrayX.__getitem__(maxRateIndex)*1000, linewidth = 1, color = "yellow", linestyle = "dashed", label = "Max Rise Rate")
plt.text(arrayX.__getitem__(maxRateIndex)*1000-0.2,arrayY.__getitem__(maxRateIndex),(str)((round)(updatedvdtlist.__getitem__(maxRateIndex),2))+"V/s",rotation = 90)

#Max Fall Rate
tempMin = 0
minRateIndex = 0
for i in range(0,len(updatedvdtlist)):
    if(updatedvdtlist.__getitem__(i) < tempMin):
        tempMin = updatedvdtlist.__getitem__(i)
        minRateIndex = i
plt.axvline(x = arrayX.__getitem__(minRateIndex)*1000, linewidth = 1, color = "orange", linestyle = "dashed", label = "Max Fall Rate")
plt.text(arrayX.__getitem__(minRateIndex)*1000-0.2,arrayY.__getitem__(minRateIndex),(str)((round)(updatedvdtlist.__getitem__(minRateIndex),2))+"V/s",rotation = 90)

#Peak Amplitude
tempMaxValue = 0
peakIndex = 0
for i in range(0, len(arrayY)):
    if(arrayY.__getitem__(i) > tempMaxValue):
        tempMaxValue = arrayY.__getitem__(i)
        peakIndex = i
plt.axvline(x = arrayX.__getitem__(peakIndex)*1000, linewidth = 1, color = "g", linestyle = "dashed", label = "Peak Amplitude")
plt.text(arrayX.__getitem__(peakIndex)*1000-0.2,arrayY.__getitem__(peakIndex),(str)((round)(arrayY.__getitem__(peakIndex)-arrayY.__getitem__(thresholdIndex),2))+"mV")

#AHP
tempMinValue = 0
AHPIndex = 0
for i in range(thresholdIndex, thresholdIndex+2000):
    if(arrayY.__getitem__(i) < tempMinValue):
        tempMinValue = arrayY.__getitem__(i)
        AHPIndex = i
plt.axvline(x = arrayX.__getitem__(AHPIndex)*1000, linewidth = 1, color = "purple", linestyle = "dashed", label = "AHP")
plt.text(arrayX.__getitem__(AHPIndex)*1000-0.2,arrayY.__getitem__(AHPIndex),(str)((round)(arrayY.__getitem__(AHPIndex),2))+"mV",rotation = 90)

#Half-Width
diff = arrayY.__getitem__(peakIndex)-arrayY.__getitem__(AHPIndex)
diff /= 2
diff += arrayY.__getitem__(AHPIndex)
yAbove1 = 0
for i in range(0,peakIndex):
    if(arrayY.__getitem__(i) >= diff):
        yAbove1 = i
        break
yBelow2 = 0
for i in range(peakIndex,AHPIndex):
    if(arrayY.__getitem__(i) <= diff):
        yBelow2 = i
        break
yAbove2 = yBelow2-1
yBelow1 = yAbove1-1
slope1 = (arrayY.__getitem__(yAbove1)-arrayY.__getitem__(yBelow1))/0.0001
slope2 = (arrayY.__getitem__(yBelow2)-arrayY.__getitem__(yAbove2))/0.0001
intercept1 = arrayY.__getitem__(yAbove1)-(slope1*arrayX.__getitem__(yAbove1))
intercept2 = arrayY.__getitem__(yAbove2)-(slope2*arrayX.__getitem__(yAbove2))
x1 = (diff-intercept1)/slope1
x2 = (diff-intercept2)/slope2
halfWidth = x2-x1
xCoordinates = [x1*1000,x2*1000]
yCoordinates = [diff,diff]
plt.plot(xCoordinates, yCoordinates, linewidth = 1, color = "brown", linestyle = "dashed", label = "Half Width")
plt.text(x1*1000+(halfWidth/2)*1000-0.4,diff+0.2,(str)(round(halfWidth*1000, 3))+"ms")
plt.xlim(arrayX.__getitem__(thresholdIndex-10)*1000,arrayX.__getitem__(AHPIndex+10)*1000)
plt.legend()
plt.show()