#Python coding challenges
#All rights reserved - these challenges are provided by OCR on their website
#The link - https://www.ocr.org.uk/images/260930-coding-challenges-booklet.pdf

from tkinter import *
from tkinter.ttk import *
from datetime import datetime, timedelta

import random, webbrowser, time, sys, os

lengthsConvDict = {"KilometerMeter":1000,"KilometerCentimeter":100000,"KilometerMile":0.621,"KilometerFoot":3281,"KilometerInch":39370,
                   "MeterKilometer":0.001,"MeterCentimeter":100,"MeterMile":0.000621,"MeterFoot":3.281,"MeterInch":39.37,
                   "CentimeterKilometer":0.00001,"CentimeterMeter":0.01,"CentimeterMile":0.00000621,"CentimeterFoot":0.0328,"CentimeterInch":0.393701,
                   "MileKilometer":1.6,"MileMeter":1600,"MileCentimeter":160000,"MileFoot":5280,"MileInch":63360,
                   "FootKilometer":0.0003048,"FootMeter":0.3048,"FootCentimeter":30.48,"FootMile":0.000189,"FootInch":12,
                   "InchKilometer":0.0000254,"InchMeter":0.0254,"InchCentimeter":2.54,"InchMile":0.0000158,"InchFoot":0.0833}
massConvDict = {"TonneKilogram":1000,"TonneGram":1000000,"TonnePound":2205,"TonneStone":157.5,
                "KilogramTonne":0.001,"KilogramGram":1000,"KilogramPound":2.205,"KilogramStone":0.157,
                "GramTonne":0.000001,"GramKilogram":0.001,"GramPound":0.0022,"GramStone":0.000157,
                "PoundTonne":0.000454,"PoundKilogram":0.454,"PoundGram":454,"PoundStone":0.0714,
                "StoneKilogram":6.35,"StoneGram":6350,"StoneTonne":0.00635,"StonePound":14}
speedConvDict = {"Meter per secondKm per Hour":3.6,"Meter per secondMile per Hour":2.237,
                 "Km per HourMeter per second":0.278,"Km per HourMile per Hour":0.621,
                 "Mile per HourMeter per second":0.447,"Mile per HourKm per Hour":1.6}
timeConvDict = {"SecondMinute":0.0167,"SecondHour":0.000278,"SecondDay":0.0000116,"SecondMonth":0.00000038,"SecondYear":0.00000003,
                "MinuteSecond":60,"MinuteHour":0.0167,"MinuteDay":0.00069,"MinuteMonth":0.0000228,"MinuteYear":0.0000019,
                "HourSecond":3600,"HourMinute":60,"HourDay":0.0417,"HourMonth":0.00137,"HourYear":0.00011,
                "DaySecond":86400,"DayMinute":1440,"DayHour":24,"DayMonth":0.033,"DayYear":0.0027,
                "MonthSecond":2628000,"MonthMinute":43800,"MonthHour":730,"MonthDay":30.4,"MonthYear":0.083,
                "YearSecond":31540000,"YearMinute":525600,"YearHour":8760,"YearDay":365,"YearMonth":12}                   

class tkinter_window(Tk):
    def __init__(self):
        super().__init__()
        self.title('Computer science coding challenges')
        Button(self,text='Coding challenges booklet (by OCR)',command=self.open_link).grid(row=0, columnspan=3)
        Button(self,text='Close',command=self.destroy).grid(row=10, columnspan=3)

    def open_link(self):
        webbrowser.open('https://www.ocr.org.uk/images/260930-coding-challenges-booklet.pdf')

