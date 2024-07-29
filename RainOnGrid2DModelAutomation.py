###############################################################################################
###################### Rain on Grid 2D Model Automation for South Africa ######################
###############################################################################################

#Last Updated: _June 28, 2024_

#This Python script quickens the approach to hydrological modeling by automating the Rain on
#Grid 2D model processes. Designed to streamline the setup, execution, and analysis phases,
#it leverages  computing techniques for efficiency. By automating data collection,
#model configuration, and output analysis, the script ensures consistent, accurate simulations
#across diverse South African landscapes, offering valuable insights for water resource
#management and disaster preparedness with minimal manual intervention.

#*********************************************************************************************
import os
import win32com.client
import shutil
import pyautogui
import tkinter as tk
from tkinter import filedialog, messagebox, Frame
import datetime
import time
import pandas as pd
import numpy as np
import pyperclip
import math
import win32gui
import win32con

###############################################################################################
####################################### 1. Project Setup ######################################
###############################################################################################
def run_script(area_name, input_folder, output_folder, documents_folder, projection_file, path_to_geometry,path_to_2d_flow_area, path_to_breaklines, path_to_land_use_layer, path_to_soil_layer, point_spacing_dx, point_spacing_dy, default_mannings_n, near_spacing_m, repeats, far_spacing_m, user_input_precipitation_data_var, path_to_rainfall_data, precipitation_data_time_interval, starting_time, ending_time, computation_interval, hydrograph_output_interval, mapping_output_interval, detailed_output_interval, friction_slope):
    #1.1 Create Folders
    #Get the current date and time in the specified format
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H%M")
    #Create the folder name
    folder_name = f"{current_time} {area_name}"
    #Combine the output folder path and the new folder name
    full_path = os.path.join(output_folder, folder_name)
    #Create the directory if it doesn't already exist
    if not os.path.exists(full_path):
        os.makedirs(full_path)
        print(f"Folder created: {full_path}")
    else:
        print(f"Folder already exists: {full_path}")

    input_files = os.path.join(full_path, "User Input Files")
    os.makedirs(input_files, exist_ok=True)

    #*********************************************************************************************
    #1.2 Create and Open HEC-RAS Project
    #1.2.1 Show HEC-RAS
    time.sleep(5)

    RASController = win32com.client.Dispatch("RAS631.HECRASController")
    RASController.ShowRas()

    #1.2.2 Define Project Information
    project_name = area_name + " HEC-RAS Project"
    plan_name = f"{area_name}_Plan"
    geometry_name = f"{area_name}_Geometry"
    steady_flow_name = f"{area_name}_Steady_Flow"
    unsteady_flow_name = f"{area_name}_Unsteady_Flow"
    description = f"The Simulation of 2D Rainfall at {area_name}, South Africa. (Created: {current_time})"

    #1.2.3 Create a New HEC-RAS Project
    time.sleep(5)
    #Left Click on 'File'
    pyautogui.click(18, 44)
    #Left Click on 'New Project ...'
    pyautogui.click(71, 72)
    #Select 'Documents' as the folder for your Project
    pyautogui.click(909, 91)
    #Create a New Folder under 'Documents'
    pyautogui.click(447, 653)
    time.sleep(1)
    pyautogui.click(444, 458)
    pyautogui.write(project_name)
    time.sleep(1)
    pyautogui.click(444, 495)
    time.sleep(2)
    pyautogui.click(1018, 590)
    time.sleep(1)
    #Enter text to 'Tile' box
    pyautogui.click(185, 121)
    time.sleep(1)
    pyautogui.write(project_name)
    time.sleep(1)
    #Enter text to 'File Name' box
    pyautogui.moveTo(568, 120)
    pyautogui.mouseDown()
    pyautogui.moveTo(382, 120)
    pyautogui.mouseUp()
    time.sleep(0.5)
    pyautogui.press('backspace')
    time.sleep(1)
    pyautogui.write(area_name)
    pyautogui.press('enter')
    time.sleep(1)
    #Click 'OK' and Create New Project
    pyautogui.click(1053, 630)

    #1.2.4 Set Description and SI Units
    #Add a Description
    time.sleep(1)
    pyautogui.click(121, 245)
    pyautogui.write(description)
    #Click on 'Options'
    time.sleep(1)
    pyautogui.click(199, 42)
    #Click on 'Unit Systems'
    time.sleep(1)
    pyautogui.click(250, 127)
    #Set HEC-RAS in SI Units
    time.sleep(1)
    pyautogui.click(301, 270)
    #Set as Default for New Projects
    time.sleep(1)
    pyautogui.click(364, 322)
    #Click 'OK'
    time.sleep(1)
    pyautogui.click(300, 295)

    #1.2.5 Save HEC-RAS Project
    #Click 'Save' Button
    time.sleep(1)
    pyautogui.click(53, 78)

    ###############################################################################################
    ####################################### 2. Model Setup ########################################
    ###############################################################################################
    #2.1 Geometry Setup
    #Open RAS Mapper
    time.sleep(1)
    pyautogui.click(469, 71)

    #2.1.1 Set Projection
    time.sleep(3)
    pyautogui.click(681, 16)
    #Click on 'Project'
    time.sleep(1)
    pyautogui.click(80, 38)
    #Click on 'Set Projection ...'
    time.sleep(2)
    pyautogui.click(110, 71)
    #Add Projection File Path
    time.sleep(1)
    pyautogui.click(887, 310)
    time.sleep(1)
    pyautogui.write(projection_file)
    #Click 'OK'
    time.sleep(1)
    pyautogui.press('enter')

    #2.1.2 Create New RAS Terrain
    #Right Click on 'Terrains'
    time.sleep(2)
    pyautogui.click(x=76, y=207, button='right')
    #Click on 'Create a NEW RAS Terrain'
    pyautogui.click(x=111, y=248)
    #Click on '+'
    pyautogui.click(x=544, y=389)
    time.sleep(2)
    #Click on File Path Tab
    pyautogui.click(x=1503, y=229)
    #Click on File Path Tab
    time.sleep(1)
    pyautogui.write(input_folder)
    pyautogui.press('enter')
    #Get File Name
    time.sleep(1)
    index = path_to_geometry.rfind('/')
    geometry_file_name = path_to_geometry[index + 1:]
    #Enter File Name
    time.sleep(1)
    pyautogui.click(x=594, y=927)
    pyautogui.write(geometry_file_name)
    #Click on 'Open'
    time.sleep(1)
    pyautogui.click(x=1698, y=965)
    #Click on 'Create'
    time.sleep(1)
    pyautogui.click(x=1244, y=711)

    #Run a Loop until 'Finished Unsteady Flow Simulation' appears
    while True:
        time.sleep(5)
        pyautogui.click(x=479, y=414)
        #Simulate pressing Ctrl+A to select all text in the active text box
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)  #Short pause to ensure the text is selected
        #Simulate copying the text to clipboard
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.1)  #Short pause to ensure the text is copied
        #Read the clipboard content
        text = pyperclip.paste()
        #Check if the specific phrase is in the copied text
        if 'Terrain Complete' in text:
            time.sleep(5)
            pyautogui.hotkey('alt', 'f4')
            break  #Exit the loop if the phrase is found
        else:
            #Wait for 20 seconds before checking again
            time.sleep(20)

    #2.1.3 Create a New RAS Layer: Land Cover Layer
    #Right Click on 'Map Layers'
    time.sleep(5)
    pyautogui.click(x=94, y=186, button='right')
    #Click on 'Create a New RAS Layer'
    time.sleep(1)
    pyautogui.click(x=183, y=274)
    #Click on 'Land Cover Layer'
    time.sleep(1)
    pyautogui.click(x=527, y=281)
    #Click on '+'
    time.sleep(1)
    pyautogui.click(x=543, y=274)
    #Click on File Path Tab
    time.sleep(1)
    pyautogui.click(x=1472, y=233)
    pyautogui.write(input_folder)
    pyautogui.press('enter')
    #Get File Name
    time.sleep(1)
    index = path_to_land_use_layer.rfind('/')
    land_cover_file_name = path_to_land_use_layer[index + 1:]
    #Enter File Name
    time.sleep(1)
    pyautogui.click(x=594, y=927)
    pyautogui.write(land_cover_file_name)
    #Click on 'Open'
    time.sleep(1)
    pyautogui.click(x=1698, y=965)
    #Click on 'Create'
    time.sleep(1)
    pyautogui.click(x=1250, y=834)

    #Run a Loop until 'Finished Unsteady Flow Simulation' appears
    while True:
        pyautogui.click(x=479, y=414)
        #Simulate pressing Ctrl+A to select all text in the active text box
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)  # short pause to ensure the text is selected
        #Simulate copying the text to clipboard
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.1)  # short pause to ensure the text is copied
        #Read the clipboard content
        text = pyperclip.paste()
        #Check if the specific phrase is in the copied text
        if 'Land cover Layer complete!' in text:
            time.sleep(2)
            pyautogui.hotkey('alt', 'f4')
            break  #Exit the loop if the phrase is found
        else:
            #Wait for 10 seconds before checking again
            time.sleep(2)

    #2.1.4 Create a New RAS Layer: Soils Layer
    #Right Click on 'Map Layers'
    time.sleep(2)
    pyautogui.click(x=94, y=186, button='right')
    #Click on 'Create a New RAS Layer'
    time.sleep(1)
    pyautogui.click(x=183, y=274)
    #Click on 'Soils Layer'
    time.sleep(1)
    pyautogui.click(x=531, y=301)
    #Click on '+'
    time.sleep(1)
    pyautogui.click(x=543, y=274)
    #Click on File Path Tab
    time.sleep(1)
    pyautogui.click(x=1472, y=233)
    pyautogui.write(input_folder)
    pyautogui.press("enter")
    #Get File Name
    time.sleep(1)
    index = path_to_soil_layer.rfind('/')
    soil_file_name = path_to_soil_layer[index + 1:]
    #Enter File Name
    time.sleep(1)
    pyautogui.click(x=594, y=927)
    pyautogui.write(soil_file_name)
    #Click on 'Open'
    time.sleep(1)
    pyautogui.click(x=1698, y=965)
    #Click on 'Create'
    time.sleep(1)
    pyautogui.click(x=1250, y=834)

    #Run a Loop until 'Finished Unsteady Flow Simulation' appears
    while True:
        pyautogui.click(x=479, y=414)
        #Simulate pressing Ctrl+A to select all text in the active text box
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)  # short pause to ensure the text is selected
        #Simulate copying the text to clipboard
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.1)  # short pause to ensure the text is copied
        #Read the clipboard content
        text = pyperclip.paste()
        #Check if the specific phrase is in the copied text
        if 'Land cover Layer complete!' in text:
            time.sleep(2)
            pyautogui.hotkey('alt', 'f4')
            break  #Exit the loop if the phrase is found
        else:
            #Wait for 10 seconds before checking again
            time.sleep(2)

    #Click on 'Map Layers' Check Mark
    time.sleep(2)
    pyautogui.click(x=40, y=188)
    #Expand 'Map Layers'
    time.sleep(1)
    pyautogui.click(x=16, y=187)

    #SAVE HEC-RAS PROJECT
    #Click on 'File'
    time.sleep(2)
    pyautogui.click(x=21, y=44)
    #Click on 'Save'
    time.sleep(2)
    pyautogui.click(x=46, y=95)

    #2.1.5 Add New Geometry
    #Right Click on 'Geometry'
    time.sleep(2)
    pyautogui.click(x=96, y=127, button='right')
    #Click 'Add New Geometry'
    time.sleep(1)
    pyautogui.click(x=133, y=142)
    #Enter a unique Name for the new Geometry
    time.sleep(1)
    pyautogui.write(geometry_name)
    #Click 'OK'
    time.sleep(1)
    pyautogui.click(x=1072, y=576)

    #Right Click on 'Geometry'
    time.sleep(2)
    pyautogui.click(x=107, y=143, button='right')
    #Click on 'Edit Geometry'
    time.sleep(1)
    pyautogui.click(x=253, y=201)
    #Click on '+' '2D Flow Areas'
    time.sleep(1)
    pyautogui.click(x=65, y=230)

    #2.1.6 Add 2D Flow Areas Perimeters
    #Right Click on 'Perimeters'
    time.sleep(2)
    pyautogui.click(x=137, y=242, button='right')
    time.sleep(0.5)
    pyautogui.click(x=135, y=242, button='right')
    time.sleep(0.5)
    pyautogui.click(x=133, y=242, button='right')
    #Click on 'Import Features from Shape File'
    time.sleep(2)
    pyautogui.click(x=216, y=507)
    #Click on File Path Button
    time.sleep(5)
    pyautogui.click(x=1360, y=202)
    #Click on File Path Tab
    time.sleep(1)
    pyautogui.click(x=1472, y=233)
    pyautogui.write(input_folder)
    pyautogui.press('enter')
    #Get File Name
    time.sleep(1)
    index = path_to_2d_flow_area.rfind('/')
    two_d_flow_file_name = path_to_2d_flow_area[index + 1:]
    #Enter File Name
    time.sleep(1)
    pyautogui.click(x=594, y=927)
    pyautogui.write(two_d_flow_file_name)
    #Click on 'Open'
    time.sleep(1)
    pyautogui.click(x=1698, y=965)
    #Click on 'Import'
    time.sleep(1)
    pyautogui.click(x=1247, y=844)

    #Right Click on '2D Flow Area'
    time.sleep(2)
    pyautogui.click(x=113, y=221, button='right')
    #Click on 'Open Attribute Table'
    time.sleep(2)
    pyautogui.click(x=171, y=260)
    #Click on 'Name' Attribute
    time.sleep(2)
    pyautogui.click(x=696, y=398)
    pyautogui.click(x=696, y=398)
    pyautogui.click(x=696, y=398)
    #Change Name
    time.sleep(2)
    first_four_upper = area_name[:4].upper()
    perimeter_name = first_four_upper + ' Perimeter'
    time.sleep(2)
    pyautogui.write(perimeter_name)
    pyautogui.press('enter')
    #Click on 'Close'
    time.sleep(2)
    pyautogui.hotkey('alt', 'f4')

    #2.1.7 Add 2D Flow Areas Breaklines
    #Right Click on 'Breaklines'
    time.sleep(2)
    pyautogui.click(x=137, y=281, button='right')
    time.sleep(0.5)
    pyautogui.click(x=135, y=281, button='right')
    time.sleep(0.5)
    pyautogui.click(x=133, y=281, button='right')
    #Click on 'Import Features from Shape File'
    time.sleep(2)
    pyautogui.click(x=192, y=539)
    #Click on File Path Button
    time.sleep(5)
    pyautogui.click(x=1354, y=200)
    #Click on File Path Tab
    time.sleep(1)
    pyautogui.click(x=1472, y=233)
    pyautogui.write(input_folder)
    pyautogui.press('enter')
    #Get File Name
    time.sleep(1)
    index = path_to_breaklines.rfind('/')
    breaklines_file_name = path_to_breaklines[index + 1:]
    #Enter File Name
    time.sleep(1)
    pyautogui.click(x=594, y=927)
    pyautogui.write(breaklines_file_name)
    #Click on 'Open'
    time.sleep(1)
    pyautogui.click(x=1698, y=965)
    #Click on 'Import'
    time.sleep(1)
    pyautogui.click(x=1247, y=844)

    #2.1.8 Add Boundary Conditions
    time.sleep(5)
    pyautogui.click(x=172, y=422)

    time.sleep(2)
    bc_setup__message(point_spacing_dx, point_spacing_dy, default_mannings_n, near_spacing_m, repeats, far_spacing_m)
    time.sleep(2)
    fix_all_meshes_message(user_input_precipitation_data_var)
    time.sleep(2)
    friction_slope_message(full_path, area_name, user_input_precipitation_data_var, path_to_rainfall_data, precipitation_data_time_interval, starting_time, ending_time, computation_interval, hydrograph_output_interval, mapping_output_interval, detailed_output_interval, friction_slope)
    time.sleep(2)
    computational_settings_message(full_path, input_files, project_name, area_name, projection_file, path_to_geometry, path_to_2d_flow_area, path_to_breaklines, path_to_land_use_layer, path_to_soil_layer, user_input_precipitation_data_var, path_to_rainfall_data, starting_time, ending_time)
    time.sleep(2)
    final_message()

