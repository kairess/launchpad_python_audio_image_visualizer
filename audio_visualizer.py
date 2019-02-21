# original code from https://github.com/Joeyyi/python-audio-visualizer
import sys, math, wave, numpy, pygame, random
from pygame.locals import *
from scipy.fftpack import dct
import launchpad_py as launchpad

lp = launchpad.Launchpad();

lp = launchpad.LaunchpadMk2()
if lp.Open(0, 'mk2'):
  print('Launchpad Mk2')

lp.LedCtrlString(' HELLO', red=255, green=0, blue=255, direction=-1, waitms=77)
lp.LedCtrlString('WORLD! ', red=0, green=255, blue=255, direction=-1, waitms=77)

N = 8 # num of bars
HEIGHT = 400 # height of a bar
WIDTH = 50 # width of a bar
FPS = 20

file_name = sys.argv[1]
status = 'stopped'
fpsclock = pygame.time.Clock()

# screen init, music playback
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode([N * WIDTH, 50 + HEIGHT]) 
pygame.display.set_caption('Audio Visulizer')
my_font = pygame.font.SysFont('consolas', 16)
pygame.mixer.music.load(file_name) # need 16bit *.wav file
pygame.mixer.music.play()
pygame.mixer.music.set_endevent()
status = "playing"

# process wave data
f = wave.open(file_name, 'rb')
params = f.getparams()
nchannels, sampwidth, framerate, nframes = params[:4]
str_data  = f.readframes(nframes)  
f.close()  
wave_data = numpy.fromstring(str_data, dtype = numpy.short)  
wave_data.shape = -1,2  
wave_data = wave_data.T  


num = nframes

def visualizer(num):
  num = int(num)
  h = abs(dct(wave_data[0][nframes - num:nframes - num + N], type=1).astype(int))
  h = [min(HEIGHT,int(i **(1 / 2.5) * HEIGHT / 50)) for i in h]

  draw_bars(h)

def vis(status):
  lp.Reset()

  global num
  if status == "stopped":
    num = nframes
    return
  elif status == "paused":
    visualizer(num)
  else:
    num -= framerate/FPS
    if num > 0:
      visualizer(num)

def get_time(): 
  seconds = max(0, pygame.mixer.music.get_pos()/1000)
  m, s = divmod(seconds, 60)
  h, m = divmod(m, 60)
  hms = ('%02d:%02d:%02d' % (h, m, s))
  return hms

def controller(key):
  global status
  if status == 'stopped':
    if key == K_RETURN:
      pygame.mixer.music.play()
      status = 'playing'
  elif status == 'paused':
    if key == K_RETURN:
      pygame.mixer.music.stop()
      status = 'stopped'
    elif key == K_SPACE:
      pygame.mixer.music.unpause()
      status = 'playing'
  elif status == 'playing':
    if key == K_RETURN:
      pygame.mixer.music.stop()
      status = 'stopped'
    elif key == K_SPACE:
      pygame.mixer.music.pause()
      status = 'paused'



def draw_bars(h):
  bars = []
  for idx, i in enumerate(h):
    bars.append([len(bars) * WIDTH,50 + HEIGHT-i,WIDTH - 1,i])

    yh = numpy.rint(i / WIDTH).astype(int)

    for y in range(yh):
      color = lp.LedGetColorByName('white')
      lp.LedCtrlXYByCode(7-idx, 8-y, color)
    
    time_sec = max(0, pygame.mixer.music.get_pos()/1000)
    if 18 < time_sec < 49:
      lp.LedCtrlXYByCode(idx, yh, lp.LedGetColorByName('red'))
    if 126 < time_sec < 157:
      lp.LedCtrlXYByCode(idx, yh, 40)
    if 49 < time_sec < 64:
      for y in range(
        numpy.random.choice(9, 1, p=[0., 0.1, 0.2, 0.1, 0.2, 0.2, 0.05, 0.05, 0.1])[0]
      ):
        lp.LedCtrlXYByCode(8, 8-y, 53)

  for i in bars:
    pygame.draw.rect(screen,[255,255,255],i,0)

while True:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      lp.Reset()
      lp.Close()
      sys.exit()
    elif event.type == KEYDOWN:
      controller(event.key)

  if num <= 0:
    status = 'stopped'

  name = my_font.render(file_name, True, (255,255,255))
  info = my_font.render(status.upper() + ' ' + get_time(), True, (255,255,255))
  screen.fill((0,0,0))
  screen.blit(name,(0, 0))
  screen.blit(info,(0, 18))
  fpsclock.tick(FPS)
  vis(status)

  pygame.display.update()

