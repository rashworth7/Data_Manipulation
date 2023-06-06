import os
import csv
import pandas as pd
import datetime

#Converting to pandas dataframe
#Adding columns for day, month and year

def csv_to_pandas(filename):
    df = pd.read_csv(filename, sep=";")
    df.dropna(how='all', inplace=True)
    df['Date'] = pd.to_datetime(df["Date"], format="%d/%m/%Y")
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df['Year'] = df['Date'].dt.year
    return df

# == INSTRUCTIONS ==
#
# Below, you'll find lots of incomplete functions.
#
# Your job: Implement each function so that it does its job effectively.
#
# Tips:
# * Use the material, Python Docs and Google as much as you want
#
# * A warning: the data you are using may not contain quite what you expect;
#   cleaning data (or changing your program) might be necessary to cope with
#   "imperfect" data

# == EXERCISES ==

# Purpose: return a boolean, False if the file doesn't exist, True if it does
# Example:
#   Call:    does_file_exist("nonsense")
#   Returns: False
#   Call:    does_file_exist("AirQuality.csv")
#   Returns: True
# Notes:
# * Use the already imported "os" module to check whether a given filename exists
def does_file_exist(filename):
    return os.path.exists(filename)

# Purpose: get the contents of a given file and return them; if the file cannot be
# found, return a nice error message instead
# Example:
#   Call: get_file_contents("AirQuality.csv")
#   Returns:
#     Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);[...]
#     10/03/2004;18.00.00;2,6;1360;150;11,9;1046;166;1056;113;1692;1268;[...]
#     [...]
#   Call: get_file_contents("nonsense")
#   Returns: "This file cannot be found!"
# Notes:
# * Learn how to open file as read-only
# * Learn how to close files you have opened
# * Use readlines() to read the contents
# * Use should use does_file_exist()

def get_file_contents(filename):
    if does_file_exist(filename):
        file = open(filename, "r")
        contents = file.readlines()
        new_content = [line for line in contents if line.strip() != ";"] #Slightly unsure on this method. Is there a better way?
        file.close()
        return new_content
    else:
        return "This file cannot be found!"
    

# get_file_contents("../AirQuality.csv")

# Purpose: fetch Christmas Day (25th December) air quality data rows, and if
# boolean argument "include_header_row" is True, return the first header row
# from the filename as well (if it is False, omit that row)
# Example:
#   Call: christmas_day_air_quality("AirQuality.csv", True)
#   Returns:
#     Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);[...]
#     25/12/2004;00.00.00;5,9;1505;-200;15,6;1168;567;525;169;1447;[...]
#     [...]
#   Call: christmas_day_air_quality("AirQuality.csv", False)
#   Returns:
#     25/12/2004;00.00.00;5,9;1505;-200;15,6;1168;567;525;169;1447;[...]
#     [...]
# Notes:
# * should use get_file_contents() - N.B. as should any subsequent
# functions you write, using anything previously built if and where necessary
def christmas_day_air_quality(filename, include_header_row):
    if does_file_exist(filename):
        output = []
        contents = get_file_contents(filename)
        if include_header_row:
            output.append(contents[0])
        for row in contents:
            if "25/12/2004" in row:
                output.append(row)
        return output

christmas_day_air_quality("../AirQuality.csv", True)
# Purpose: fetch Christmas Day average of "PT08.S1(CO)" values to 2 decimal places
# Example:
#   Call: christmas_day_average_air_quality("AirQuality.csv")
#   Returns: 1439.21
# Data sample:
# Date;Time;CO(GT);PT08.S1(CO);NMHC(GT);C6H6(GT);PT08.S2(NMHC);NOx(GT);PT08.S3(NOx);NO2(GT);PT08.S4(NO2);PT08.S5(O3);T;RH;AH;;
# 10/03/2004;18.00.00;2,6;1360;150;11,9;1046;166;1056;113;1692;1268;13,6;48,9;0,7578;;
def christmas_day_average_air_quality(filename):
    # if does_file_exist(filename):
    #     xmas_data = christmas_day_air_quality(filename, False)
    #     print(f"Xmas data is {type(xmas_data)}")
    #     sum_air_quality = 0
    #     count = 0
    #     for row in xmas_data:
    #         count += 1
    #         row_as_list = row.split(";")
    #         sum_air_quality += int(row_as_list[3])
    #     return round(sum_air_quality / count, 2)

#Using Pandas - this seems much more effecient and easier to use - especially if you print the df

    if does_file_exist(filename):
        df = csv_to_pandas(filename)
        dec_df = df[df['Month'] == 12]
        xmas_df = dec_df[dec_df['Day'] == 25]
        average_PT08 = round(xmas_df['PT08.S1(CO)'].mean(), 2)
        return average_PT08

