pip install -r requirements.txt
pyinstaller main.py --noconfirm --noconsole
cp -r assets ./dist/main/
echo "================================================="
echo "BUILD COMPLETE"
echo "output_file: ./dist/main/main"
echo "================================================="

