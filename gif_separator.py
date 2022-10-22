import imageio.v3 as iio
import imageio
import json

path = 'assets/player_raw/'
name = 'rw.gif'
frames = iio.imread(path+name)
dots = 172, 56, 28, 80


iio.imwrite(f'{name.strip(".gif")}_output.gif', frames[:, dots[0]:dots[0]+dots[3]+1, dots[1]:dots[1]+dots[2]+1])
