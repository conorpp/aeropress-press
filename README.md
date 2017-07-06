Based on 2 stepper motors, some compression springs, and limit switches.
It uses some microcontroller and stepper drivers.

It will have two buttons, "go" and "reset".

### Go

**State 1, fast press**:  The press quickly falls until it contacts the aeropress and the first limit switch on the sensor
plate is activated.

**State 2, Slow press**:  Compresses the aeropress slowly, at some user defined rate for your favorite brew.  It eventually
compresses it completely and will start compression the springs at the bottom, eventually hitting another limit switch.

**State 3, Reset**: Raises the press completely, until top limit switch is hit.

### Reset

See state 3, Reset.

![](/images/draft.png)

It requires five plates to be 3D printed.  And on the BOM there will be:

* 4 compression springs
* 2 stepper motors w/ drivers
* some MCU breakout, probably arduino
* 2 limit switches
* 8 nylon bearings
* 2 lead screws
* 4 smooth rods
* buttons

In progress.

