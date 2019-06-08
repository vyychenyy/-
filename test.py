import os

os.system('cd Cloud-Platform && ls')
#os.system('ls')
#os.system ('git config --global user.name "enaosun"')
#os.system('git config --global user.email "enao_sun@163.com"')
#os.system('git pull origin master')
os.system('git fetch origin')
os.system('git merge origin/master')
os.system('git add .')

#os.system('git remote add origin "https://github.com/vyychenyy/Cloud-Platform.git"')
os.system('git commit -m "try"')

os.system('git push --set-upstream origin master')