def continue_after_bc_setup__message(point_spacing_dx, point_spacing_dy, default_mannings_n, near_spacing_m, repeats, far_spacing_m):
    #SAVE HEC-RAS PROJECT
    #Click on 'Zoom Out'
    time.sleep(2)
    pyautogui.click(x=563, y=74)
    #Click on 'File'
    time.sleep(2)
    pyautogui.click(x=21, y=44)
    #Click on 'Save'
    time.sleep(2)
    pyautogui.click(x=46, y=95)
    #Click on 'Arrow'
    time.sleep(2)
    pyautogui.click(x=501, y=70)
    pyautogui.click(x=500, y=41)

    #SAVE HEC-RAS PROJECT
    #Click on 'Zoom Out'
    time.sleep(2)
    pyautogui.click(x=563, y=74)
    #Click on 'File'
    time.sleep(2)
    pyautogui.click(x=21, y=44)
    #Click on 'Save'
    time.sleep(2)
    pyautogui.click(x=46, y=95)
    #Click on 'Arrow'
    time.sleep(2)
    pyautogui.click(x=501, y=70)
    pyautogui.click(x=500, y=41)

    #*********************************************************************************************
    #2.2 2D Flow Area Setup
    #2.2.1 Force Mesh Recomputation
    #Right Click on '2D FLow Areas'
    time.sleep(2)
    pyautogui.click(x=102, y=222, button='right')
    #Click on '2D Flow Area Editor'
    time.sleep(1)
    pyautogui.click(x=147, y=326)
    #Click on 'Points Spacing (m) DX'
    time.sleep(2)
    pyautogui.click(x=879, y=421)
    #Erase all
    for _ in range(10):
        pyautogui.press('backspace')
    #Enter Points Spacing (m) DX
    pyautogui.write(point_spacing_dx)
    #Click on 'Points Spacing (m) DY'
    time.sleep(1)
    pyautogui.click(x=972, y=420)
    #Erase all
    for _ in range(10):
        pyautogui.press('backspace')
    #Enter Points Spacing (m) DY
    pyautogui.write(point_spacing_dy)
    #Click on 'Default Manning's n Value'
    time.sleep(1)
    pyautogui.click(x=879, y=635)
    #Erase all
    for _ in range(10):
        pyautogui.press('backspace')
    #Enter Default Manning's n Value
    pyautogui.write(default_mannings_n)
    #Click on 'Generate Computation Points'
    time.sleep(5)
    pyautogui.click(x=842, y=544)
    #Click on 'Force Mesh Recomputation'
    time.sleep(25)
    pyautogui.click(x=763, y=713)
    #Click on 'Close'
    time.sleep(10)
    pyautogui.hotkey('alt', 'f4')

    #2.2.2 Edit Breakline Properties
    #Right Click on 'Breaklines'
    time.sleep(1)
    pyautogui.click(x=127, y=282, button='right')
    #Click on 'Edit Breakline Properties'
    time.sleep(2)
    pyautogui.click(x=187, y=385)

    #Click on 'Near Spacing' Column
    time.sleep(5)
    pyautogui.click(x=942, y=449)
    #Click on 'Set Value' Button
    time.sleep(1)
    pyautogui.click(x=1135, y=406)
    #Set Value
    time.sleep(1)
    pyautogui.click(x=764, y=573)
    pyautogui.write(near_spacing_m)
    #Click OK
    time.sleep(1)
    pyautogui.click(x=1118, y=470)

    #Click on 'Near Repats' Column
    time.sleep(2)
    pyautogui.click(x=1064, y=447)
    #Click on 'Set Value' Button
    time.sleep(1)
    pyautogui.click(x=1135, y=406)
    #Set Value
    time.sleep(1)
    pyautogui.click(x=764, y=573)
    pyautogui.write(repeats)
    #Click OK
    time.sleep(1)
    pyautogui.click(x=1118, y=470)

    #Click on 'Far Spacing' Column
    time.sleep(2)
    pyautogui.click(x=1200, y=450)
    #Click on 'Set Value' Button
    time.sleep(1)
    pyautogui.click(x=1135, y=406)
    #Set Value
    time.sleep(1)
    pyautogui.click(x=764, y=573)
    pyautogui.write(far_spacing_m)
    #Click OK
    time.sleep(1)
    pyautogui.click(x=1118, y=470)

    #Click 'OK'
    time.sleep(2)
    pyautogui.click(x=1185, y=639)

    #2.2.3 Regenerate Grid
    #Right Click on '2D Flow Areas'
    time.sleep(2)
    pyautogui.click(x=102, y=224, button='right')
    #Right Click on 'Force Recompute of all Meshes'
    time.sleep(1)
    pyautogui.click(x=161, y=348)

    #2.2.4 Fix All Meshes (15 Loops)
    #Click on 'Reset View' Button
    time.sleep(5)
    pyautogui.click(x=561, y=73)
    for i in range(15):
        #Right Click on 'Perimeters'
        time.sleep(2)
        pyautogui.click(x=127, y=241, button='right')
        #Click on 'Try to Fix all Meshes'
        time.sleep(1)
        pyautogui.click(x=199, y=428)
        #Click on 'OK'
        time.sleep(15)
        pyautogui.hotkey('alt', 'f4')

    #SAVE HEC-RAS PROJECT
    #Click on 'Zoom Out'
    time.sleep(2)
    pyautogui.click(x=563, y=74)
    #Click on 'File'
    time.sleep(2)
    pyautogui.click(x=21, y=44)
    #Click on 'Save'
    time.sleep(2)
    pyautogui.click(x=46, y=95)
    #Click on 'Arrow'
    time.sleep(2)
    pyautogui.click(x=501, y=70)
    pyautogui.click(x=500, y=41)

    time.sleep(2)
    pyautogui.click(x=162, y=262)

