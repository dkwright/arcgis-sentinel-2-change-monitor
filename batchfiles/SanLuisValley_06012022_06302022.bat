REM ********* Set Variable Values **************
set pPath="C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" 
set mdcsPath=C:\Image_Mgmt_Workflows\MDCS\arcgis-sentinel-2-change-monitor
set mdPath=C:\data\Sentinel-2\SanLuisValley.gdb\SanLuisValley

REM bbox needs to be WGS84 4326 MINX,MINY,MAXX,MAXY
REM SanLuisValley
%pPath%  "%mdcsPath%\scripts\MDCS.py" -i:"%mdcsPath%\Parameter\Config\DEA.xml" -m:"%mdPath%" -c:CM+sentinelModifySrc+AF+AR+CV -p:2022-06-01$startDate -p:2022-06-30$endDate -p:100$cloud -p:-106.54028166999996,36.93116725900006,-105.32903899399997,38.23272276600005$coordinate -p:1$interval 
REM Mark duplicates, remove them, and set properties all at once
%pPath%  "%mdcsPath%\scripts\MDCS.py" -i:"%mdcsPath%\Parameter\Config\DEA.xml" -m:"%mdPath%" -c:markduplicate+RRFMD+SP