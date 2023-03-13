# AnimationTool
A Bad Animation Tool (that will probably never be finished or made into something useful)

You can run this with python, but it has a few requirements. Pygame, tkinter, and easy gui need to be installed. The commands to install these that should work if you have python setup:
```
pip install pygame
pip install tkinter
pip install easygui
```

## What you need to know to make something with it

| Keys | Function |
|-----:|---------------|
|left click|selects things|
|right click|click and drag to move camera|
|esc|resets frame, timeline zoom, and camera position in case something weird happens|
|     o|toggles Onion Skin (showing last/next frame)               |
|     tab|adds a frame aftetr the current one with the same object positions          |
|    backspace |deletes the frame that is being viewed               |
|space|plays animation from current frame onwards|
|left arrow|changes viewed frame to the next|
|right arrow|changes viewed frame to the previous|

**When you add an object it spawns above the camera area**
Each object has several circles which you can click and drag to modify it's state in the current frame.

| Color | Function |
|-----:|---------------|
|yellow|position|
|green|scale|
|blue|rotation|
|pink|current spritesheet frame (only on spritesheets)|

<sub>Note: rotation rotates the sprite before it is scaled, this means it will have a resolution of the original image and will fit inside said resolution even if the rotation would normally require it to be outside it. You can change this by changing the order of pygame.scale() and pygame.rotate) in each of the objects.</sub>

That *should* be about it, though it has many small bugs and quirks. Probably not what you want to use to make much of anything with, this is something I made for fun.
