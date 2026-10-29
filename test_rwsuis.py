from rwsuis import RWS

# help(RWS) # display useful help on package
norbertIP = "http://152.94.160.198"
robot = RWS.RWS(norbertIP)
# wrd = robot.get_rapid_variable("WRD")
# if (wrd==0): 
 #    print(" Robot is waiting for Python to set ’ WPW ’ ")
( tr , rot ) = robot.get_robtarget_variables("target_K2")
print(tr)
# print(f"Translation for ’ p1 ’ is x ={ tr [0]:.2 f } , y ={ tr [1]:.2 f } , ={ tr [2]:.2 f } " )

new_rt = [0 ,0 ,314]
