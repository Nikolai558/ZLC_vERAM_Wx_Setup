@ECHO OFF

:version_chk

SET USER_VER=1.0rc1

TITLE ZLC vERAM Wx Setup (%USER_VER%)

SET GITHUB_VERSION_CHK_URL=https://github.com/KSanders7070/ZLC_vERAM_Wx_Setup/blob/main/Version_Check

SET BATCH_FILE_RELEASES_URL=https://github.com/KSanders7070/ZLC_vERAM_Wx_Setup/releases

ECHO.
ECHO.
ECHO * * * * * * * * * * * * *
ECHO  CHECKING FOR UPDATES...
ECHO * * * * * * * * * * * * *
ECHO.
ECHO.

CD /d "%temp%"
IF Not Exist TempBatWillDelete.bat goto MK_TEMP_FOLDER
	DEL /Q TempBatWillDelete.bat

:MK_TEMP_FOLDER

If Not Exist "%temp%\VersionCheckWillDelete\" MD "%temp%\VersionCheckWillDelete"

CD /d "%temp%\VersionCheckWillDelete"

powershell -Command "Invoke-WebRequest %GITHUB_VERSION_CHK_URL% -OutFile 'version_check.HTML'"

For /F "Tokens=3 Delims=><" %%G In ('%__AppDir__%findstr.exe ">VERSION-" "version_check.html"') Do For /F "Tokens=1* Delims=-" %%H In ("%%G") Do Set "GH_VER=%%I"

If "%USER_VER%" == "%GH_VER%" GOTO RMDIR

:UPDATE_AVAIL

CLS

CD /d "%temp%"
rd /s /q "%temp%\VersionCheckWillDelete\"

ECHO.
ECHO.
ECHO * * * * * * * * * * * * *
ECHO     UPDATE AVAILABLE
ECHO * * * * * * * * * * * * *
ECHO.
ECHO.
ECHO GITHUB VERSION: %GH_VER%
ECHO YOUR VERSION:   %USER_VER%
ECHO.
ECHO.
ECHO.
ECHO  CHOICES:
ECHO.
ECHO     A   -   AUTOMATICALLY UPDATE THE BATCH FILE YOU ARE USING NOW.
ECHO.
ECHO     M   -   MANUALLY DOWNLOAD THE NEWEST BATCH FILE UPDATE AND USE THAT FILE.
ECHO.
ECHO     C   -   CONTINUE USING THIS FILE.
ECHO.
ECHO.
ECHO.
ECHO NOTE: IF YOU HAVE ATTMEPTED TO AUTOATMICALLY UPDATE ALREADY AND YOU CONTINUE
ECHO       TO GET THIS UPDATE SCREEN, PLEASE UTILIZE THE MANUAL UPDATE OPTION.
ECHO.
ECHO.
ECHO.

:UPDATE_CHOICE

SET UPDATE_CHOICE=UPDATE_METHOD_NOT_SELECTED

	SET /p UPDATE_CHOICE=Please type either A, M, or C and press Enter: 
		if /I %UPDATE_CHOICE%==A GOTO AUTO_UPDATE
		if /I %UPDATE_CHOICE%==M GOTO MANUAL_UPDATE
		if /I %UPDATE_CHOICE%==C GOTO CONTINUE
		if /I %UPDATE_CHOICE%==UPDATE_METHOD_NOT_SELECTED GOTO UPDATE_CHOICE
			echo.
			echo.
			echo.
			echo.
			echo  %UPDATE_CHOICE% IS NOT A RECOGNIZED RESPONSE. Try again.
			echo.
			GOTO UPDATE_CHOICE

:AUTO_UPDATE

CLS

ECHO.
ECHO.
ECHO * * * * * * * * * * * * * * * * * * * * * * * * * * *
ECHO.
ECHO   PRESS ANY KEY TO START THE AUTOMATIC UPDATE.
ECHO.
ECHO.
ECHO   THIS SCREEN WILL CLOSE.
ECHO.
ECHO   WAIT 5 SECONDS
ECHO.
ECHO   THE NEW UPDATED BATCH FILE WILL START BY ITSELF.
ECHO.
ECHO * * * * * * * * * * * * * * * * * * * * * * * * * * *
ECHO.
ECHO.

PAUSE

SET CUR_BAT_DIR=%~dp0

SET BAT_NAME=%~nx0

CD /d "%temp%"

ECHO @ECHO OFF>TempBatWillDelete.bat
ECHO TIMEOUT 5>TempBatWillDelete.bat
ECHO CD /d "%~dp0">TempBatWillDelete.bat
ECHO START %~nx0>TempBatWillDelete.bat
ECHO EXIT>TempBatWillDelete.bat

