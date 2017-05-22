from Arduino import Arduino
from Tracking import tracking
from time import sleep

def alloff():
    board.digitalWrite(LEDpin0, "LOW")
    board.digitalWrite(LEDpin1, "LOW")
    board.digitalWrite(LEDpin2, "LOW")
    return

def allon():
    board.digitalWrite(LEDpin0, "HIGH")
    board.digitalWrite(LEDpin1, "HIGH")
    board.digitalWrite(LEDpin2, "HIGH")
    return

def allflash():
    board.digitalWrite(LEDpin0, "HIGH")
    board.digitalWrite(LEDpin1, "HIGH")
    board.digitalWrite(LEDpin2, "HIGH")
    sleep(.2)
    board.digitalWrite(LEDpin0, "LOW")
    board.digitalWrite(LEDpin1, "LOW")
    board.digitalWrite(LEDpin2, "LOW")
    sleep(.2)
    return


if __name__ == "__main__":

    LEDpin0 = 3
    BUTpin0 = 11
    LEDpin1 = 4
    BUTpin1 = 12
    LEDpin2 = 5
    BUTpin2 = 13

    baud = "9600"
    board = Arduino(baud)

    board.pinMode(LEDpin0, "OUTPUT")
    board.pinMode(LEDpin1, "OUTPUT")
    board.pinMode(LEDpin2, "OUTPUT")
    board.pinMode(BUTpin0, "INPUT")
    board.pinMode(BUTpin1, "INPUT")
    board.pinMode(BUTpin2, "INPUT")


    # first, get starting cup
    startingcup = 0
    while True:

        for i in range(0, 3):
            allflash()

        print("ready")
        while True:
            but0 = board.digitalRead(BUTpin0)
            but1 = board.digitalRead(BUTpin1)
            but2 = board.digitalRead(BUTpin2)

            if but0 == 1:
                board.digitalWrite(LEDpin0, "HIGH")
                startingcup = 0
                break

            if but1 == 1:
                board.digitalWrite(LEDpin1, "HIGH")
                startingcup = 1
                break

            if but2 == 1:
                board.digitalWrite(LEDpin2, "HIGH")
                startingcup = 2
                break

        sleep(.5)
        alloff()

        result = tracking(board, startingcup)
        print("resulting position: " + str(result))
        if result == 0:
            board.digitalWrite(LEDpin0, "HIGH")
        if result == 1:
            board.digitalWrite(LEDpin1, "HIGH")
        if result == 2:
            board.digitalWrite(LEDpin2, "HIGH")
        del (result)
        sleep(5)


