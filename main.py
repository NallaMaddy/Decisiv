#################################
# Argument setup and parsing    #
#################################
from argparse import ArgumentParser

parser = ArgumentParser()

parser.add_argument('fileName', help ='Source File Path')

arguments = parser.parse_args()

#################################
# File Processing               #
#################################
from Data_Processing_Strategy import DataProcessingStrategy, GetVinDetails

vinsFile = 'vins.csv'
vinSummaryFile = 'vin_summary.csv'

DataProcessingStrategy(arguments.fileName, vinsFile)

GetVinDetails(vinsFile, vinSummaryFile)
