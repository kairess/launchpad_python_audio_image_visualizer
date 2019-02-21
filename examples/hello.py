import sys
import launchpad_py as launchpad
import random

def main():
	lp = launchpad.Launchpad();

	lp = launchpad.LaunchpadMk2()
	if lp.Open(0, "mk2"):
		print("Launchpad Mk2")

	lp.LedCtrlString("Chloe ", red=255, green=0, blue=255, direction=-1, waitms=100)

	# Clear the buffer because the Launchpad remembers everything :-)
	lp.ButtonFlush()

	# butHit = 10
		
	# while 1:
	# 	# lp.LedCtrlRaw( random.randint(0,127), random.randint(0,63), random.randint(0,63), random.randint(0,63) )
		
	# 	# time.wait( 5 )
		
	# 	but = lp.ButtonStateRaw()

	# 	if but != []:
	# 		butHit -= 1
	# 		if butHit < 1:
	# 			break
	# 		print( butHit, " event: ", but )

	lp.Reset() # turn all LEDs off
	lp.Close()
	
if __name__ == '__main__':
  main()