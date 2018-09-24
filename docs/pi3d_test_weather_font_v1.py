import demo
import sys
if sys.version_info[0] == 3:
  unichr = chr

import pi3d

mytext = ''
for i in range(50):
  mytext = mytext + chr(0xf000 + i)
  if i % 7 == 0:
    mytext = mytext + '\n'# Setup display and initialise pi3d
DISPLAY = pi3d.Display.create(x=10, y=10, w=900, h=600, frames_per_second=25)
DISPLAY.set_background(0.4, 0.6, 0.8, 1.0)      # r,g,b,alpha

ortho_cam = pi3d.Camera(is_3d=False) # 2d orthographic view camera

flatsh = pi3d.Shader("uv_flat")

#load ttf font and set the font colour to 'raspberry'
arialFont = pi3d.Font("fonts/weathericons-regular-webfont.ttf",  (221,0,170,255),
                    codepoints=mytext)
arialFont.blend = True #much better anitaliased look but must String.draw() after everything else      
mystring = pi3d.String(font=arialFont, string=mytext,
                  camera=ortho_cam, z=1.0, is_3d=False, justify="r") # orthographic view
mystring.set_shader(flatsh)

# Fetch key presses.
mykeys = pi3d.Keyboard()

# Display scene and rotate shape
while DISPLAY.loop_running():
  mystring.draw()
  mystring.rotateIncZ(0.05)

  k = mykeys.read()
  if k==27:
    mykeys.close()
    DISPLAY.destroy()
    break
