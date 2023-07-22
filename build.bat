rmdir /s /q dist

cd src

pyinstaller --noconsole --distpath ../dist --workpath ../build --onefile --name DiscOverlay --specpath  ../build/spec --icon ../../src/assets/discord_icon.ico --clean app.py

cd ..

rmdir /s /q build

robocopy ./src/assets ./dist/assets /E /NFL /NDL /NJH /NJS /nc /ns /np