class Task2(tkinter_window):
    def __init__(self):
        super().__init__()

        distance = 100*random.randint(1,100)
        text = f'The distance between the cameras is: {distance/1600} miles'

        Label(self,text='Enter time for first speed camera (hr:min:sec) : ').grid(row=1, column=0)
        Label(self,text='Enter time for second speed camera (hr:min:sec) : ').grid(row=2, column=0)
        Label(self,text='Enter a valid number plate [XX11 XXX] : ').grid(row=4,column=0)
        Label(self,text=text).grid(row=3, columnspan=3)

        self.time1 = Entry(self)
        self.time2 = Entry(self)
        self.plate = Entry(self)

        self.time1.grid(row=1, column=1)
        self.time2.grid(row=2, column=1)
        self.plate.grid(row=4, column=1)

        Button(self,text='Calculate speed',command=lambda: self.calculate_speed1(distance)).grid(row=7,columnspan=3)

    def calculate_speed1(self, distance):
        time2 = self.time2.get()
        time1 = self.time1.get()
        number_plate = self.plate.get()
        plateValid = self.check_plate(number_plate)
        if plateValid:
            thatText = "The car\'s registration plate is valid"
        else:
            thatText = "The car\'s registration plate is not valid"
        try:
            time2 = datetime.strptime(time2, '%H:%M:%S')
            time1 = datetime.strptime(time1, '%H:%M:%S')
            timeDif = time2 - time1
            timeDif = timeDif.total_seconds()
            speed = self.calculate_speed2(distance, timeDif)
            thisText = f'The average speed of the car was: {speed} mph'
        except:
            thisText = "Please enter time format for time (hr:min:sec)!"
        Label(self,text=thisText).grid(row=5, columnspan=3)
        Label(self,text=thatText).grid(row=6, columnspan=3)

    def calculate_speed2(self, distance, timeDif):
        speed1 = distance / timeDif
        speed2 = ((speed1 / 1000) * 3600) / 1.6
        speed2 = round(speed2, 2)
        return speed2

    def check_plate(self, number_plate):
        plateValid = True
        number_plate = number_plate.replace(" ", "")
        if len(number_plate) != 7:
            plateValid = False
        elif not number_plate[0].isalpha() or \
        not number_plate[1].isalpha() or \
        not number_plate[2].isdigit() or \
        not number_plate[3].isdigit() or \
        not number_plate[4].isalpha() or \
        not number_plate[5].isalpha() or \
        not number_plate[6].isalpha():
            plateValid = False
        return plateValid

    def generate_test_entries(self, entry_count):
        alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
        while entry_count >= 0:
            plate1 = "".join(random.choice(alphabet) for _ in range(0, 4))
            plate2 = "".join(random.choice(alphabet) for _ in range(0, 3)) 
            number_plate = plate1+" "+plate2

            start_time = datetime.now()
            end_time = start_time + timedelta(
                minutes=random.randrange(120),
                seconds=random.randrange(120)
            )
            distance = 100*random.randint(1,100)
            yield number_plate, start_time.time(), end_time.time(), distance
            entry_count = entry_count - 1

    def write_to_file(self, entries):
        for plate, start, end, distance in self.generate_test_entries(99):
            entries.append(f"{plate} | {start} | {end} | {distance}\n")
            
        with open("test_data", "w") as f:
            f.writelines(entries)
        
    def read_entry(self, entry_string):
        entry = entry_string.split(" | ")
        start_time = datetime.strptime(entry[1], "%H:%M:%S.%f")
        end_time = datetime.strptime(entry[2], "%H:%M:%S.%f")
        distance = int(entry[3])
        return entry[0], start_time, end_time, distance

    def read_file(self):
        with open("test_data", "r") as f:
            count = 1
            speedingCount = 0
            validCount = 0
            for line in f.readlines():
                number_plate, start, end, distance = self.read_entry(line)
                difference = end - start
                difference = difference.total_seconds()
                speed = self.calculate_speed2(distance, difference)
                valid = self.check_plate(number_plate)
                speeding = speed > 70
                if speeding:
                    speedingCount += 1
                if valid:
                    validCount += 1
                print(f"[{count}] Plate={number_plate} (valid?: {valid}), speed={speed} mph (speeding?: {speeding})")
                count += 1
            print(f'There were {speedingCount} cars speeding')
            print(f'There were {validCount} cars with valid registration plates')
    
class Task3(tkinter_window):
    def __init__(self):
        super().__init__()

        Label(self,text='Enter in below the four digits').grid(row=1, columnspan=4)

        self.num1 = IntVar()
        self.num2 = IntVar()
        self.num3 = IntVar()
        self.num4 = IntVar()

        spin1 = Spinbox(self, textvariable=self.num1, from_=0, to =9)
        spin2 = Spinbox(self, textvariable=self.num2, from_=0, to =9)
        spin3 = Spinbox(self, textvariable=self.num3, from_=0, to =9)
        spin4 = Spinbox(self, textvariable=self.num4, from_=0, to =9)

        spin1.grid(row=2, column=0)
        spin2.grid(row=2, column=1)
        spin3.grid(row=2, column=2)
        spin4.grid(row=2, column=3)

        self.resultsBox = Text(self)
        self.resultsBox.grid(row=3, columnspan=4)

        Button(self,text='Display combinations',command=self.displayResults).grid(row=5,columnspan=4)

    def displayResults(self):
        self.resultsBox.delete(0.0, END)
        digits = []
        digit1 = self.num1.get()
        digit2 = self.num2.get()
        digit3 = self.num3.get()
        digit4 = self.num4.get()
        digits.append(digit1)
        digits.append(digit2)
        digits.append(digit3)
        digits.append(digit4)
        combinations = self.calc_combinations(digits)
        for combo in combinations:
            text = f'{combo} \n'
            self.resultsBox.insert(END, text)
        text = f'There are {len(combinations)} different combinations'
        self.resultsBox.insert(END, text)

    def calc_combinations(self, digits):
        combinations = []

        maxCombos = self.calulate_max_combos(digits)
        
        while len(combinations) < maxCombos:
            combo = ""
            random.shuffle(digits)
            for digit in digits:
                combo += str(digit)
            if combo not in combinations:
                combinations.append(combo)

        return combinations

    def calulate_max_combos(self, digits):
        num1 = len(digits)
        factorial1 = self.calc_factorial(num1)
        digitsDict = {}
        for item in digits:
            if (item in digitsDict):
                digitsDict[item] += 1
            else:
                digitsDict[item] = 1
        greatestNum = 1
        num3 = 1
        for num in digitsDict.values():
            if num > greatestNum:
                greatestNum = num
            elif num > 1 and num == greatestNum:
                num3 = num
        num2 = greatestNum
        factorial2 = self.calc_factorial(num2)
        factorial3 = self.calc_factorial(num3)
        max_combos = round((factorial1 / (factorial2 * factorial3)), 0)
        return max_combos
            
    def calc_factorial(self, num):
        factorial = 1
        for i in range(1,num + 1):
           factorial *= i
        return factorial

