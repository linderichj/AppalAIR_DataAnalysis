
from noaaDataOutlet import dataPreProcessOutlet
from noaaDataInside import dataPreProcessInside
from sensorArduinoData import dataPreProcessSensor
from dewpoint import calcInsideTdew
from plotRh import plotRh
from plotT import plotT
from plotTdew import plotTdew


def main(): 
    dataset = 'DataSet2/'
    inputFileNoaa = 'app_20241004.csv'
    inputFileSensor = '20241004_160009UTC_WN_Inlet.csv'

    outputFileOutlet = 'reducedOutlet.csv'
    outputFileInside = 'reducedInside.csv'
    outputFileSensor = 'reducedSensor.csv'

    # dataPreProcessOutlet(dataset, inputFileNoaa, outputFileOutlet)
    # dataPreProcessInside(dataset, inputFileNoaa, outputFileInside)
    # dataPreProcessSensor(dataset, inputFileSensor, outputFileSensor)

    # calcInsideTdew(dataset, outputFileInside, outputFileOutlet, 'RH_dewpointOutlet')
    # calcInsideTdew(dataset, outputFileInside, outputFileSensor, 'RH_dewpointInlet')

    plotRh(dataset, outputFileOutlet, outputFileInside, outputFileSensor, 'plotRh.png')
    plotT(dataset, outputFileOutlet, outputFileInside, outputFileSensor, 'plotT.png')
    plotTdew(dataset, outputFileOutlet, outputFileInside, outputFileSensor, 'plotTdew.png')

main()