def continue_after_fix_all_meshes_message(user_input_precipitation_data_var):
    #SAVE HEC-RAS PROJECT
    #Click on 'Zoom Out'
    time.sleep(2)
    pyautogui.click(x=563, y=74)
    #Click on 'File'
    time.sleep(2)
    pyautogui.click(x=21, y=44)
    #Click on 'Save'
    time.sleep(2)
    pyautogui.click(x=46, y=95)
    #Click on 'Arrow'
    time.sleep(2)
    pyautogui.click(x=501, y=70)
    pyautogui.click(x=500, y=41)

    #CLOSE RAS MAPPER
    #Click on 'X'
    time.sleep(2)
    pyautogui.click(x=561, y=74)
    time.sleep(2)
    pyautogui.hotkey('alt', 'f4')
    #Click on 'Yes'
    time.sleep(1)
    pyautogui.click(x=923, y=612)

    ###############################################################################################
    ############################# 3. Rain on Grid 2D Model Plan Setup #############################
    ###############################################################################################
    if user_input_precipitation_data_var == '0':
        user_input_precipitation_data_var = False
    else:
        user_input_precipitation_data_var = True

    #Open 'Geometry' Window
    time.sleep(5)
    pyautogui.click(x=83, y=72)
    #Get the handle for the foreground window
    hwnd = win32gui.GetForegroundWindow()
    #Get window placement info
    placement = win32gui.GetWindowPlacement(hwnd)
    #Check if the window is not maximized (the second element in the tuple is not 2)
    if placement[1] != win32con.SW_MAXIMIZE:
        time.sleep(5)  # Wait for 2 seconds
        pyautogui.hotkey('win', 'up')  # Send 'Alt + F4' to close the window
    else:
        time.sleep(5)

    #Click on 'File' Button
    time.sleep(2)
    pyautogui.click(x=15, y=36)
    #Click on 'Open Geometry Data' Button
    time.sleep(1)
    pyautogui.click(x=61, y=92)
    #Select First Geometry File
    time.sleep(1)
    pyautogui.click(x=531, y=360)
    #Click on 'OK' Button
    time.sleep(1)
    pyautogui.click(x=1271, y=800)

    #Click on 'File' Button
    time.sleep(5)
    pyautogui.click(x=15, y=36)
    #Click on 'Save Geometry Data' Button
    time.sleep(1)
    pyautogui.click(x=51, y=118)

