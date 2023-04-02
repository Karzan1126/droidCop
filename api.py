from flask import Flask, render_template
import RPi.GPIO as GPIO

app = Flask(_name_)

pins = (11,12) #pins is a dict

GPIO.setmode(GPIO.BOARD) #Numbers GPIOs by physical location
GPIO.setup(pins, GPIO.OUT) #set pins' node is output
GPIO.outout(pins, GPIO.LOW) # set pins to LOW(0V) to off led

p_R = GPIO.PWM(pins[0],2000) # Set freq to 2 KHz
p_G = GPIO.PWM(pins[1], 2000)

def map (x, in_min, in_max, out_min, out_max):
    return(x - in_min) * (out_max - out_min)/(in_max - in_min) + out_min

def setColor(col):
    R_val = col >> 8
    G_val = col & 0x00FF
    
    R_val = map(R_val,0,255,0,100)
    G_val = map(G_val,0,255,0,100)
    
    p_R.ChangeDutyCycle(R_val) #change duty cycle
    p_G.ChangeDutyCycle(G_val)
    
@app.route('/on')
def on():
    p_R.start(0) #Initial duty cycle = 0 (LEDs off)
    p_G.start(0)
    setColor(0xFF00)
    return render_template('dchomepage.html')

@app.route('/off')
def off():
    p_R.stop()
    p_G.stop()
    GPIO.output(pins,GPIO.LOW)
    return render_template('dcoperation.html')
    