#print(christmas_day_average_air_quality("../AirQuality.csv"))

# Purpose: scrape all the data and calculate average values for each of the 12 months
#          for the "PT08.S1(CO)" values, returning a dictionary of keys as integer
#          representations of months and values as the averages (to 2 decimal places)
# Example:
#   Call: get_averages_for_month("AirQuality.csv")
#   Returns: {1: 1003.47, [...], 12: 948.71}
# Notes:
# * Data from months across multiple years should all be averaged together
def get_averages_for_month(filename):

    if does_file_exist(filename):
        df = pd.read_csv(filename, sep=";") #reads the csv file into pandas with the seperator as a ;
        df['Date'] = pd.to_datetime(df['Date'], format="%d/%m/%Y") #changes the date column to a datetime (like the datetime moldule)
        df['Month'] = df['Date'].dt.month # Creates a month column

        averages_dict = {}
        for month in range(1, 13):
            month_df = df[df['Month'] == month]
            average_PT08 = round(month_df['PT08.S1(CO)'].mean(), 2)
            averages_dict[month] = average_PT08
    
    return averages_dict

# get_averages_for_month("../AirQuality.csv")
# Purpose: write only the rows relating to March (any year) to a new file, in the same
# location as the original, including the header row of labels
# Example
#   Call: create_march_data("AirQuality.csv")
#   Returns: nothing, but writes header + March data to file called
#            "AirQualityMarch.csv" in same directory as "AirQuality.csv"
def create_march_data(filename):

    #Using pandas which seems a much more effecient method but it outputs the values as floats - I can't work out an effecient way to change them all to integers

    # if does_file_exist(filename):
    #     df = csv_to_pandas(filename)
    #     df_march = df[df['Month'] == 3]
    #     df_march_output = df_march.drop(columns=['Month', 'Day']).astype(int)
    #     df_march_output['Date'] = df_march_output['Date'].dt.strftime('%d/%m/%Y')
    #     df_march_output.to_csv("./Users/richardashworth/Documents/makers_challenges/python_foundations/extension_challenges/01_files/program/AirQualityMarch.csv", index=False, sep=";")

    if does_file_exist(filename):
        contents = get_file_contents(filename)
        data = [contents[0]]
        for row in contents:
            if "/03/" in row:
                data.append(row)
                
        with open("/Users/richardashworth/Documents/makers_challenges/python_foundations/extension_challenges/01_files/program/AirQualityMarch.csv", "w") as file:


            for line in data:
                file.write(line)

# Purpose: write monthly responses files to a new directory called "monthly_responses",
# in the same location as AirQuality.csv, each using the name format "mm-yyyy.csv",
# including the header row of labels in each one.
# Example
#   Call: create_monthly_responses("AirQuality.csv")
#   Returns: nothing, but files such as monthly_responses/05-2004.csv exist containing
#            data matching responses from that month and year
def create_monthly_responses(filename):
    # df = csv_to_pandas(filename)

    # df[['PT08.S1(CO)', 'NMHC(GT)', 'PT08.S2(NMHC)', 'NOx(GT)', 'PT08.S3(NOx)', 'NO2(GT)', 'PT08.S4(NO2)', 'PT08.S5(O3)']] = df[['PT08.S1(CO)', 'NMHC(GT)', 'PT08.S2(NMHC)', 'NOx(GT)', 'PT08.S3(NOx)', 'NO2(GT)', 'PT08.S4(NO2)', 'PT08.S5(O3)']].astype(int)
    # print(df)

    if does_file_exist(filename):
        os.mkdir("/Users/richardashworth/Documents/makers_challenges/python_foundations/extension_challenges/01_files/program/monthly_responses")
        contents = get_file_contents(filename)
        date = contents[1][3:10]
        data = [contents[0]]
        file_name = f"{date[:2]}-{date[3:]}"
        for row in contents[1:]: #start from one to ignore header line
            if date != row [3:10]: #if date is not the same then create a new csv with the previous date
                with open(f"/Users/richardashworth/Documents/makers_challenges/python_foundations/extension_challenges/01_files/program/monthly_responses/{file_name}.csv", 'w') as file:
                    for line in data:
                        file.write(line)
                    file.close()
                date = row[3:10]
                file_name = f"{date[:2]}-{date[3:]}"
                data = [contents[0]]
                data.append(row) #repeated a lot of code here, need to think about how I can make it more efecient
            else:
                data.append(row)
        with open(f"/Users/richardashworth/Documents/makers_challenges/python_foundations/extension_challenges/01_files/program/monthly_responses/{file_name}.csv", 'w') as file:
                    for line in data:
                        file.write(line)
                    file.close()



# create_monthly_responses("../AirQuality.csv")