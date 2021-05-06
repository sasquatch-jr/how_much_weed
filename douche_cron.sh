set -e
#!/bin/bash
cd $HOME/how_much_weed
python3 douchie_love.py
git add douche_love.html
git commit -m "Latest Run"
git push origin master