class Task6(tkinter_window):
    def __init__(self):
        super().__init__()

        self.state1 = StringVar()
        self.state2 = StringVar()
        self.state3 = StringVar()
        self.convertedNum = IntVar()

        Label(self, text='Enter the type of conversion:').grid(row=1, column=0)
        Label(self, text='Enter units and values below').grid(row=2, column=0)

        conversions = ["Length", "Mass", "Speed", "Temperature", "Time"]
        self.lengthUnits = ["Kilometer", "Meter", "Centimeter", "Mile", "Foot", "Inch"]
        self.massUnits = ["Tonne", "Kilogram", "Gram", "Pound", "Stone"]
        self.speedUnits = ["Meter per second", "Km per Hour", "Mile per Hour"]
        self.tempUnits = ["Celcius", "Kelvin", "Farenheit"]
        self.timeUnits = ["Second", "Minute", "Hour", "Day", "Month", "Year"]

        convTypes = Combobox(self, textvariable=self.state1, values=conversions)
        convTypes.grid(row=1, column=1)

        self.entry1 = Entry(self)
        entry2 = Entry(self, textvariable=self.convertedNum, state="disabled")

        self.entry1.grid(row=3, column=0)
        entry2.grid(row=3, column=2)

        Button(self, text='Confirm conversion type', command=self.setUnits).grid(row=5, column=1)
        Button(self, text='Convert', command=self.convert).grid(row=5, column=2)

    def setUnits(self):
        self.ConversionType = self.state1.get()
        if self.ConversionType == "Length":
            conversionUnits = self.lengthUnits
        elif self.ConversionType == "Mass":
            conversionUnits = self.massUnits
        elif self.ConversionType == "Speed":
            conversionUnits = self.speedUnits
        elif self.ConversionType == "Temperature":
            conversionUnits = self.tempUnits
        else:
            conversionUnits = self.timeUnits
        fromUnits = Combobox(self, textvariable=self.state2, values=conversionUnits)
        toUnits = Combobox(self, textvariable=self.state3, values=conversionUnits)
        fromUnits.grid(row=3, column=1)
        toUnits.grid(row=3, column=3)

    def convert(self):
        conversionFrom = self.state2.get()
        conversionTo = self.state3.get()
        num = self.entry1.get()
        if self.ConversionType == "Length":
            converted = self.LengthConversion(conversionFrom, conversionTo, num)
        elif self.ConversionType == "Mass":
            converted = self.MassConversion(conversionFrom, conversionTo, num)
        elif self.ConversionType == "Speed":
            converted = self.SpeedConversion(conversionFrom, conversionTo, num)
        elif self.ConversionType == "Temperature":
            converted = self.TemperatureConversion(conversionFrom, conversionTo, num)
        else:
            converted = self.TimeConversion(conversionFrom, conversionTo, num)
        self.convertedNum.set(converted)

    def LengthConversion(self, conversionFrom, conversionTo, num):
        conversion = conversionFrom+conversionTo
        if conversion in lengthsConvDict.keys():
            convFactor = lengthsConvDict[conversion]
        else:
            convFactor = 1
        return float(num) * convFactor

    def MassConversion(self, conversionFrom, conversionTo, num):
        conversion = conversionFrom+conversionTo
        if conversion in massConvDict.keys():
            convFactor = massConvDict[conversion]
        else:
            convFactor = 1
        return float(num) * convFactor

    def SpeedConversion(self, conversionFrom, conversionTo, num):
        conversion = conversionFrom+conversionTo
        if conversion in speedConvDict.keys():
            convFactor = speedConvDict[conversion]
        else:
            convFactor = 1
        return float(num) * convFactor

    def TimeConversion(self, conversionFrom, conversionTo, num):
        conversion = conversionFrom+conversionTo
        if conversion in timeConvDict.keys():
            convFactor = timeConvDict[conversion]
        else:
            convFactor = 1
        return float(num) * convFactor

    def TemperatureConversion(self, conversionFrom, conversionTo, num):
        conversion = conversionFrom+conversionTo
        num = float(num)
        if conversion == "CelciusFarenheit":
            converted = (num * 1.8) + 32
        elif conversion == "CelciusKelvin":
            converted = num + 273
        elif conversion == "KelvinCelcius":
            converted = num - 273
        elif conversion == "KelvinFarenheit":
            converted = ((num - 273) * 1.8) + 32
        elif conversion == "FarenheitCelcius":
            converted = (num - 32) * (5/9)
        elif conversion == "FarenheitKelvin":
            converted = ((num - 32) * (5/9)) + 273
        else:
            converted = num
        return converted
        
def main():
    window = Task6()
    window.mainloop()

if __name__ == "__main__":
    main()
