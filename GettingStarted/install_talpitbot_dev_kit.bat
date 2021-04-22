@setlocal enableextensions
@cd /d "%~dp0"
@ECHO OFF

SET CURRENTDIR="%cd%"

:: check python version 
py -0 | findstr "3.8" || goto no_python_version 


:: check if git exists
where git > nul 2>&1 || goto no_git

:: check if botIt directory exists in the desktop
IF EXIST "%CURRENTDIR%\botIt" (goto botIt_exsist)

:: clean the screen
cls

:: get the feature name from the user
set /p feature_name=Enter your feature name:

:: get the user token
set /p user_bot_token=Enter your bot token:

:: go to desktop
cd %CURRENTDIR%
:: get our project's files
git clone https://github.com/dvirby/BotIt.git --recurse-submodules || goto clone_problem

:after_cloning(
:: insert to our new directory
cd %CURRENTDIR%/BotIt/

:: do not track settings.py
git update-index --assume-unchanged settings.py
git update-index --skip-worktree settings.py
git update-index --assume-unchanged credentials.yaml
git update-index --skip-worktree credentials.yaml

:: create a new branch and checkout to this branch
git checkout -b %feature_name%

robocopy GettingStarted/FeatureTemplate Features/%feature_name% /E

rename "%CURRENTDIR%\BotIt\Features\%feature_name%\UI\your_feature_name.py" %feature_name%.py

:: create a virtual Environments and download all the requirements
py -3.8 -m venv %CURRENTDIR%\BotIt\Virtual_Environments
call %CURRENTDIR%\botIt\Virtual_Environments\Scripts\activate

:: Add talpiot & BotFramework to PATH
pip install virtualenvwrapper-win
call add2virtualenv BotFramework
call add2virtualenv APIs

:: download all the features requirements
cd %CURRENTDIR%\BotIt\GettingStarted
python install_feature_reqs.py

:: insert user token to credentials.yaml file 
cd %CURRENTDIR%\BotIt\GettingStarted
python change_yaml_file.py %user_bot_token% %CURRENTDIR%\BotIt\credentials.yaml


cls
echo finished installation, press any key to continue
pause
goto end_of_BotIt_install

)

:no_python_version
(
	cls
	:: check if git exists
	where git > nul 2>&1 || echo You have a problem with git, please download git and then continue 
	
	echo You have a problem with the python version, please download python 3.8 version and then continue
	pause
	goto eof
)

:no_git
(
	cls
	echo You have a problem with git, please download git and then continue
	pause
	goto eof
)

:clone_problem
(
	:: check if there is a error in the clone and them ask for user:pass@gitlab...
	cls
	set /p user_name=Enter your username to gitlab:
	set /p pass=Enter your password to gitlab:
	
	:: go to desktop
	cd %CURRENTDIR%

	:: get our project's files
	git clone https://%user_name%:%pass%@gitlab.com/dvir.benyashar.41/botIt.git --recurse-submodules || goto big_clone_problem
	goto after_cloning
)

:botIt_exsist
(
	cls
	echo Please delete the directory "botIt" and try again.
	pause
	goto eof
)

:big_clone_problem(
	:: if the user didn't success to make the clone
	echo You have problem with cloning, please send a message to one of the botIt team members.
	goto eof
)

:end_of_BotIt_install