START /MIN TempBatWillDelete.bat

CD /d "%~dp0"

powershell -Command "Invoke-WebRequest %BATCH_FILE_RELEASES_URL%/download/v%GH_VER%/%~nx0 -OutFile '%~nx0'"

EXIT /b

:MANUAL_UPDATE

CLS

START "" "%BATCH_FILE_RELEASES_URL%"

ECHO.
ECHO.
ECHO GO TO THE FOLLOWING WEBSITE, DOWNLOAD AND USE THE LATEST VERSION OF %~nx0
ECHO.
ECHO.
ECHO    %BATCH_FILE_RELEASES_URL%
ECHO.
ECHO.
ECHO.
ECHO.
ECHO NOTE: PRESSING ANY KEY NOW WILL QUIT THIS VERSION OF THE BATCH FILE.
ECHO.
ECHO.

PAUSE

EXIT /b

:RMDIR

CLS

CD /d "%temp%"
rd /s /q "%temp%\VersionCheckWillDelete\"

:CONTINUE

tasklist /FI "IMAGENAME eq vERAM.exe" 2>NUL | find /I /N "vERAM.exe">NUL
if "%ERRORLEVEL%"=="0" (
	
	COLOR 0C
	
	ECHO.
	ECHO.
	ECHO               *********
	ECHO                WARNING
	ECHO               *********
	ECHO.
	ECHO  YOUR vERAM PROGRAM IS CURRENTLY OPEN.
	ECHO.
	ECHO  Please Close vERAM and then restart
	echo  this BATCH File.
	ECHO.
	ECHO.
	ECHO  Press any key to Close this Batch File.
	PAUSE>NUL
	EXIT
)

IF EXIST "%TEMP%\vERAM_ZLC_WX_SETUP" RD /S /Q "%TEMP%\vERAM_ZLC_WX_SETUP"
MD "%TEMP%\vERAM_ZLC_WX_SETUP"

ECHO.
ECHO.
ECHO               *********
ECHO                 ABOUT
ECHO               *********
ECHO.
ECHO.
ECHO  This BATCH File will manipulate your
ECHO  vERAMConfig.xml file in order to add
ECHO  all of the standard weather stations
ECHO  and altimeter settings for ZLC ARTCC.
ECHO.
ECHO  It takes around 2 seconds for every
ECHO  MB of size of your vERAMConfig.xml
ECHO.
ECHO  IF THERE IS AN ISSUE AFTER RUNNING:
ECHO       This BATCH file will create a
ECHO       back-up config file onto your
ECHO       desktop prior to running labeled:
ECHO       "BACKUP-vERAMConfig.xml"
ECHO.
ECHO       Replace the contents of your
ECHO       vERAMConfig.xml file with the
ECHO       contents of that backup file.
ECHO.
ECHO.
ECHO  TO START THE PROCESS, PRESS ANY KEY.
ECHO.
ECHO.
PAUSE>NUL

IF NOT EXIST "%USERPROFILE%\AppData\Local\vERAM\vERAMConfig.xml" GOTO CONFIG_NOT_FOUND
IF EXIST "%USERPROFILE%\AppData\Local\vERAM\vERAMConfig.xml" GOTO CONFIG_FOUND

:CONFIG_NOT_FOUND

CLS
	
echo.
echo.
echo ------------------------------------
echo.
echo  Select the directory
echo  where the vERAMConfig.xml file is.
echo.
echo.
echo  NOTE:
echo    -if you right click on your
echo     vERAM.exe Shortcut, and select
echo     "Open File Location", this is
echo     the directory that this BATCH
echo     needs selected.
echo.
echo ------------------------------------
echo.
echo.

set "psCommand="(new-object -COM 'Shell.Application')^
.BrowseForFolder(0,'Select The Folder With vERAMConfig.xml',0,0).self.path""

	for /f "usebackq delims=" %%I in (`powershell %psCommand%`) do set "VRC_DIR=%%I"

GOTO EX_MARK_CONVRT

:CONFIG_FOUND

SET SOURCE_DIR=%USERPROFILE%\AppData\Local\vERAM

:MAKE_BKUP

TYPE vERAMConfig.xml>"%USERPROFILE%\DESKTOP\BACKUP-vERAMConfig.xml"

:EX_MARK_CONVRT

CLS

ECHO.
ECHO.
ECHO  PREPARING FILES, PLEASE WAIT...
ECHO.
ECHO.

CD "%SOURCE_DIR%"

powershell -Command "(gc vERAMConfig.xml) -replace '!', '^!' | Out-File -encoding ASCII '%TEMP%\vERAM_ZLC_WX_SETUP\temp-vERAMConfig.xml'"

:TRANSFER

