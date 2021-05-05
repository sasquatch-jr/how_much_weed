set -e
#!/bin/bash
cd $HOME/how_much_weed
python3 how_much.py
git add index.html
git commit -m "Latest Run"
git push origin master
