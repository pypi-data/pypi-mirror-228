@ECHO OFF

set VER=%1

IF "a%VER%"=="a" (
    ECHO version required ^(ex: 1.2.3^)
    exit /b
)


set CURRENT=%~dp0
set RELEASE=%CURRENT%release
set RELEASE_TEMP=%CURRENT%release_temp


cd /d %~dp0

git flow release finish %VER%

del /Q /S %RELEASE%
del /Q /S %RELEASE_TEMP%
mkdir %RELEASE%
mkdir %RELEASE_TEMP%

rye run pyinstaller.exe src\bufap\cli\bufap-cli.spec --distpath %RELEASE_TEMP%
rye run pyinstaller.exe src\bufap\gui\bufap-gui.spec --distpath %RELEASE_TEMP%


COPY README.md %RELEASE_TEMP%

pushd %RELEASE_TEMP%
powershell compress-archive -Force * %RELEASE%\bufap-%VER%.zip
popd

git flow release publish %VER%