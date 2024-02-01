@echo off
setlocal

set "Desktop=C:\Users\%USERNAME%\Desktop"

git clone https://github.com/010101aa/pac_man.git

move "/pac_man" "%Desktop%"

exit /b
