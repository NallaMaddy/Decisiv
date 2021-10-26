import os
import glob
import pandas as pd
import requests

def DataProcessingStrategy(srcFileName, outFileName=None):
    ### read source excel workbook
    xl = pd.ExcelFile('decisiv’xlsx')

    ### print sheet names from the workbook
    # print(xl.sheet_names)

    ### read assets sheet into a data frame
    df_a = xl.parse('assets').drop_duplicates()

    ### read estimates sheet into a data frame
    df_e = xl.parse('estimates').drop_duplicates()

    ### read estimates line items operations sheet into a data frame
    df_el = xl.parse('estimate line items-operations').drop_duplicates()

    ### Join assets and estimates on dim_asset_id
    df_ae = df_a.merge(df_e, on='dim_asset_id')

    ### Join above data frame to line items operations
    df_agg = df_ae.merge(df_el, left_on='estimate_id', right_on='source_id')

    ### Calculate the Total Cost and Number of Operations per VIN
    df_summary = df_agg.groupby('vin').agg(CountOfOps=('operation_name', 'count'), TotalCost=('total_price', 'sum'))

    ### Export the results to CSV
    df_summary.to_csv(outFileName)


def GetVinDetails(vin_file, vin_summary = None):
    ### Base URL
    baseurl ='https://vpic.nhtsa.dot.gov/api/vehicles/DecodeVinExtended/'

    ### read VIN summary file
    df = pd.read_csv(vin_file)

    ### Open a file to write vin data
    vin_f = open(vin_summary, "a+")

    ### Loop through VINs and call API to get additional details
    for vin in df['vin']:
        full_url = baseurl + vin +'?format=json'
        resp = requests.get(full_url)
        res = resp.json()
        result = res['Results']
        res_df = pd.DataFrame(result)
        #vin_details = [vin, [res_df[res_df['Variable'] == 'Make'].Value.values[0], [res_df[res_df['Variable'] == 'Model'].Value.values[0]], [res_df[res_df['Variable'] == 'Engine Model'].Value.values[0],[res_df[res_df['Variable'] == 'Make Model'].Value.values[0]]
        #vin_f.write(vin_details)

    vin_f.close()

 '   if __name__ == '__main__':
        sourcefile = 'sample.xlsx'
        outfilename = 'summary.csv'
        vinsummary = 'vin_summary.csv'

    DataProcessingStrategy(sourcefile, outfilename)

    GetVinDetails(outfilename, vinsummary)