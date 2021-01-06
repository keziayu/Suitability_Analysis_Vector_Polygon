# Suitability Analysis for Vector Polygon Data (SAVPD) v1.0
# Date last modified: Dec 4, 2020
# Authors: Matthew Archbell, Tasfia Khaled, Eric McNeill, Ramandeep Singh, Kezia Yu
# Purpose: This program will be used to assess suitability of vector shapefiles using the Union and
# Select tools. It is to automate the suitability analysis for habitat (or whatever phenomena the user would like)
# using vector polygon input data. The relative importance of each polygon layer is represented by user inputted weights.
# Finally, the program will output a new feature class containing the suitability values in a new attribute field
# along with the corresponding weights of each polygon layer for reference.
# Description: The workspace is set to the location of the script file. User inputs shapefiles names and their weights.
# Union function is computed using user inputs, and an output shapefile is created with user input name. Fields are
# added for individual weights as well as a suitability index field summing these weights.
# Assumptions: Python script file is located in the same directory as all the shapefiles being used in the program.
# Planned Limitations: Certain parameters can't be customized (e.g. allow gaps is set to default). Because the
# workspace is set the location of the script file, shapefiles from other directories can not be incorporated unless
# they are moved to the directory of the script in advance.
# Special Cases/Known Problems: There is no limit to the number of shapefiles users can add for the analysis, therefore we
# expect that program performance will be negatively affected once a certain number of files is reached. 
# Inputs: Shapefile names and associated weight value, name of the output file
# Outputs: Unioned shapefile with addtional fields containing weights and sutiability index
# References:   Calculate Field Example: https://pro.arcgis.com/en/pro-app/tool-reference/data-management/calculate-field.htm 
#               Zip Example: https://www.geeksforgeeks.org/python-iterate-multiple-lists-simultaneously/
#               Add Field Example: https://pro.arcgis.com/en/pro-app/tool-reference/data-management/add-field.htm
#               Union Example: https://pro.arcgis.com/en/pro-app/tool-reference/analysis/union.htm
#               Get Messages Example: https://pro.arcgis.com/en/pro-app/arcpy/functions/getmessages.htm
#               General Inspiration: Karen Whillans 
# Coding contribution was equal between all members. We decided to use a collaboratrive approach whereby all members were present
# when developing ideas, writing code, and debugging.

# Import necessary modules for the program to run. Workspace set to location of this script file.
import arcpy
from arcpy import env
import os

cwd = os.getcwd() 

env.workspace = cwd

def main():
    # Introductory display messages for the user
    print("Suitability Analysis for Vector Polygon Data (SAVPD) v1.0")
    print("Welcome to SAVPD program! All inputs must be located within the directory that this program is saved to: " + cwd)
    print("The output shapefile will also be saved to this directory")
    print("-------------------------------------------------------------------------------------------------------------------")
    print("")

    # Before the user selects shapefiles for anlysis, a list is presented for them to see what is available
    print("These are the shapefiles avaialble for inclusion in the suitability analysis within the current directory: ")
    print("")
    shpList = arcpy.ListFiles("*.shp")
    for i in range(len(shpList)):
        print(shpList[i])

    print("")

    # Create empty lists to store the shapefiles that will be included in the union as well as their respective weight values
    unionList = []
    weightList = []

    # First shapefile to be used in analysis and its weight input by the user are appeneded to lists
    fc = input("Enter first shapefile name: ")
    print("")
    unionList.append(fc)
    fcWeight = float(input("Enter weight: "))
    weightList.append(fcWeight)
    print("")

    # Since a minimum of 2 shapefiles are required the next shapefile input is mandatory
    # If user specifies they want other shapefiles to participate in the analysis they may add more (as many as they desire)
    while True:
        fc = input("Enter shapefile name: ")
        print("")
        unionList.append(fc)
        fcWeight = float(input("Enter weight: "))
        weightList.append(fcWeight)
        print("")

        moreData = input("Would you like any more shapefiles to participate in the suitability anlaysis? (Y/N): ")
        print("")
        if moreData.upper() == "N":
            break

    # Display the names of the files entered as well as their weight values
    # This is simply to let the user see all of their entries
    print("")
    print("Shapefiles and respective weights for suitability analysis:")
    print("")
    print("File Name", "\t\t\t\t", "Weight")
    print("-----------------------------------------------------------------------")
    for i in range(len(unionList)):
        print("{:<41s}{:<25.2f}".format(unionList[i], weightList[i]))

    print("")

    # User specifies the name of output file that will be saved
    outputFile = input("Enter the name of the output suitability analysis file: ")

    print("")
    print("Calcualting Suitability Analysis...")
    print("")

    # Compute union function tool using the user input values stored in unionList
    # Several paramaters are set to default values
    # Add a field interatively for each shapefile input (conFID1->conFIDX where X is the number of shapefiles)
    # Add a suitability index field
    myresult = arcpy.Union_analysis(unionList, outputFile, "ONLY_FID")

    for i in range(len(unionList)):
        myresult = arcpy.AddField_management(myresult, "ConFID" + str(i + 1), "DOUBLE")

    myresult = arcpy.AddField_management(myresult, "Suitable", "DOUBLE")

    # A list of fields in the output file assigned to variable so certain elements can be extracted later
    # Two FID lists are created: fid_list contains field names of the new fields we created that will store indivual index values
    #                            fid_list2 contains field names of the Union-created fields indicating presence of polygons from each shapefile
    outputFields = arcpy.ListFields(myresult)

    fid_list = []
    for i in outputFields:
        if str(i.name).startswith("Con"):
            fid_list.append(i.name)

    fid_list2 = []
    for i in outputFields:
        if str(i.name).startswith("FID_"):
            fid_list2.append(i.name)

    # Codeblock to be used in arcpy.Calculate field tool for populating conFID (converted FID) fields
    # FIDvalue argument refers to value withn the Union-created fields whereby any value greater than -1 indicates the presence of a polygon
    # weights argument refers to the user input weights associated with each shapefile contained in the list weightList
    # expression will iteratively go through each of the conFID fields to populate individual index values
    # expression2 is created as astring of the items in fid_list and concated with characters to be suitable as an expression in the calculate field tool
    # epxression2 will sum the values of each of the now populated conFID fields
    codeblock = """def calcFID(FIDvalue, weights):
        if FIDvalue != -1:
            return weights

        else:
            return 0"""

    for (a, b, c) in zip(fid_list, fid_list2, weightList):
        expression = "calcFID(!" + b + "!," + str(c) + ")"
        arcpy.CalculateField_management(myresult, a, expression, "PYTHON3", codeblock)
        
    expression2 = str("!")
    for i in range(len(fid_list)):
        if i < len(fid_list)-1:
            expression2 = expression2 + str(fid_list[i]) + "! + !"
        else:
            expression2 = expression2 + str(fid_list[i]) + "!"

    arcpy.CalculateField_management(myresult, "Suitable", expression2, "PYTHON3")

    # Ending statement
    print("Suitability Analysis Complete")
    print("Output file: " + outputFile + " has been created in: " + cwd)

# Exception handlers for when main program is run from most specific to most general (messages printed out)
# Run program
try:

    if __name__ == "__main__":
        main()

except ValueError:
    print("Weight must be a number")
    
except arcpy.ExecuteError:
    print(arcpy.GetMessages(2))

except Exception:
    print("There was an unexpected error")