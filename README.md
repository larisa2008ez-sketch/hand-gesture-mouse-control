# hand gesture mouse control for macos

a simple computer vision project that lets you control your mac's mouse cursor and drag-and-drop items in the air using your webcam. it's tweaked specifically to work on modern macos and python 3.14 without crashing.

## what it actually does
* moves the cursor: tracks your index finger and moves the mouse across the screen.
* drag and drop: pinch your thumb and index finger together to click and hold. separate them to let go.
* works on apple silicon: i fixed all the annoying mac bugs, like ssl certificate failures during model download and mediapipe timestamp errors on m-series chips.

## setup and installation

it's best to run this inside a virtual environment (venv) so you don't mess up your global python packages.

```bash
# create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# install the required dependencies (including pyobjc for mac support)
pip install opencv-python mediapipe pyautogui pyobjc-core pyobjc
