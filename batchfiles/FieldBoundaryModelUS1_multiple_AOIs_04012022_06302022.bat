REM ********* Set Variable Values **************
set pPath="C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe" 
set mdcsPath=C:\Image_Mgmt_Workflows\MDCS\arcgis-sentinel-2-change-monitor
set mdPath=C:\data\Sentinel-2\FieldBoundaryModelUS1_multiple_AOIs.gdb\FieldBoundaryModelUS1_multiple_AOIs

REM bbox needs to be WGS84 4326 MINX,MINY,MAXX,MAXY
REM Imperial_Valley
%pPath%  "%mdcsPath%\scripts\MDCS.py" -i:"%mdcsPath%\Parameter\Config\DEA.xml" -m:"%mdPath%" -c:CM+sentinelModifySrc+AF+AR+CV -p:2022-05-01$startDate -p:2022-06-28$endDate -p:100$cloud -p:-115.89090323799996,32.65081569800003,-115.23081141599994,33.33123665100004$coordinate -p:1$interval 
REM TreasureValley
%pPath%  "%mdcsPath%\scripts\MDCS.py" -i:"%mdcsPath%\Parameter\Config\DEA.xml" -m:"%mdPath%" -c:CM+sentinelModifySrc+AF+AR+CV -p:2022-05-01$startDate -p:2022-06-28$endDate -p:100$cloud -p:-117.81464996999995,42.04847521500005,-111.10895665599998,44.32551814200008$coordinate -p:1$interval 
REM CentralValley
%pPath%  "%mdcsPath%\scripts\MDCS.py" -i:"%mdcsPath%\Parameter\Config\DEA.xml" -m:"%mdPath%" -c:CM+sentinelModifySrc+AF+AR+CV -p:2022-05-01$startDate -p:2022-06-28$endDate -p:100$cloud -p:-123.05368237899995,34.808751510000036,-117.62241659399996,41.180800979000026$coordinate -p:1$interval 
REM SanLuisValley
%pPath%  "%mdcsPath%\scripts\MDCS.py" -i:"%mdcsPath%\Parameter\Config\DEA.xml" -m:"%mdPath%" -c:CM+sentinelModifySrc+AF+AR+CV -p:2022-05-01$startDate -p:2022-06-28$endDate -p:100$cloud -p:-106.54028166999996,36.93116725900006,-105.32903899399997,38.23272276600005$coordinate -p:1$interval 
REM Yakima
%pPath%  "%mdcsPath%\scripts\MDCS.py" -i:"%mdcsPath%\Parameter\Config\DEA.xml" -m:"%mdPath%" -c:CM+sentinelModifySrc+AF+AR+CV -p:2022-05-01$startDate -p:2022-06-28$endDate -p:100$cloud -p:-121.52517425199994,45.83169851100007,-117.96019644299997,47.959396920000074$coordinate -p:1$interval 
REM Midwest1
%pPath%  "%mdcsPath%\scripts\MDCS.py" -i:"%mdcsPath%\Parameter\Config\DEA.xml" -m:"%mdPath%" -c:CM+sentinelModifySrc+AF+AR+CV -p:2022-05-01$startDate -p:2022-06-28$endDate -p:100$cloud -p:-97.13105221599994,41.86047715600006,-93.49979580199994,43.848741833000076$coordinate -p:1$interval 
REM Midwest2
%pPath%  "%mdcsPath%\scripts\MDCS.py" -i:"%mdcsPath%\Parameter\Config\DEA.xml" -m:"%mdPath%" -c:CM+sentinelModifySrc+AF+AR+CV -p:2022-05-01$startDate -p:2022-06-28$endDate -p:100$cloud -p:-89.99811351499994,38.41683673800003,-85.44433848599994,42.249421418000054$coordinate -p:1$interval 
REM Midwest3
%pPath%  "%mdcsPath%\scripts\MDCS.py" -i:"%mdcsPath%\Parameter\Config\DEA.xml" -m:"%mdPath%" -c:CM+sentinelModifySrc+AF+AR+CV -p:2022-05-01$startDate -p:2022-06-28$endDate -p:100$cloud -p:-92.91439668699996,35.98965643100007,-89.04639301499998,38.88961345600006$coordinate -p:1$interval 
REM Midwest4
%pPath%  "%mdcsPath%\scripts\MDCS.py" -i:"%mdcsPath%\Parameter\Config\DEA.xml" -m:"%mdPath%" -c:CM+sentinelModifySrc+AF+AR+CV -p:2022-05-01$startDate -p:2022-06-28$endDate -p:100$cloud -p:-92.08738047599996,41.06657310300005,-87.70272988699998,44.249202754000066$coordinate -p:1$interval 
REM Mark duplicates, remove them, and set properties all at once
%pPath%  "%mdcsPath%\scripts\MDCS.py" -i:"%mdcsPath%\Parameter\Config\DEA.xml" -m:"%mdPath%" -c:markduplicate+RRFMD+SP