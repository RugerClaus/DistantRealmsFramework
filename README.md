<h1>Welcome to Distant Realms, a top down survival RPG</h1>

**DEPENDENCIES**

<p>This project has a few dependencies. The only third party assets are the fonts in assets/font:</p>
<p>This project uses the OpenSansPX font, a modified version of Open Sans, under the Apache License 2.0. Please see the LICENSE.txt in the assets/font directory for more details.</p>

<p>The reason we're lacking a requirements.txt file, is that there are only 4 dependencies!<p>

<h3>From the root directory run this series of commands to get set up</h3>

```bash
python3 -m venv virtualenv
source virtualenv/bin/activate
pip install pygame-ce pyinstaller mutagen requests
python3 setup.py
python3 main.py --dev
```
**NOTE:** passing the flag --dev enables developer mode by default on startup
**NOTE:** `setup.py` is absolutely **ESSENTIAL** to run the program.


**FEATURE ADDITIONS**

<p>For feature additions, before coming up with your own you should take a look at the requested_additions file in the root directory of this repository and see if you can piece in any of those requested features. Then submit a pull request to have your code merged into the main branch. This is mostly notation for me though</p>