CLS

ECHO.
ECHO.
ECHO PROCESSED:

CD "%TEMP%\vERAM_ZLC_WX_SETUP"

setlocal EnableDelayedExpansion

SET PHASE=HEADER
SET WX_STATUS=NOT_REACHED

set file=temp-vERAMConfig.xml
set /a TOTAL_LINES=0
for /f %%a in ('type "%file%"^|find "" /v /c') do set /a TOTAL_LINES=%%a

SET /A COUNT=0

SET PERC_1=Not_Used
SET PERC_3=Not_Used
SET PERC_6=Not_Used
SET PERC_8=Not_Used
SET PERC_10=Not_Used
SET PERC_20=Not_Used
SET PERC_30=Not_Used
SET PERC_40=Not_Used
SET PERC_50=Not_Used
SET PERC_60=Not_Used
SET PERC_70=Not_Used
SET PERC_80=Not_Used
SET PERC_90=Not_Used
SET PERC_94=Not_Used
SET PERC_97=Not_Used
SET PERC_99=Not_Used

for /f "tokens=* delims=" %%a in (temp-vERAMConfig.xml) do (

	SET /A COUNT=!COUNT! + 1
	set /a "PERC=100*!COUNT!/!TOTAL_LINES!"
	
	IF !PERC! EQU 1 IF !PERC_1!==Not_Used ECHO !PERC!%% && SET PERC_1=Used
	IF !PERC! EQU 3 IF !PERC_3!==Not_Used ECHO !PERC!%% && SET PERC_3=Used
	IF !PERC! EQU 6 IF !PERC_6!==Not_Used ECHO !PERC!%% && SET PERC_6=Used
	IF !PERC! EQU 8 IF !PERC_8!==Not_Used ECHO !PERC!%% && SET PERC_8=Used
	IF !PERC! EQU 10 IF !PERC_10!==Not_Used ECHO !PERC!%% && SET PERC_10=Used
	IF !PERC! EQU 20 IF !PERC_20!==Not_Used ECHO !PERC!%% && SET PERC_20=Used
	IF !PERC! EQU 30 IF !PERC_30!==Not_Used ECHO !PERC!%% && SET PERC_30=Used
	IF !PERC! EQU 40 IF !PERC_40!==Not_Used ECHO !PERC!%% && SET PERC_40=Used
	IF !PERC! EQU 50 IF !PERC_50!==Not_Used ECHO !PERC!%% && SET PERC_50=Used
	IF !PERC! EQU 60 IF !PERC_60!==Not_Used ECHO !PERC!%% && SET PERC_60=Used
	IF !PERC! EQU 70 IF !PERC_70!==Not_Used ECHO !PERC!%% && SET PERC_70=Used
	IF !PERC! EQU 80 IF !PERC_80!==Not_Used ECHO !PERC!%% && SET PERC_80=Used
	IF !PERC! EQU 90 IF !PERC_90!==Not_Used ECHO !PERC!%% && SET PERC_90=Used
	IF !PERC! EQU 94 IF !PERC_94!==Not_Used ECHO !PERC!%% && SET PERC_94=Used
	IF !PERC! EQU 97 IF !PERC_97!==Not_Used ECHO !PERC!%% && SET PERC_97=Used
	IF !PERC! EQU 99 IF !PERC_99!==Not_Used ECHO !PERC!%% && SET PERC_99=Used

	SET LINE=%%a
	
	IF "!PHASE!"=="ZLC_WX_DONE" (
		
		SET LAST_LINE_CHK=!LINE:~0,13!

			IF NOT "!LAST_LINE_CHK!"=="</vERAMConfig>" ECHO !LINE!>>"OUTPUT_TEMP.xml"
			IF "!LAST_LINE_CHK!"=="</vERAMConfig>" ECHO ^</vERAMConfig^>>>"OUTPUT_TEMP.xml"
	)
	
	IF "!PHASE!"=="ZLC" (
	
		SET REQWX_CHK=!LINE:~9,19!

			IF "!REQWX_CHK!"=="RequestedAltimeters" SET WX_STATUS=REACHED
		
		IF "!WX_STATUS!"=="DONE" (
			
			SET PHASE=ZLC_WX_DONE
		
			ECHO !LINE!>>"OUTPUT_TEMP.xml"
		)
		
		IF "!WX_STATUS!"=="PRINTED" (
		
			SET BCN_CHK=!LINE:~9,19!

			IF "!BCN_CHK!"=="SelectedBeaconCodes" SET WX_STATUS=DONE
			
			IF "!WX_STATUS!"=="DONE" ECHO !LINE!>>"OUTPUT_TEMP.xml"
		)
		
		IF "!WX_STATUS!"=="NOT_REACHED" (
			
			ECHO !LINE!>>"OUTPUT_TEMP.xml"
		)
		
		IF "!WX_STATUS!"=="REACHED" (
			
			(
			ECHO         ^<RequestedAltimeters^>
			ECHO           ^<string^>KBIL^</string^>
			ECHO           ^<string^>KBKE^</string^>
			ECHO           ^<string^>KBOI^</string^>
			ECHO           ^<string^>KBPI^</string^>
			ECHO           ^<string^>KBTM^</string^>
			ECHO           ^<string^>KBZN^</string^>
			ECHO           ^<string^>KCDC^</string^>
			ECHO           ^<string^>KCOD^</string^>
			ECHO           ^<string^>KCTB^</string^>
			ECHO           ^<string^>KEKO^</string^>
			ECHO           ^<string^>KELY^</string^>
			ECHO           ^<string^>KGDV^</string^>
			ECHO           ^<string^>KGGW^</string^>
			ECHO           ^<string^>KGJT^</string^>
			ECHO           ^<string^>KGPI^</string^>
			ECHO           ^<string^>KGTF^</string^>
			ECHO           ^<string^>KHLN^</string^>
			ECHO           ^<string^>KHVR^</string^>
			ECHO           ^<string^>KIDA^</string^>
			ECHO           ^<string^>KJAC^</string^>
			ECHO           ^<string^>KLWT^</string^>
			ECHO           ^<string^>KMLS^</string^>
			ECHO           ^<string^>KMSO^</string^>
			ECHO           ^<string^>KMUO^</string^>
			ECHO           ^<string^>KOGD^</string^>
			ECHO           ^<string^>KPIH^</string^>
			ECHO           ^<string^>KPVU^</string^>
			ECHO           ^<string^>KRIW^</string^>
			ECHO           ^<string^>KRKS^</string^>
			ECHO           ^<string^>KSDY^</string^>
			ECHO           ^<string^>KSHR^</string^>
			ECHO           ^<string^>KSLC^</string^>
			ECHO           ^<string^>KSUN^</string^>
			ECHO           ^<string^>KTPH^</string^>
			ECHO           ^<string^>KTWF^</string^>
			ECHO           ^<string^>KVEL^</string^>
			ECHO           ^<string^>KWMC^</string^>
			ECHO           ^<string^>KWRL^</string^>
			ECHO           ^<string^>KXWA^</string^>
			ECHO         ^</RequestedAltimeters^>
			ECHO         ^<RequestedWeatherReports^>
			ECHO           ^<string^>KBIL^</string^>
			ECHO           ^<string^>KBOI^</string^>
			ECHO           ^<string^>KBZN^</string^>
			ECHO           ^<string^>KGPI^</string^>
			ECHO           ^<string^>KGTF^</string^>
			ECHO           ^<string^>KHLN^</string^>
			ECHO           ^<string^>KIDA^</string^>
			ECHO           ^<string^>KJAC^</string^>
			ECHO           ^<string^>KMSO^</string^>
			ECHO           ^<string^>KOGD^</string^>
			ECHO           ^<string^>KPIH^</string^>
			ECHO           ^<string^>KPVU^</string^>
			ECHO           ^<string^>KSLC^</string^>
			ECHO           ^<string^>KSUN^</string^>
			ECHO           ^<string^>KTWF^</string^>
			ECHO         ^</RequestedWeatherReports^>
			)>>"OUTPUT_TEMP.xml"
			
			SET WX_STATUS=PRINTED
		)
	)
	
	IF "!PHASE!"=="HEADER" (
		
		SET FACILITY_CHK=!LINE:~6,7!
		
			IF "!FACILITY_CHK!"=="<ID>ZLC" SET PHASE=ZLC
			
			ECHO !LINE!>>"OUTPUT_TEMP.xml"
	)
)

endlocal

TYPE OUTPUT_TEMP.xml>"%SOURCE_DIR%\vERAMConfig.xml"

RD /S /Q "%TEMP%\vERAM_ZLC_WX_SETUP"

CLS

COLOR 0A

ECHO.
ECHO.
ECHO                          ******
ECHO                           DONE
ECHO                          ******
ECHO.
ECHO.
ECHO  Your ZLC vERAM Profile should now have all of the Standard
echo  ZLC Weather Stations and Altimeters.
ECHO  Relaunch vERAM and the ZLC Profile.
ECHO.
ECHO.
ECHO  REMINDER:
ECHO.
ECHO       -A backup vERAMConfig.xml file can be found on your
echo        desktop just in case something went wrong.
ECHO.
ECHO.
ECHO.
ECHO.
ECHO Press any key to exit.
PAUSE>NUL
