# Suitability Analysis for Vector Polygon Data (SAVPD) v1.0
GEOM67_G7_Implementation
# Date last modified: Dec 4, 2020
 Authors: Matthew Archbell, Tasfia Khaled, Eric McNeill, Ramandeep Singh, Kezia Yu
# Purpose: 
This program will be used to assess suitability of vector shapefiles using the Union and 
Select tools. It is to automate the suitability analysis for habitat (or whatever phenomena the user would like)
using vector polygon input data. The relative importance of each polygon layer is represented by user inputted weights.
Finally, the program will output a new feature class containing the suitability values in a new attribute field
along with the corresponding weights of each polygon layer for reference.
# Description: 
The workspace is set to the location of the script file. User inputs shapefiles names and their weights.
Union function is computed using user inputs, and an output shapefile is created with user input name. Fields are
added for individual weights as well as a suitability index field summing these weights.
# Assumptions: 
Python script file is located in the same directory as all the shapefiles being used in the program.
# Planned Limitations: 
Certain parameters can't be customized (e.g. allow gaps is set to default). Because the
workspace is set the location of the script file, shapefiles from other directories can not be incorporated unless
they are moved to the directory of the script in advance.
# Special Cases/Known Problems: 
There is no limit to the number of shapefiles users can add for the analysis, therefore we
expect that program performance will be negatively affected once a certain number of files is reached. 
# Inputs: 
Shapefile names and associated weight value, name of the output file
# Outputs: 
Unioned shapefile with addtional fields containing weights and sutiability index
# References: 
              Calculate Field Example: https://pro.arcgis.com/en/pro-app/tool-reference/data-management/calculate-field.htm 
              Zip Example: https://www.geeksforgeeks.org/python-iterate-multiple-lists-simultaneously/
              Add Field Example: https://pro.arcgis.com/en/pro-app/tool-reference/data-management/add-field.htm
              Union Example: https://pro.arcgis.com/en/pro-app/tool-reference/analysis/union.htm
              Get Messages Example: https://pro.arcgis.com/en/pro-app/arcpy/functions/getmessages.htm
              General Inspiration: Karen Whillans 
