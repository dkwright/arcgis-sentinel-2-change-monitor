REM ********* Set Variable Values **************
set pPath="C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" 
set mdcsPath=C:\Image_Mgmt_Workflows\MDCS\arcgis-sentinel-2-change-monitor

cd %mdcsPath%
cd scripts

echo Creating MDs...
%pPath%  "%mdcsPath%\scripts\01-manage-mosaic-datasets.py"
echo Mosaic Dataset management script is finished.

echo Copying MDs to Image Hosting fileserver...
%pPath%  "%mdcsPath%\scripts\02-manage-image-services.py"
echo Image Service management script is finished.

echo Press any key to close ...
pause
exit