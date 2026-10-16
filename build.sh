pip install requirements.txt
pyinstaller main.py --noconfirm --noconsole
cp assets ./dist/main/
echo "================================================="
echo "BUILD COMPLETE"
echo "output_file: ./dist/main/main"
echo "================================================="

