#This script automatically copies daily husbandry videos of the 110 tub to the ceph. This .bat is intended to run continuously; please re-start it if accidentally closed. If the ceph is not mounted at drive letter Z:/, this .bat will not work. 

@echo off
setlocal enabledelayedexpansion

for /f "delims=" %%a in ('wmic os get localdatetime ^| find "."') do set datetime=%%a

set year=!datetime:~0,4!
set month=!datetime:~4,2!
set day=!datetime:~6,2!
set hour=!datetime:~8,2!
set minute=!datetime:~10,2!
set second=!datetime:~12,2!

robocopy E:\CrabitatCam_daily\tub\ Z:\raw\CrabLab\CrabitatCam_daily\110\tub\ /E /MOVE /MON:1 /LOG+:E:\CrabitatCam_daily\robocopy\tub_Robocopylog_!day!_!month!_!year!_!hour!!minute!.txt /v /tee