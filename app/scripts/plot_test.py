import numpy as np
x=np.linspace(0,2*np.pi,30)
plt = plot(x, np.sin(x))
button('capture 1',"capture1('CH1',100,10)","update-plot",target=plt)

plt2 = plot(x, np.sin(x))
button('capture 2',"capture2(50,10)","update-plot",target=plt2,stacking='xyy')

plt3 = plot(x, np.sin(x))
button('capture 4',"capture4(50,10)","update-plot",target=plt3,stacking='xyyyy')
