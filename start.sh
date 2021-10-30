#!/bin/bash


echo """
 _   _      _ _______       _   
| | | |    | | | ___ \     | |  
| |_| | ___| | | |_/ / ___ | |_ 
|  _  |/ _ \ | | ___ \/ _ \| __|
| | | |  __/ | | |_/ / (_) | |_ 
\_| |_/\___|_|_\____/ \___/ \__|
                                
"""
rm -rf Plugins
git clone https://github.com/The-HellBot/Plugins
cd Plugins
python3 -m hellbot