def continue_after_friction_slope_message(full_path, area_name, user_input_precipitation_data_var, path_to_rainfall_data, precipitation_data_time_interval, starting_time, ending_time, computation_interval, hydrograph_output_interval, mapping_output_interval, detailed_output_interval, friction_slope):
    #CLOSE Geometric Data WINDOW
    #Click on 'X'
    time.sleep(2)
    pyautogui.click(x=1385, y=7)
    time.sleep(2)
    pyautogui.hotkey('alt', 'f4')

    #3.1 Rainfall Input Setup
    #Open 'Unsteady FLow Data' Window
    time.sleep(5)
    pyautogui.click(x=183, y=70)
    #Click on Storage/2D Flow Areas
    time.sleep(1)
    pyautogui.click(x=559, y=473)
    #Click on Normal Depth
    time.sleep(1)
    pyautogui.click(x=547, y=217)
    #Click on Friction SLope Text Box
    time.sleep(1)
    pyautogui.click(x=1174, y=508)
    #Click on Friction SLope Text Box
    time.sleep(1)
    pyautogui.click(x=1174, y=508)
    #Select all Friction Slope Values
    pyautogui.dragTo(1089, 508, duration=1, button='left')
    #Backspace
    time.sleep(1)
    pyautogui.press('backspace')
    #Click on Friction SLope Text Box and add Text
    time.sleep(1)
    pyautogui.click(x=1174, y=508)
    time.sleep(1)
    pyautogui.write(friction_slope)
    #Click on 'OK' Button
    time.sleep(1)
    pyautogui.click(x=1008, y=619)

    #Click on 'Add SA/2DFlow Area...' Button
    time.sleep(5)
    pyautogui.click(x=631, y=335)
    #Select First Perimeter
    time.sleep(1)
    pyautogui.click(x=779, y=457)
    #Click on Arrow Button
    time.sleep(1)
    pyautogui.click(x=962, y=532)
    #Click on 'OK' Button
    time.sleep(1)
    pyautogui.click(x=1006, y=666)

    #Click on 'Boundary Condition' for Perimeter 1
    time.sleep(2)
    pyautogui.click(x=840, y=473)
    #Click on 'Precipitation'
    time.sleep(1)
    pyautogui.click(x=706, y=280)
    #Click on 'Fixed Start Time'
    time.sleep(2)
    pyautogui.click(x=834, y=315)

    precipitation_data_time_interval_list = ["1 Second", "2 Second", "3 Second", "4 Second", "5 Second", "6 Second",
                                             "10 Second", "12 Second", "15 Second", "20 Second", "30 Second",
                                             "1 Minute", "2 Minute", "3 Minute", "4 Minute", "5 Minute", "6 Minute",
                                             "10 Minute", "12 Minute", "15 Minute", "20 Minute", "30 Minute",
                                             "1 Hour", "2 Hour", "3 Hour", "4 Hour", "6 Hour", "8 Hour", "12 Hour",
                                             "1 Day", "1 Week", "1 Month", "1 Year"]

    if user_input_precipitation_data_var == True:
        #Choose the Precipiation Data Time Interval
        #Click to Open Combo Box
        time.sleep(2)
        pyautogui.click(x=1478, y=247)
        #Move Up
        time.sleep(1)
        pyautogui.press('up', 100)
        #Choose Precipiation Data Time Interval
        index = precipitation_data_time_interval_list.index(precipitation_data_time_interval)

        if index == 0:
            pyautogui.press('enter')
        else:
            pyautogui.press('down', index)
            time.sleep(1)
            pyautogui.press('enter')

        #Read dat File as a Data Frame
        df = pd.read_csv(path_to_rainfall_data, delimiter='\t', names=['Date', 'Simulation Time', 'Precipitation (mm)'],
                         header=None)

        #Click on 'Date' Text Box and enter Date
        precipitation_start_date = df['Date'].iloc[0]
        precipitation_start_time = df['Simulation Time'].iloc[0]

        time.sleep(1)
        pyautogui.click(x=1083, y=312)
        pyautogui.write(precipitation_start_date)
        #Click on 'Time' Text Box and enter Date
        time.sleep(1)
        pyautogui.click(x=1238, y=316)
        pyautogui.write(precipitation_start_time)

        #Create a Precipitation List
        precipitation_mm = []
        for i in range(len(df)):
            precipitation_mm.append(str(df['Precipitation (mm)'].iloc[i]))

        #Loop through list and add values to Precipitation Hydrograph
        time.sleep(1)
        pyautogui.click(x=1362, y=441)
        pyautogui.click(x=1362, y=441)
        time.sleep(2)

        for i in range(len(df)):
            if i == 0:
                time.sleep(0.5)
                pyautogui.write(precipitation_mm[0])
                pyautogui.press('enter')
                pyautogui.press('enter')
                time.sleep(0.5)
            else:
                pyautogui.write(precipitation_mm[i])
                pyautogui.press('enter')
    else:
        #Set the total rainfall and the duration of the hyetograph
        total_rainfall = 120  # in mm
        duration = 24  # in hours
        num_intervals = duration * 12  # 5-minute intervals
        #SCS Type 3 distribution percentages for 24 hours spread across 5-minute intervals
        #Assuming we stretch the standard hourly distribution to a finer scale
        hourly_distribution = np.array(
            [0.01, 0.02, 0.03, 0.05, 0.07, 0.09, 0.11, 0.12, 0.10, 0.08, 0.07, 0.05, 0.04, 0.03, 0.02, 0.01])
        #Stretch the hourly distribution to the 5-minute distribution
        distribution_percentages = np.repeat(hourly_distribution, num_intervals // len(hourly_distribution))
        #Ensure the percentages sum to 1
        distribution_percentages = distribution_percentages / distribution_percentages.sum()
        #Calculate the rainfall for each interval
        rainfall_amounts = total_rainfall * distribution_percentages
        #Generate the time intervals
        intervals = pd.date_range(start="00:00", periods=num_intervals, freq="5T")
        #Create DataFrame
        df = pd.DataFrame({
            'Date': [interval.strftime('%d%b%Y').upper() for interval in intervals],
            'Time': [interval.strftime('%H%M') for interval in intervals],
            'Precipitation (mm)': rainfall_amounts
        })
        scs_precipitation_start_date = df['Date'].iloc[0]
        scs_precipitation_start_time = df['Time'].iloc[0]
        scs_precipitation_data_time_interval = '5 Minute'
        #Save DataFrame as.dat File
        df.to_csv(f"{full_path}/{area_name} SA SCS T3 (120mm).dat", sep='\t', index=False)

        #Click on 'Date' Text Box and enter Date
        time.sleep(1)
        pyautogui.click(x=1083, y=312)
        pyautogui.write(scs_precipitation_start_date)
        #Click on 'Time' Text Box and enter Date
        time.sleep(1)
        pyautogui.click(x=1238, y=316)
        pyautogui.write(scs_precipitation_start_time)

        #Choose the Precipiation Data Time Interval
        #Click to Open Combo Box
        time.sleep(2)
        pyautogui.click(x=1478, y=247)
        #Move Up
        time.sleep(1)
        pyautogui.press('up', 100)
        #Choose Precipiation Data Time Interval
        index = precipitation_data_time_interval_list.index(scs_precipitation_data_time_interval)

        if index == 0:
            pyautogui.press('enter')
        else:
            pyautogui.press('down', index)
            time.sleep(1)
            pyautogui.press('enter')

        #Create a Precipitation List
        precipitation_mm = []
        for i in range(len(df)):
            precipitation_mm.append(str(df['Precipitation (mm)'].iloc[i]))

        #Change No. Ordinates
        time.sleep(2)
        pyautogui.click(x=859, y=347)
        time.sleep(2)
        pyautogui.click(x=857, y=438)
        pyautogui.press('backspace', 50)
        time.sleep(2)
        pyautogui.write(str(len(df)))
        time.sleep(2)
        pyautogui.press('enter')

        #Loop through list and add values to Precipitation Hydrograph
        time.sleep(2)
        pyautogui.click(x=1362, y=441)
        pyautogui.click(x=1362, y=441)
        time.sleep(2)

        for i in range(len(df)):
            if i == 0:
                time.sleep(0.5)
                pyautogui.write(precipitation_mm[0])
                pyautogui.press('enter')
                pyautogui.press('enter')
                time.sleep(0.5)
            else:
                pyautogui.write(precipitation_mm[i])
                pyautogui.press('enter')

    #Click on 'Plot Data'
    time.sleep(2)
    pyautogui.click(x=1218, y=847)
    #Click on 'Table'
    time.sleep(5)
    pyautogui.click(x=1796, y=153)

    #Open Screenshot
    time.sleep(3)
    pyautogui.hotkey('win', 'shift', 's')
    #Create Window to Screenshot
    time.sleep(3)
    pyautogui.moveTo(3, 58)
    time.sleep(0.2)
    pyautogui.dragTo(1916, 1017, button='left', duration=2)

    #Give a little delay for the script to run safely
    time.sleep(5)
    #Press the Windows key
    pyautogui.press('win')
    time.sleep(2)
    #Type 'File Explorer' into the search box
    pyautogui.write('File Explorer')
    #Press Enter to open File Explorer
    pyautogui.press('enter')
    #Maximise Window
    #Get the handle for the foreground window
    hwnd = win32gui.GetForegroundWindow()
    #Get window placement info
    placement = win32gui.GetWindowPlacement(hwnd)
    #Check if the window is not maximized (the second element in the tuple is not 2)
    if placement[1] != win32con.SW_MAXIMIZE:
        time.sleep(5)  #Wait for 2 seconds
        pyautogui.hotkey('win', 'up')  #Send 'Alt + F4' to close the window
    else:
        time.sleep(5)
    #Click on "File Path" Bar
    time.sleep(2)
    pyautogui.click(x=1292, y=64)
    pyautogui.write('Pictures\Screenshots')
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.click(x=1292, y=64)
    pyautogui.hotkey('ctrl', 'c')
    screenshot_path = pyperclip.paste()

    time.sleep(2)
    #Assuming the newest screenshot is the one you want to rename and move
    #Find the latest file in the folder based on creation time
    latest_file = max([os.path.join(screenshot_path, f) for f in os.listdir(screenshot_path)], key=os.path.getctime)
    #New file name construction
    new_filename = f"{area_name} Time Series Graph.png"
    new_file_path = os.path.join(screenshot_path, new_filename)
    #Rename the file
    os.rename(latest_file, new_file_path)
    #Copy the new file to the destination folder
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    shutil.copy(new_file_path, full_path)
    #Delete the original screenshot
    os.remove(new_file_path)

    time.sleep(10)
    #Click on 'X'
    time.sleep(2)
    pyautogui.click(x=1318, y=14)
    time.sleep(2)
    pyautogui.hotkey('alt', 'f4')

    #Click on 'X'
    time.sleep(2)
    pyautogui.click(x=1318, y=14)
    time.sleep(2)
    pyautogui.hotkey('alt', 'f4')

    #Click on 'OK' Button
    time.sleep(2)
    pyautogui.click(x=1321, y=848)

    #Click on 'File' Button
    time.sleep(2)
    pyautogui.click(x=465, y=44)
    #Click on 'Save Unsteady Flow Data' Button
    time.sleep(1)
    pyautogui.click(x=536, y=132)
    #Click on TextBox
    time.sleep(1)
    pyautogui.click(x=35, y=120)
    unsteady_flow_plan_name = area_name + ' Unsteady Flow Data'
    pyautogui.write(unsteady_flow_plan_name)
    #Click 'OK'
    time.sleep(1)
    pyautogui.click(x=79, y=652)
    #Exit 'Unsteady Flow Data' Window
    time.sleep(2)
    pyautogui.hotkey('alt', 'f4')

    #*********************************************************************************************
    #3.2 Simulation Settings Setup
    #Click on 'Unsteady Flow Analysis' Button
    time.sleep(2)
    pyautogui.click(x=324, y=72)
    #Click on 'Geometry Preprocessor' Check Box
    time.sleep(1)
    pyautogui.click(x=624, y=400)
    #Click on 'Unsteady Flow Simulation' Check Box
    pyautogui.click(x=624, y=421)
    #Click on 'Post Processor' Check Box
    pyautogui.click(x=624, y=458)
    #Click on 'Floodplain Mapping' Check Box
    pyautogui.click(x=621, y=501)

    #Click on Simulation Time Window >> Starting Date and add Text
    starting_date = df['Date'].iloc[0]

    time.sleep(2)
    pyautogui.click(x=804, y=548)
    pyautogui.write(starting_date)
    #Click on Simulation Time Window >> Ending Date and add Text
    ending_date = df['Date'].iloc[-1]

    time.sleep(1)
    pyautogui.click(x=813, y=575)
    pyautogui.write(ending_date)
    #Click on Simulation Time Window >> Starting Time and add Text
    time.sleep(1)
    pyautogui.click(x=1155, y=546)
    pyautogui.write(starting_time)
    #Click on Simulation Time Window >> Ending Time and add Text
    time.sleep(1)
    pyautogui.click(x=1158, y=577)
    pyautogui.write(ending_time)

    #Click on Short ID Text Box and add Text
    time.sleep(2)
    pyautogui.click(x=1041, y=297)
    first_four_upper = area_name[:4].upper()
    short_id = first_four_upper + ' Flow'
    pyautogui.write(short_id)

    computation_interval_list = ["0.1 Second", "0.2 Second", "0.3 Second", "0.4 Second", "0.5 Second",
                                 "1 Second", "2 Second", "3 Second", "4 Second", "5 Second", "6 Second",
                                 "10 Second", "12 Second", "15 Second", "20 Second", "30 Second",
                                 "1 Minute", "2 Minute", "3 Minute", "4 Minute", "5 Minute", "6 Minute",
                                 "10 Minute", "12 Minute", "15 Minute", "20 Minute", "30 Minute",
                                 "1 Hour", "2 Hour", "3 Hour", "4 Hour", "6 Hour", "8 Hour", "12 Hour", "1 Day"]

    #Choose the Precipiation Data Time Interval
    #Click to Open Combo Box
    time.sleep(2)
    pyautogui.click(x=884, y=623)
    #Move Up
    time.sleep(1)
    pyautogui.press('up', 100)
    #Choose Precipiation Data Time Interval
    index = computation_interval_list.index(computation_interval)

    if index == 0:
        pyautogui.press('enter')
    else:
        pyautogui.press('down', index)
        time.sleep(1)
        pyautogui.press('enter')

    hydrograph_output_interval_list = ["1 Second", "2 Second", "3 Second", "4 Second", "5 Second", "6 Second",
                                       "10 Second", "12 Second", "15 Second", "20 Second", "30 Second",
                                       "1 Minute", "2 Minute", "3 Minute", "4 Minute", "5 Minute", "6 Minute",
                                       "10 Minute", "12 Minute", "15 Minute", "20 Minute", "30 Minute",
                                       "1 Hour", "2 Hour", "3 Hour", "4 Hour", "6 Hour", "8 Hour", "12 Hour",
                                       "1 Day", "1 Week", "1 Month", "1 Year"]

    #Choose the Hydrograph Ouput Interval
    #Click to Open Combo Box
    time.sleep(2)
    pyautogui.click(x=1207, y=624)
    #Move Up
    time.sleep(1)
    pyautogui.press('up', 100)
    #Choose Hydrograph Ouput Interval
    index = hydrograph_output_interval_list.index(hydrograph_output_interval)

    if index == 0:
        pyautogui.press('enter')
    else:
        pyautogui.press('down', index)
        time.sleep(1)
        pyautogui.press('enter')

    mapping_output_interval_list = ["Max Profile", "0.1 Second", "0.2 Second", "0.3 Second", "0.4 Second", "0.5 Second",
                                    "1 Second", "2 Second", "3 Second", "4 Second", "5 Second", "6 Second",
                                    "10 Second", "12 Second", "15 Second", "20 Second", "30 Second",
                                    "1 Minute", "2 Minute", "3 Minute", "4 Minute", "5 Minute", "6 Minute",
                                    "10 Minute", "12 Minute", "15 Minute", "20 Minute", "30 Minute",
                                    "1 Hour", "2 Hour", "3 Hour", "4 Hour", "6 Hour", "8 Hour", "12 Hour",
                                    "1 Day", "1 Week", "1 Month", "1 Year"]

    #Choose the Mapping Output Interval
    #Click to Open Combo Box
    time.sleep(2)
    pyautogui.click(x=883, y=650)
    #Move Up
    time.sleep(1)
    pyautogui.press('up', 100)
    #Choose Hydrograph Ouput Interval
    index = mapping_output_interval_list.index(mapping_output_interval)

    if index == 0:
        pyautogui.press('enter')
    else:
        pyautogui.press('down', index)
        time.sleep(1)
        pyautogui.press('enter')

    detailed_output_interval_list = ["Max Profile", "1 Second", "2 Second", "3 Second", "4 Second", "5 Second",
                                     "6 Second",
                                     "10 Second", "12 Second", "15 Second", "20 Second", "30 Second",
                                     "1 Minute", "2 Minute", "3 Minute", "4 Minute", "5 Minute", "6 Minute",
                                     "10 Minute", "12 Minute", "15 Minute", "20 Minute", "30 Minute",
                                     "1 Hour", "2 Hour", "3 Hour", "4 Hour", "6 Hour", "8 Hour", "12 Hour",
                                     "1 Day", "1 Week", "1 Month", "1 Year"]

    #Choose the Detailed Output Interval
    #Click to Open Combo Box
    time.sleep(2)
    pyautogui.click(x=1206, y=649)
    #Move Up
    time.sleep(1)
    pyautogui.press('up', 100)
    #Choose Detailed Ouput Interval
    index = detailed_output_interval_list.index(detailed_output_interval)

    if index == 0:
        pyautogui.press('enter')
    else:
        pyautogui.press('down', index)
        time.sleep(1)
        pyautogui.press('enter')

    #Click on 'File' Button
    time.sleep(2)
    pyautogui.click(x=614, y=265)
    #CLick on 'Save Plan' Button
    time.sleep(1)
    pyautogui.click(x=651, y=349)
    #CLick on 'Title' Text Box and add Text
    time.sleep(1)
    pyautogui.click(x=40, y=119)
    plan_data_rename = area_name + ' Unsteady Flow Plan Data'
    pyautogui.write(plan_data_rename)
    #CLick on 'OK' Button
    time.sleep(1)
    pyautogui.click(x=74, y=655)
    #CLick on 'OK' Button
    time.sleep(1)
    pyautogui.click(x=897, y=612)

def continue_after_computational_settings_message(full_path, input_files, documents_folder_path, project_name, area_name, projection_file, path_to_geometry, path_to_2d_flow_area, path_to_breaklines, path_to_land_use_layer, path_to_soil_layer, user_input_precipitation_data_var, path_to_rainfall_data, starting_time, ending_time):
    ###############################################################################################
    ####################################### 4. Run the Model ######################################
    ###############################################################################################
    #4.1 Run the Model
    #Click on 'File' Button
    global path_to_rainfall_data_rename
    time.sleep(2)
    pyautogui.click(x=614, y=265)
    #CLick on 'Save Plan' Button
    time.sleep(1)
    pyautogui.click(x=651, y=349)

    #CLick on 'Compute' Button
    time.sleep(5)
    pyautogui.click(x=914, y=792)

    #Run a Loop until 'Finished Unsteady Flow Simulation' appears
    while True:
        pyautogui.click(x=1154, y=613)
        #Simulate pressing Ctrl+A to select all text in the active text box
        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)  # short pause to ensure the text is selected
        #Simulate copying the text to clipboard
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(0.1)  # short pause to ensure the text is copied
        #Read the clipboard content
        text = pyperclip.paste()
        #Check if the specific phrase is in the copied text
        if 'Finished Unsteady Flow Simulation' in text:
            time.sleep(5)
            pyautogui.click(x=1856, y=989)
            break  #Exit the loop if the phrase is found
        else:
            #Wait for 10 seconds before checking again
            time.sleep(10)

    #Close 'Unsteady Flow Analysis' Window
    time.sleep(2)
    pyautogui.click(x=918, y=240)
    time.sleep(1)
    pyautogui.hotkey('alt', 'f4')

    #Save HEC-RAS Project
    time.sleep(2)
    pyautogui.click(x=139, y=10)
    time.sleep(1)
    pyautogui.click(x=49, y=71)

    #*********************************************************************************************
    #4.2 Display User Inputs and Model Outputs
    #Open RAS Mapper
    time.sleep(2)
    pyautogui.click(x=471, y=71)

    #Adjust View
    time.sleep(10)
    pyautogui.click(x=563, y=73)
    #Click on '+' Button for Results
    time.sleep(2)
    pyautogui.click(x=16, y=267)
    #Select 'xxxx Flow' Tick Box
    time.sleep(1)
    pyautogui.click(x=64, y=286)

    #Click on 'Geometry' to deselect view option
    time.sleep(2)
    pyautogui.click(x=38, y=126)
    #Click on 'Map Layers' to deselect view option
    time.sleep(2)
    pyautogui.click(x=38, y=406)

    #4.2.1 Save Depth Layer Output
    #Select 'Depth (Max)' Tick Box
    time.sleep(2)
    pyautogui.click(x=87, y=346)
    #Click on 'Depth (Max)' Layer
    time.sleep(2)
    pyautogui.click(x=111, y=342)

    #Change Colour Scale of Depth
    #Right Click on 'Depth'
    time.sleep(2)
    pyautogui.click(x=111, y=341, button='right')
    #Click on 'Layer Properties'
    time.sleep(2)
    pyautogui.click(x=164, y=353)
    #Click on 'Edit Surface'
    time.sleep(2)
    pyautogui.click(x=935, y=468)
    #Click on 'Max' Textbox, backspace values and enter '3.00'
    time.sleep(2)
    pyautogui.click(x=812, y=313)
    time.sleep(2)
    pyautogui.write(['backspace'] * 50)
    time.sleep(1)
    pyautogui.write('3.00')
    #Click on 'Max' Textbox, backspace values and enter '3.00'
    time.sleep(2)
    pyautogui.click(x=814, y=344)
    time.sleep(2)
    pyautogui.write(['backspace'] * 50)
    time.sleep(1)
    pyautogui.write('0.00')
    #Click 'Create Ramp Values'
    time.sleep(1)
    pyautogui.click(x=1125, y=336)
    #Click 'OK'
    time.sleep(2)
    pyautogui.click(x=1065, y=834)
    #Close 'Layer Properties' Window
    time.sleep(2)
    pyautogui.click(x=946, y=239)
    pyautogui.hotkey('alt', 'f4')

    #Open Screenshot
    time.sleep(2)
    pyautogui.hotkey('win', 'shift', 's')
    #Click on 'Screen Recorder'
    time.sleep(2)
    pyautogui.click(x=909, y=29)
    #Create Window to Screenshot
    time.sleep(3)
    pyautogui.moveTo(489, 100)
    time.sleep(0.2)
    pyautogui.dragTo(1915, 1008, button='left', duration=2)
    #Mute Computer
    time.sleep(1)
    pyautogui.click(x=1054, y=40)
    #Start Screen Recording
    time.sleep(1)
    pyautogui.click(x=845, y=39)
    #Play the Animation
    time.sleep(4)
    pyautogui.click(x=1799, y=78)
    pyautogui.moveTo(x=1799, y=8)
    #Stop Recording
    n_seconds = math.ceil((((int(ending_time) - int(starting_time) + 100) / 100) / 3) + 1)
    time.sleep(n_seconds)
    pyautogui.click(x=875, y=39)

    #Save Animation
    time.sleep(2)
    pyautogui.click(x=1235, y=20)
    pyautogui.hotkey('ctrl', 's')

    #Save Animation as...File Name
    time.sleep(2)
    pyautogui.write(['backspace'] * 100)
    time.sleep(2)
    depth_animation_name = area_name + ' Depth Animation.mp4'
    pyautogui.write(depth_animation_name)
    #Save Animation as...Folder Path
    time.sleep(1)
    pyautogui.click(x=1182, y=101)
    pyautogui.write(full_path)
    time.sleep(1)
    pyautogui.hotkey('enter')
    time.sleep(1)
    #Click Save
    time.sleep(2)
    pyautogui.click(x=1230, y=597)
    pyautogui.hotkey('alt', 's')
    #Close Screen Recording Window
    time.sleep(2)
    pyautogui.click(x=1235, y=20)
    pyautogui.hotkey('alt', 'f4')

    #Click on 'Min' Button
    time.sleep(2)
    pyautogui.click(x=1003, y=72)

    #Open Screenshot
    time.sleep(2)
    pyautogui.hotkey('win', 'shift', 's')
    #Create Window to Screenshot
    time.sleep(3)
    pyautogui.moveTo(489, 100)
    time.sleep(0.2)
    pyautogui.dragTo(1915, 1008, button='left', duration=2)

    #Give a little delay for the script to run safely
    time.sleep(5)
    #Press the Windows key
    pyautogui.press('win')
    time.sleep(2)
    #Type 'File Explorer' into the search box
    pyautogui.write('File Explorer')
    #Press Enter to open File Explorer
    pyautogui.press('enter')
    #Maximise Window
    #Get the handle for the foreground window
    hwnd = win32gui.GetForegroundWindow()
    #Get window placement info
    placement = win32gui.GetWindowPlacement(hwnd)
    #Check if the window is not maximized (the second element in the tuple is not 2)
    if placement[1] != win32con.SW_MAXIMIZE:
        time.sleep(5)  # Wait for 2 seconds
        pyautogui.hotkey('win', 'up')  # Send 'Alt + F4' to close the window
    else:
        time.sleep(5)
    #Click on "File Path" Bar
    time.sleep(4)
    pyautogui.click(x=1292, y=64)
    pyautogui.write('Pictures\Screenshots')
    pyautogui.press('enter')
    time.sleep(4)
    pyautogui.click(x=1292, y=64)
    pyautogui.hotkey('ctrl', 'c')
    screenshot_path = pyperclip.paste()

    time.sleep(4)
    #Assuming the newest screenshot is the one you want to rename and move
    #Find the latest file in the folder based on creation time
    latest_file = max([os.path.join(screenshot_path, f) for f in os.listdir(screenshot_path)], key=os.path.getctime)
    #New file name construction
    new_filename = f"{area_name} Min Depth.png"
    new_file_path = os.path.join(screenshot_path, new_filename)
    #Rename the file
    os.rename(latest_file, new_file_path)
    #Copy the new file to the destination folder
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    shutil.copy(new_file_path, os.path.join(full_path, new_filename))
    #Delete the original screenshot
    os.remove(new_file_path)

    #Click on 'X'
    time.sleep(2)
    pyautogui.click(x=1318, y=14)
    time.sleep(2)
    pyautogui.hotkey('alt', 'f4')

    #Click on 'Max' Button
    time.sleep(2)
    pyautogui.click(x=957, y=73)

    #Open Screenshot
    time.sleep(2)
    pyautogui.hotkey('win', 'shift', 's')
    #Create Window to Screenshot
    time.sleep(3)
    pyautogui.moveTo(489, 100)
    time.sleep(0.2)
    pyautogui.dragTo(1915, 1008, button='left', duration=2)

    #Give a little delay for the script to run safely
    time.sleep(5)
    #Press the Windows key
    pyautogui.press('win')
    time.sleep(2)
    #Type 'File Explorer' into the search box
    pyautogui.write('File Explorer')
    #Press Enter to open File Explorer
    pyautogui.press('enter')
    #Click on "File Path" Bar
    time.sleep(4)
    pyautogui.click(x=1292, y=64)
    pyautogui.write('Pictures\Screenshots')
    pyautogui.press('enter')
    time.sleep(4)
    pyautogui.click(x=1292, y=64)
    pyautogui.hotkey('ctrl', 'c')
    screenshot_path = pyperclip.paste()

    time.sleep(4)
    #Assuming the newest screenshot is the one you want to rename and move
    #Find the latest file in the folder based on creation time
    latest_file = max([os.path.join(screenshot_path, f) for f in os.listdir(screenshot_path)], key=os.path.getctime)
    #New file name construction
    new_filename = f"{area_name} Max Depth.png"
    new_file_path = os.path.join(screenshot_path, new_filename)
    #Rename the file
    os.rename(latest_file, new_file_path)
    #Copy the new file to the destination folder
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    shutil.copy(new_file_path, os.path.join(full_path, new_filename))
    #Delete the original screenshot
    os.remove(new_file_path)

    #Click on 'X'
    time.sleep(2)
    pyautogui.click(x=1318, y=14)
    time.sleep(2)
    pyautogui.hotkey('alt', 'f4')

    #4.2.2 Save Velocity Layer Output
    #Select 'Velocity (Max)' Tick Box
    time.sleep(2)
    pyautogui.click(x=87, y=345)
    pyautogui.click(x=86, y=369)
    #Click on 'Velocity (Max)' Layer
    time.sleep(2)
    pyautogui.click(x=121, y=366)
    #Reset 'Play Animation' Bar
    for i in range(50):
        pyautogui.click(x=1042, y=74)

    #Change Colour Scale of Depth
    #Right Click on 'Velocity'
    time.sleep(2)
    pyautogui.click(x=110, y=362, button='right')
    #Click on 'Layer Properties'
    time.sleep(2)
    pyautogui.click(x=169, y=377)
    #Click on 'Edit Surface'
    time.sleep(2)
    pyautogui.click(x=935, y=468)
    #Click on 'Max' Textbox, backspace values and enter '3.00'
    time.sleep(2)
    pyautogui.click(x=812, y=313)
    time.sleep(2)
    pyautogui.write(['backspace'] * 50)
    time.sleep(1)
    pyautogui.write('3.00')
    #Click on 'Max' Textbox, backspace values and enter '3.00'
    time.sleep(2)
    pyautogui.click(x=814, y=344)
    time.sleep(2)
    pyautogui.write(['backspace'] * 50)
    time.sleep(1)
    pyautogui.write('0.00')
    #Click 'Create Ramp Values'
    time.sleep(1)
    pyautogui.click(x=1125, y=336)
    #Click 'OK'
    time.sleep(2)
    pyautogui.click(x=1065, y=834)
    #Close 'Layer Properties' Window
    time.sleep(2)
    pyautogui.click(x=946, y=239)
    pyautogui.hotkey('alt', 'f4')

    #Open Screenshot
    time.sleep(2)
    pyautogui.hotkey('win', 'shift', 's')
    #Click on 'Screen Recorder'
    time.sleep(2)
    pyautogui.click(x=909, y=29)
    #Create Window to Screenshot
    time.sleep(3)
    pyautogui.moveTo(489, 100)
    time.sleep(0.2)
    pyautogui.dragTo(1915, 1008, button='left', duration=2)
    #Mute Computer
    time.sleep(1)
    pyautogui.click(x=1054, y=40)
    #Start Screen Recording
    time.sleep(1)
    pyautogui.click(x=845, y=39)
    #Play the Animation
    time.sleep(4)
    pyautogui.click(x=1799, y=78)
    pyautogui.moveTo(x=1799, y=8)
    #Stop Recording
    n_seconds = math.ceil((((int(ending_time) - int(starting_time) + 100) / 100) / 3) + 1)
    time.sleep(n_seconds)
    pyautogui.click(x=875, y=39)

    #Save Animation
    time.sleep(2)
    pyautogui.click(x=1235, y=20)
    pyautogui.hotkey('ctrl', 's')

    #Save Animation as...File Name
    time.sleep(2)
    pyautogui.write(['backspace'] * 100)
    time.sleep(2)
    depth_animation_name = area_name + ' Velocity Animation.mp4'
    pyautogui.write(depth_animation_name)
    #Save Animation as...Folder Path
    time.sleep(1)
    pyautogui.click(x=1182, y=101)
    pyautogui.write(full_path)
    time.sleep(1)
    pyautogui.hotkey('enter')
    time.sleep(1)
    #Click Save
    time.sleep(2)
    pyautogui.click(x=1230, y=597)
    pyautogui.hotkey('alt', 's')
    #Close Screen Recording Window
    time.sleep(2)
    pyautogui.click(x=1235, y=20)
    pyautogui.hotkey('alt', 'f4')

    #Click on 'Min' Button
    time.sleep(2)
    pyautogui.click(x=1003, y=72)

    #Open Screenshot
    time.sleep(2)
    pyautogui.hotkey('win', 'shift', 's')
    #Create Window to Screenshot
    time.sleep(3)
    pyautogui.moveTo(489, 100)
    time.sleep(0.2)
    pyautogui.dragTo(1915, 1008, button='left', duration=2)

    #Give a little delay for the script to run safely
    time.sleep(5)
    #Press the Windows key
    pyautogui.press('win')
    time.sleep(2)
    #Type 'File Explorer' into the search box
    pyautogui.write('File Explorer')
    #Press Enter to open File Explorer
    pyautogui.press('enter')
    #Click on "File Path" Bar
    time.sleep(4)
    pyautogui.click(x=1292, y=64)
    pyautogui.write('Pictures\Screenshots')
    pyautogui.press('enter')
    time.sleep(4)
    pyautogui.click(x=1292, y=64)
    pyautogui.hotkey('ctrl', 'c')
    screenshot_path = pyperclip.paste()

    time.sleep(4)
    #Assuming the newest screenshot is the one you want to rename and move
    #Find the latest file in the folder based on creation time
    latest_file = max([os.path.join(screenshot_path, f) for f in os.listdir(screenshot_path)], key=os.path.getctime)
    #New file name construction
    new_filename = f"{area_name} Min Velocity.png"
    new_file_path = os.path.join(screenshot_path, new_filename)
    #Rename the file
    os.rename(latest_file, new_file_path)
    #Copy the new file to the destination folder
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    shutil.copy(new_file_path, os.path.join(full_path, new_filename))
    #Delete the original screenshot
    os.remove(new_file_path)

    #Click on 'X'
    time.sleep(2)
    pyautogui.click(x=1318, y=14)
    time.sleep(2)
    pyautogui.hotkey('alt', 'f4')

    #Click on 'Max' Button
    time.sleep(2)
    pyautogui.click(x=957, y=73)

    #Open Screenshot
    time.sleep(2)
    pyautogui.hotkey('win', 'shift', 's')
    #Create Window to Screenshot
    time.sleep(3)
    pyautogui.moveTo(489, 100)
    time.sleep(0.2)
    pyautogui.dragTo(1915, 1008, button='left', duration=2)

    #Give a little delay for the script to run safely
    time.sleep(5)
    #Press the Windows key
    pyautogui.press('win')
    time.sleep(2)
    #Type 'File Explorer' into the search box
    pyautogui.write('File Explorer')
    #Press Enter to open File Explorer
    pyautogui.press('enter')
    #Click on "File Path" Bar
    time.sleep(4)
    pyautogui.click(x=1292, y=64)
    pyautogui.write('Pictures\Screenshots')
    pyautogui.press('enter')
    time.sleep(4)
    pyautogui.click(x=1292, y=64)
    pyautogui.hotkey('ctrl', 'c')
    screenshot_path = pyperclip.paste()

    time.sleep(4)
    #Assuming the newest screenshot is the one you want to rename and move
    #Find the latest file in the folder based on creation time
    latest_file = max([os.path.join(screenshot_path, f) for f in os.listdir(screenshot_path)], key=os.path.getctime)
    #New file name construction
    new_filename = f"{area_name} Max Velocity.png"
    new_file_path = os.path.join(screenshot_path, new_filename)
    #Rename the file
    os.rename(latest_file, new_file_path)
    #Copy the new file to the destination folder
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    shutil.copy(new_file_path, os.path.join(full_path, new_filename))
    #Delete the original screenshot
    os.remove(new_file_path)

    #Click on 'X'
    time.sleep(2)
    pyautogui.click(x=1318, y=14)
    time.sleep(2)
    pyautogui.hotkey('alt', 'f4')

    #4.2.3 Save WSE Layer Output
    #Select 'WSE (Max)' Tick Box
    time.sleep(2)
    pyautogui.click(x=86, y=369)
    pyautogui.click(x=85, y=386)
    #Click on 'WSE (Max)' Layer
    time.sleep(2)
    pyautogui.click(x=133, y=382)
    #Reset 'Play Animation' Bar
    for i in range(50):
        pyautogui.click(x=1042, y=74)

    #Change Colour Scale of Depth
    #Right Click on 'WSE'
    time.sleep(2)
    pyautogui.click(x=113, y=381, button='right')
    #Click on 'Layer Properties'
    time.sleep(2)
    pyautogui.click(x=174, y=398)
    #Click on 'Edit Surface'
    time.sleep(2)
    pyautogui.click(x=935, y=468)
    #Click on 'No.Values' Textbox, backspace values and enter '14.00'
    time.sleep(2)
    pyautogui.click(x=950, y=346)
    time.sleep(2)
    pyautogui.write(['backspace'] * 50)
    time.sleep(1)
    pyautogui.write('14')
    #Click 'Create Ramp Values'
    time.sleep(1)
    pyautogui.click(x=1125, y=336)
    #Click 'OK'
    time.sleep(2)
    pyautogui.click(x=1065, y=834)
    #Close 'Layer Properties' Window
    time.sleep(2)
    pyautogui.click(x=946, y=239)
    pyautogui.hotkey('alt', 'f4')

    #Open Screenshot
    time.sleep(2)
    pyautogui.hotkey('win', 'shift', 's')
    #Click on 'Screen Recorder'
    time.sleep(2)
    pyautogui.click(x=909, y=29)
    #Create Window to Screenshot
    time.sleep(3)
    pyautogui.moveTo(489, 100)
    time.sleep(0.2)
    pyautogui.dragTo(1915, 1008, button='left', duration=2)
    #Mute Computer
    time.sleep(1)
    pyautogui.click(x=1054, y=40)
    #Start Screen Recording
    time.sleep(1)
    pyautogui.click(x=845, y=39)
    #Play the Animation
    time.sleep(4)
    pyautogui.click(x=1799, y=78)
    pyautogui.moveTo(x=1799, y=8)
    #Stop Recording
    n_seconds = math.ceil((((int(ending_time) - int(starting_time) + 100) / 100) / 3) + 1)
    time.sleep(n_seconds)
    pyautogui.click(x=875, y=39)

    #Save Animation
    time.sleep(2)
    pyautogui.click(x=1235, y=20)
    pyautogui.hotkey('ctrl', 's')

    #Save Animation as...File Name
    time.sleep(2)
    pyautogui.write(['backspace'] * 100)
    time.sleep(2)
    depth_animation_name = area_name + ' WSE Animation.mp4'
    pyautogui.write(depth_animation_name)
    #Save Animation as...Folder Path
    time.sleep(1)
    pyautogui.click(x=1182, y=101)
    pyautogui.write(full_path)
    time.sleep(1)
    pyautogui.hotkey('enter')
    time.sleep(1)
    #Click Save
    time.sleep(2)
    pyautogui.click(x=1230, y=597)
    pyautogui.hotkey('alt', 's')
    #Close Screen Recording Window
    time.sleep(1)
    pyautogui.click(x=1235, y=20)
    pyautogui.hotkey('alt', 'f4')

    #Click on 'Min' Button
    time.sleep(2)
    pyautogui.click(x=1003, y=72)

    #Open Screenshot
    time.sleep(2)
    pyautogui.hotkey('win', 'shift', 's')
    #Create Window to Screenshot
    time.sleep(3)
    pyautogui.moveTo(489, 100)
    time.sleep(0.2)
    pyautogui.dragTo(1915, 1008, button='left', duration=2)

    #Give a little delay for the script to run safely
    time.sleep(2)
    #Press the Windows key
    pyautogui.press('win')
    time.sleep(2)
    #Type 'File Explorer' into the search box
    pyautogui.write('File Explorer')
    #Press Enter to open File Explorer
    pyautogui.press('enter')
    #Click on "File Path" Bar
    time.sleep(2)
    pyautogui.click(x=1292, y=64)
    pyautogui.write('Pictures\Screenshots')
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.click(x=1292, y=64)
    pyautogui.hotkey('ctrl', 'c')
    screenshot_path = pyperclip.paste()

    time.sleep(2)
    #Assuming the newest screenshot is the one you want to rename and move
    #Find the latest file in the folder based on creation time
    latest_file = max([os.path.join(screenshot_path, f) for f in os.listdir(screenshot_path)], key=os.path.getctime)
    #New file name construction
    new_filename = f"{area_name} Min WSE.png"
    new_file_path = os.path.join(screenshot_path, new_filename)
    #Rename the file
    os.rename(latest_file, new_file_path)
    #Copy the new file to the destination folder
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    shutil.copy(new_file_path, os.path.join(full_path, new_filename))
    #Delete the original screenshot
    os.remove(new_file_path)

    #Click on 'X'
    time.sleep(2)
    pyautogui.click(x=1318, y=14)
    time.sleep(2)
    pyautogui.hotkey('alt', 'f4')

    #Click on 'Max' Button
    time.sleep(2)
    pyautogui.click(x=957, y=73)

    #Open Screenshot
    time.sleep(2)
    pyautogui.hotkey('win', 'shift', 's')
    #Create Window to Screenshot
    time.sleep(3)
    pyautogui.moveTo(489, 100)
    time.sleep(0.2)
    pyautogui.dragTo(1915, 1008, button='left', duration=2)

    #Give a little delay for the script to run safely
    time.sleep(2)
    #Press the Windows key
    pyautogui.press('win')
    time.sleep(4)
    #Type 'File Explorer' into the search box
    pyautogui.write('File Explorer')
    #Press Enter to open File Explorer
    pyautogui.press('enter')
    #Click on "File Path" Bar
    time.sleep(2)
    pyautogui.click(x=1292, y=64)
    pyautogui.write('Pictures\Screenshots')
    pyautogui.press('enter')
    time.sleep(2)
    pyautogui.click(x=1292, y=64)
    pyautogui.hotkey('ctrl', 'c')
    screenshot_path = pyperclip.paste()

    time.sleep(2)
    #Assuming the newest screenshot is the one you want to rename and move
    #Find the latest file in the folder based on creation time
    latest_file = max([os.path.join(screenshot_path, f) for f in os.listdir(screenshot_path)], key=os.path.getctime)
    #New file name construction
    new_filename = f"{area_name} Max WSE.png"
    new_file_path = os.path.join(screenshot_path, new_filename)
    #Rename the file
    os.rename(latest_file, new_file_path)
    #Copy the new file to the destination folder
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    shutil.copy(new_file_path, os.path.join(full_path, new_filename))
    #Delete the original screenshot
    os.remove(new_file_path)

    #Click on 'X'
    time.sleep(2)
    pyautogui.click(x=1318, y=14)
    time.sleep(2)
    pyautogui.hotkey('alt', 'f4')

    ###############################################################################################
    ####################### 5. Close HEC-RAS and Save all Projects and Outputs ####################
    ###############################################################################################
    #5.1 Close HEC-RAS and Save all Projects and Outputs
    #Click on 'File' Button
    time.sleep(2)
    pyautogui.click(x=32, y=43)
    #Click on 'Save' Button
    time.sleep(1)
    pyautogui.click(x=41, y=89)
    #Close RAS Mapper
    time.sleep(2)
    pyautogui.hotkey('alt', 'f4')
    #Click on 'Save' Button
    time.sleep(1)
    pyautogui.click(x=52, y=70)
    #Close HEC-RAS Mapper
    time.sleep(2)
    pyautogui.hotkey('alt', 'f4')

    #*********************************************************************************************
    #5.2 Copy all Files and Paste in Correct Folders
    #Copy all Input Files and Paste into Input Folder
    if user_input_precipitation_data_var == True:
        projection_file_rename = input_files + "/" + area_name + " Projection File.prj"
        path_to_geometry_rename = input_files + "/" + area_name + " Terrain File.tif"
        path_to_2d_flow_area_rename = input_files + "/" + area_name + " 2D Flow Area.shp"
        path_to_breaklines_rename = input_files + "/" + area_name + " Breaklines.shp"
        path_to_land_use_layer_rename = input_files + "/" + area_name + " Land Use Layer.shp"
        path_to_soil_layer_rename = input_files + "/" + area_name + " Soil Layer.shp"
        path_to_rainfall_data_rename = input_files + "/" + area_name + " Rainfall Data.dat"
    else:
        projection_file_rename = input_files + "/" + area_name + " Projection File.prj"
        path_to_geometry_rename = input_files + "/" + area_name + " Terrain File.tif"
        path_to_2d_flow_area_rename = input_files + "/" + area_name + " 2D Flow Area.shp"
        path_to_breaklines_rename = input_files + "/" + area_name + " Breaklines.shp"
        path_to_land_use_layer_rename = input_files + "/" + area_name + " Land Use Layer.shp"
        path_to_soil_layer_rename = input_files + "/" + area_name + " Soil Layer.shp"

    #Define source files and new names
    if user_input_precipitation_data_var == True:
        files_info = {projection_file: projection_file_rename, path_to_geometry: path_to_geometry_rename,
                      path_to_2d_flow_area: path_to_2d_flow_area_rename, path_to_breaklines: path_to_breaklines_rename,
                      path_to_land_use_layer: path_to_land_use_layer_rename,
                      path_to_soil_layer: path_to_soil_layer_rename,
                      path_to_rainfall_data: path_to_rainfall_data_rename}
    else:
        files_info = {projection_file: projection_file_rename, path_to_geometry: path_to_geometry_rename,
                      path_to_2d_flow_area: path_to_2d_flow_area_rename, path_to_breaklines: path_to_breaklines_rename,
                      path_to_land_use_layer: path_to_land_use_layer_rename,
                      path_to_soil_layer: path_to_soil_layer_rename}

    #Create the destination directory if it does not exist
    if not os.path.exists(input_files):
        os.makedirs(input_files)

    #Copy each file to the destination directory and rename it
    for src_path, new_name in files_info.items():
        #Define the destination path
        dest_file_path = os.path.join(input_files, new_name)
        #Copy the file
        shutil.copy(src_path, dest_file_path)

    print("All files have been copied and renamed successfully.")

    #Copy HEC-RAS Project Folder and Paste into Project Folder
    #Define the project name and construct the path to the source directory in the user's "Documents"
    source_dir = os.path.join(documents_folder_path, project_name)

    #Define the full path of the destination including the project folder name
    full_destination_path = os.path.join(full_path, project_name)

    #Check if the source directory exists before copying
    if os.path.exists(source_dir):
        #Copy the directory
        shutil.copytree(source_dir, full_destination_path)
        print(f"Successfully copied {project_name} to {full_destination_path}")
    else:
        print(f"Error: The source directory {source_dir} does not exist.")

    #Delete HEC-RAS Project Folder in Documents Folder
    time.sleep(5)

    #Iterate through each item in the directory
    for item in os.listdir(source_dir):
        item_path = os.path.join(source_dir, item)
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)  # Remove files and links
                print(f"Deleted file: {item_path}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Remove directories
                print(f"Deleted directory: {item_path}")
        except Exception as e:
            print(f"Failed to delete {item_path}. Reason: {e}")

def cancel_clicked():
    root.quit()

def bc_setup__message(point_spacing_dx, point_spacing_dy, default_mannings_n, near_spacing_m, repeats, far_spacing_m):
    global root
    root = tk.Tk()
    root.title("Boundary Condition Setup")

    #Set the icon
    root.iconbitmap('rog_automation.ico')

    label = tk.Label(root, text="Add the Boundary Conditions and click 'Continue' when completed.")
    label.pack(pady=10)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    continue_button = tk.Button(button_frame, text="Continue", command=lambda: continue_after_bc_setup__message(point_spacing_dx, point_spacing_dy, default_mannings_n, near_spacing_m, repeats, far_spacing_m))
    continue_button.pack(side=tk.LEFT, padx=10)

    cancel_button = tk.Button(button_frame, text="Cancel", command=cancel_clicked)
    cancel_button.pack(side=tk.LEFT, padx=10)

    root.mainloop()

def fix_all_meshes_message(user_input_precipitation_data_var):
    global root
    root = tk.Tk()
    root.title("Fix all Meshes")

    #Set the icon
    root.iconbitmap('rog_automation.ico')

    label = tk.Label(root, text="Fix all remaining Meshes and click 'Continue' when completed.")
    label.pack(pady=10)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    continue_button = tk.Button(button_frame, text="Continue", command=lambda: continue_after_fix_all_meshes_message(user_input_precipitation_data_var))
    continue_button.pack(side=tk.LEFT, padx=10)

    cancel_button = tk.Button(button_frame, text="Cancel", command=cancel_clicked)
    cancel_button.pack(side=tk.LEFT, padx=10)

    root.mainloop()

def friction_slope_message(full_path, area_name, user_input_precipitation_data_var, path_to_rainfall_data, precipitation_data_time_interval, starting_time, ending_time, computation_interval, hydrograph_output_interval, mapping_output_interval, detailed_output_interval, friction_slope):
    global root, entry
    root = tk.Tk()
    root.title("Friction Slope Calculation")

    #Set the icon
    root.iconbitmap('rog_automation.ico')

    label = tk.Label(root, text="Please Calculate the Friction Slope and Click Continue.")
    label.pack(pady=10)

    entry = tk.Entry(root)
    entry.pack(pady=10)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    continue_button = tk.Button(button_frame, text="Continue", command=lambda: continue_after_friction_slope_message(full_path, area_name, user_input_precipitation_data_var, path_to_rainfall_data, precipitation_data_time_interval, starting_time, ending_time, computation_interval, hydrograph_output_interval, mapping_output_interval, detailed_output_interval, friction_slope))
    continue_button.pack(side=tk.LEFT, padx=10)

    cancel_button = tk.Button(button_frame, text="Cancel", command=cancel_clicked)
    cancel_button.pack(side=tk.LEFT, padx=10)

    root.mainloop()

def computational_settings_message(full_path, input_files, documents_folder_path, project_name, area_name, projection_file, path_to_geometry, path_to_2d_flow_area, path_to_breaklines, path_to_land_use_layer, path_to_soil_layer, user_input_precipitation_data_var, path_to_rainfall_data, starting_time, ending_time):
    global root
    root = tk.Tk()
    root.title("Computational Settings")

    #Set the icon
    root.iconbitmap('rog_automation.ico')

    label = tk.Label(root, text="Please change any further Computational Settings.")
    label.pack(pady=10)

    button_frame: Frame = tk.Frame(root)
    button_frame.pack(pady=10)

    continue_button = tk.Button(button_frame, text="Continue", command=lambda: continue_after_computational_settings_message(full_path, input_files, documents_folder_path, project_name, area_name, projection_file, path_to_geometry, path_to_2d_flow_area, path_to_breaklines, path_to_land_use_layer, path_to_soil_layer, user_input_precipitation_data_var, path_to_rainfall_data, starting_time, ending_time))
    continue_button.pack(side=tk.LEFT, padx=10)

    cancel_button = tk.Button(button_frame, text="Cancel", command=cancel_clicked)
    cancel_button.pack(side=tk.LEFT, padx=10)

    root.mainloop()

def final_message():
    global root
    root = tk.Tk()
    root.title("2D Rain-On-Grid Model is Complete!")

    #Set the icon
    root.iconbitmap('rog_automation.ico')

    label = tk.Label(root, text="The Model is Complete!")
    label.pack(pady=0.5)
    label = tk.Label(root,
                     text="Please press Close button and DELETE HEC-RAS PROJECT FILE IN YOUR DOCUMENTS FOLDER AFTER CLOSING ALL PROGRAMS.")
    label.pack(pady=0.5)

    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    close_button = tk.Button(button_frame, text="Close", command=cancel_clicked)
    close_button.pack(side=tk.LEFT, padx=10)

    root.mainloop()

###############################################################################################
################################# 6. Graphical User Interface #################################
###############################################################################################
#Helper function to select files
def browse_file(entry, file_types):
    file_path = filedialog.askopenfilename(filetypes=file_types)
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

def browse_directory(entry):
    folder_path = filedialog.askdirectory()
    if folder_path:
        entry.delete(0, tk.END)
        entry.insert(0, folder_path)
        
def validate_inputs(values):
    required_fields = [
        "area_name", "input_folder_path", "output_folder_path", "documents_folder_path",
        "projection_file", "path_to_geometry", "path_to_2d_flow_area", "path_to_breaklines",
        "path_to_land_use_layer", "path_to_soil_layer", "point_spacing_dx", "point_spacing_dy",
        "default_mannings_n", "near_spacing_m", "repeats", "far_spacing_m", "starting_time",
        "ending_time"
    ]

    if values["user_input_precipitation_data"]:
        required_fields.extend(["path_to_rainfall_data", "precipitation_data_time_interval"])

    missing_inputs = [field for field in required_fields if not values[field]]
    if missing_inputs:
        missing_inputs_str = ', '.join(missing_inputs)
        messagebox.showerror("Input Error", f"Please provide values for the following inputs: {missing_inputs_str}")
        return False
    return True

def proceed():
    values = {
        "area_name": area_name.get(),
        "input_folder_path": input_folder.get(),
        "output_folder_path": output_folder.get(),
        "documents_folder_path": documents_folder.get(),
        "projection_file": projection_file.get(),
        "path_to_geometry": path_to_geometry.get(),
        "path_to_2d_flow_area": path_to_2d_flow_area.get(),
        "path_to_breaklines": path_to_breaklines.get(),
        "path_to_land_use_layer": path_to_land_use_layer.get(),
        "path_to_soil_layer": path_to_soil_layer.get(),
        "point_spacing_dx": point_spacing_dx.get(),
        "point_spacing_dy": point_spacing_dy.get(),
        "default_mannings_n": default_mannings_n.get(),
        "near_spacing_m": near_spacing_m.get(),
        "repeats": repeats.get(),
        "far_spacing_m": far_spacing_m.get(),
        "user_input_precipitation_data": user_input_precipitation_data_var.get(),
        "path_to_rainfall_data": path_to_rainfall_data.get(),
        "precipitation_data_time_interval": precipitation_data_time_interval.get(),
        "starting_time": starting_time.get(),
        "ending_time": ending_time.get(),
        "computation_interval": computation_interval.get(),
        "hydrograph_output_interval": hydrograph_output_interval.get(),
        "mapping_output_interval": mapping_output_interval.get(),
        "detailed_output_interval": detailed_output_interval.get()
    }
    
    if validate_inputs(values):
        if messagebox.showinfo("User Input Received", "Thank You for your Input. The HEC-RAS Rain-on-Grid Automation Program will run. PLEASE CLOSE ALL OTHER FILES AND PROGRAMS BEFORE CLICKING 'OK' AND DO NOT USE YOUR MOUSE OR KEYBOARD THERE AFTER.") == 'ok':            
            run_script(area_name, input_folder, output_folder, documents_folder, projection_file, path_to_geometry, path_to_2d_flow_area, path_to_breaklines, path_to_land_use_layer, path_to_soil_layer, point_spacing_dx, point_spacing_dy, default_mannings_n, near_spacing_m, repeats, far_spacing_m, user_input_precipitation_data_var, path_to_rainfall_data, precipitation_data_time_interval, starting_time, ending_time, computation_interval, hydrograph_output_interval, mapping_output_interval, detailed_output_interval)

def toggle_precipitation_inputs():
    if user_input_precipitation_data_var.get():
        path_to_rainfall_data.config(state='normal')
        rainfall_browse.config(state='normal')
        precipitation_data_time_interval.config(state='normal')
    else:
        path_to_rainfall_data.config(state='disabled')
        rainfall_browse.config(state='disabled')
        precipitation_data_time_interval.config(state='disabled')

app = tk.Tk()
app.title("HEC-RAS 2D Rain on Grid Model Automation")
app.iconbitmap('rog_automation.ico')

#Create frames for each group of inputs
frame_project = tk.LabelFrame(app, text="Project Information")
frame_geometry = tk.LabelFrame(app, text="Geometry Setup")
frame_hydraulic = tk.LabelFrame(app, text="Hydraulic Properties")
frame_2d_flow = tk.LabelFrame(app, text="2D Flow Area Editor")
frame_boundary = tk.LabelFrame(app, text="Breakline Properties")
frame_precipitation = tk.LabelFrame(app, text="Precipitation Data")
frame_simulation = tk.LabelFrame(app, text="Simulation Time Window")
frame_computation = tk.LabelFrame(app, text="Computation Settings")

frames = [frame_project, frame_geometry, frame_hydraulic, frame_2d_flow, frame_boundary, frame_precipitation, frame_simulation, frame_computation]

#Positioning frames
for i, frame in enumerate(frames):
    frame.pack(fill="both", expand="yes", padx=20, pady=10)

#Project Information Inputs
tk.Label(frame_project, text="Area Name:").pack(side="left")
area_name = tk.Entry(frame_project)
area_name.pack(side="left", padx=5)

tk.Label(frame_project, text="Input Folder:").pack(side="left")
input_folder = tk.Entry(frame_project)
input_folder.pack(side="left", padx=5)
input_folder_browse = tk.Button(frame_project, text="Browse", command=lambda: browse_directory(input_folder))
input_folder_browse.pack(side="left")

tk.Label(frame_project, text="Output/Download Folder:").pack(side="left")
output_folder = tk.Entry(frame_project)
output_folder.pack(side="left", padx=5)
output_folder_browse = tk.Button(frame_project, text="Browse", command=lambda: browse_directory(output_folder))
output_folder_browse.pack(side="left")

tk.Label(frame_project, text="Documents Folder:").pack(side="left")
documents_folder = tk.Entry(frame_project)
documents_folder.pack(side="left", padx=5)
documents_folder_browse = tk.Button(frame_project, text="Browse", command=lambda: browse_directory(documents_folder))
documents_folder_browse.pack(side="left")

tk.Label(frame_project, text="Projection File (.prj):").pack(side="left")
projection_file = tk.Entry(frame_project)
projection_file.pack(side="left", padx=5)
projection_file_browse = tk.Button(frame_project, text="Browse", command=lambda: browse_file(projection_file, [('PRJ files', '*.prj')]))
projection_file_browse.pack(side="left")

#Geometry Setup Inputs
tk.Label(frame_geometry, text="Terrain File:").pack(side="left")
path_to_geometry = tk.Entry(frame_geometry)
path_to_geometry.pack(side="left", fill="x", expand=True, padx=5)
geometry_browse = tk.Button(frame_geometry, text="Browse", command=lambda: browse_file(path_to_geometry, [('TIFF files', '*.tif')]))
geometry_browse.pack(side="left")

tk.Label(frame_geometry, text="2D Flow Area Shape File:").pack(side="left")
path_to_2d_flow_area = tk.Entry(frame_geometry)
path_to_2d_flow_area.pack(side="left", fill="x", expand=True, padx=5)
flow_area_browse = tk.Button(frame_geometry, text="Browse", command=lambda: browse_file(path_to_2d_flow_area, [('Shapefiles', '*.shp')]))
flow_area_browse.pack(side="left")

tk.Label(frame_geometry, text="Breaklines Shape File:").pack(side="left")
path_to_breaklines = tk.Entry(frame_geometry)
path_to_breaklines.pack(side="left", fill="x", expand=True, padx=5)
breaklines_browse = tk.Button(frame_geometry, text="Browse", command=lambda: browse_file(path_to_breaklines, [('Shapefiles', '*.shp')]))
breaklines_browse.pack(side="left")

#Hydraulic Properties Inputs
tk.Label(frame_hydraulic, text="Land Use Shape File:").pack(side="left")
path_to_land_use_layer = tk.Entry(frame_hydraulic)
path_to_land_use_layer.pack(side="left", fill="x", expand=True, padx=5)
land_use_browse = tk.Button(frame_hydraulic, text="Browse", command=lambda: browse_file(path_to_land_use_layer, [('Shapefiles', '*.shp')]))
land_use_browse.pack(side="left")

tk.Label(frame_hydraulic, text="Soil Layer Shape File:").pack(side="left")
path_to_soil_layer = tk.Entry(frame_hydraulic)
path_to_soil_layer.pack(side="left", fill="x", expand=True, padx=5)
soil_layer_browse = tk.Button(frame_hydraulic, text="Browse", command=lambda: browse_file(path_to_soil_layer, [('Shapefiles', '*.shp')]))
soil_layer_browse.pack(side="left")

tk.Label(frame_hydraulic, text="Default Manning's n:").pack(side="left")
default_mannings_n = tk.Entry(frame_hydraulic)
default_mannings_n.insert(0, "0.06")
default_mannings_n.pack(side="left", padx=5)

#2D Flow Area Editor
tk.Label(frame_2d_flow, text="Points Spacing DX:").pack(side="left")
point_spacing_dx = tk.Entry(frame_2d_flow)
point_spacing_dx.insert(0, "10")
point_spacing_dx.pack(side="left", padx=5)
tk.Label(frame_2d_flow, text="Points Spacing DY:").pack(side="left")
point_spacing_dy = tk.Entry(frame_2d_flow)
point_spacing_dy.insert(0, "10")
point_spacing_dy.pack(side="left", padx=5)

#Breakline Properties
tk.Label(frame_boundary, text="Near Spacing (m):").pack(side="left")
near_spacing_m = tk.Entry(frame_boundary)
near_spacing_m.insert(0, "5")
near_spacing_m.pack(side="left", padx=5)

tk.Label(frame_boundary, text="Repeats:").pack(side="left")
repeats = tk.Entry(frame_boundary)
repeats.insert(0, "2")
repeats.pack(side="left", padx=5)

tk.Label(frame_boundary, text="Far Spacing (m):").pack(side="left")
far_spacing_m = tk.Entry(frame_boundary)
far_spacing_m.insert(0, "7.5")
far_spacing_m.pack(side="left", padx=5)

#Precipitation Data
tk.Label(frame_precipitation, text="User Input for Precipitation Data:").pack(side="left")
user_input_precipitation_data_var = tk.IntVar()
user_input_precipitation_data = tk.Checkbutton(frame_precipitation, variable=user_input_precipitation_data_var, command=toggle_precipitation_inputs)
user_input_precipitation_data.pack(side="left", padx=5)

precipitation_description = tk.Label(frame_precipitation, text="If you do not check the box, the program will use SCS Type 3 distribution.", font=('Helvetica', 8, 'italic', 'bold'))
precipitation_description.pack(side="left", padx=5, pady=5)

tk.Label(frame_precipitation, text="Rainfall Data:").pack(side="left")
path_to_rainfall_data = tk.Entry(frame_precipitation, state='disabled')
path_to_rainfall_data.pack(side="left", expand="yes", fill="x", padx=5)
rainfall_browse = tk.Button(frame_precipitation, text="Browse", command=lambda: browse_file(path_to_rainfall_data, [('DAT files', '*.dat')]), state='disabled')
rainfall_browse.pack(side="left")

tk.Label(frame_precipitation, text="Rainfall Data Time Interval:").pack(side="left")
precipitation_data_time_interval = tk.Entry(frame_precipitation, state='disabled')
precipitation_data_time_interval.pack(side="left", padx=5)

#Simulation Time Window
tk.Label(frame_simulation, text="Starting Time:").pack(side="left")
starting_time = tk.Entry(frame_simulation)
starting_time.insert(0, "0100")
starting_time.pack(side="left", padx=5)

tk.Label(frame_simulation, text="Ending Time:").pack(side="left")
ending_time = tk.Entry(frame_simulation)
ending_time.insert(0, "1100")
ending_time.pack(side="left", padx=5)

#Computation Settings
computation_settings = {
    "Computation Interval": "1 Minute",
    "Hydrograph Output Interval": "1 Hour",
    "Mapping Output Interval": "1 Hour",
    "Detailed Output Interval": "1 Hour"
}

for label, default in computation_settings.items():
    tk.Label(frame_computation, text=label).pack(side="left")
    options = ["0.1 Second", "0.2 Second", "0.3 Second", "0.4 Second", "0.5 Second",
               "1 Second", "2 Second", "3 Second", "4 Second", "5 Second", "6 Second",
               "10 Second", "12 Second", "15 Second", "20 Second", "30 Second",
               "1 Minute", "2 Minute", "3 Minute", "4 Minute", "5 Minute", "6 Minute",
               "10 Minute", "12 Minute", "15 Minute", "20 Minute", "30 Minute",
               "1 Hour", "2 Hour", "3 Hour", "4 Hour", "6 Hour", "8 Hour", "12 Hour", "1 Day"]
    variable = tk.StringVar(app)
    variable.set(default)
    dropdown = tk.OptionMenu(frame_computation, variable, *options)
    dropdown.pack(side="left", padx=5)

    if label == "Computation Interval":
        computation_interval = variable
    elif label == "Hydrograph Output Interval":
        hydrograph_output_interval = variable
    elif label == "Mapping Output Interval":
        mapping_output_interval = variable
    elif label == "Detailed Output Interval":
        detailed_output_interval = variable

#Proceed Button
proceed_button = tk.Button(app, text="Proceed", command=proceed)
proceed_button.pack(side="bottom", pady=15)

app.mainloop()

#*********************************************************************************************
#*********************************************************************************************