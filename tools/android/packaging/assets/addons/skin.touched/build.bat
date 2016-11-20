@echo off
ECHO ----------------------------------------
echo Creating Touched Build Folder
IF Exist ..\..\project\Win32BuildSetup\BUILD_WIN32\Xbmc\addons\skin.touched rmdir ..\..\project\Win32BuildSetup\BUILD_WIN32\Xbmc\addons\skin.touched /S /Q
md ..\..\project\Win32BuildSetup\BUILD_WIN32\Xbmc\addons\skin.touched\media\

Echo build.bat>>exclude.txt
Echo \skin.touched\media\>>exclude.txt
Echo exclude.txt>>exclude.txt

ECHO ----------------------------------------
ECHO Creating XBT File...
START /B /WAIT ..\..\Tools\TexturePacker\TexturePacker -dupecheck -input media -output ..\..\project\Win32BuildSetup\BUILD_WIN32\Xbmc\addons\skin.touched\media\Textures.xbt

ECHO ----------------------------------------
ECHO XBT Texture Files Created...
ECHO Building Skin Directory...
xcopy "..\skin.touched" "..\..\project\Win32BuildSetup\BUILD_WIN32\Xbmc\addons\skin.touched" /E /Q /I /Y /EXCLUDE:exclude.txt

del exclude.txt
