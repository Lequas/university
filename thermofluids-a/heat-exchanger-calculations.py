import numpy as np
from rich.console import Console
from rich.table import Table
from rich.theme import Theme
from rich.text import Text
from rich.align import Align
from rich.style import Style

hotFlowRate = 3.37 * 1/60000 # m^3/sec
hotInlet    = 59.0 # Deg Celcius
hotOutlet   = 53.9 # Deg Celcius
hotAv       = (hotInlet+hotOutlet)/2

coldFlowRate = 4.00 * 1/60000 # m^3/sec
coldInlet    = 17.2 # Deg Celcius
coldOutlet   = 22.4 # Deg Celcius
coldAv = (coldInlet+coldOutlet)/2

hotDensity = 1000 * ( 1 - (hotAv+288.9414) / (508929*(hotAv+68.129630))*(hotAv - 3.9863)**2 )
coldDensity = 1000 * ( 1 - (coldAv+288.9414) / (508929*(coldAv+68.129630))*(coldAv - 3.9863)**2 )

c = 4.184 * 1000 # J/kg °C 
m = hotFlowRate * hotDensity
Q = m*c*(hotInlet - hotOutlet)  

R = (hotAv-coldAv)/Q

hotPipeRadius = 0.01 / 2 #meters
hotPipeArea = np.pi * hotPipeRadius**2
hotVelocity = hotFlowRate / hotPipeArea

coldPipeRadius = (0.020) / 2 #meters
coldPipeArea = ( np.pi * coldPipeRadius**2 ) - hotPipeArea 
coldVelocity = coldFlowRate / coldPipeArea

# Hot values
hotDynamicViscosity = 0.0004923 # N/m^2 at hotAv
hotReynolds = ( hotDensity*hotVelocity*2*hotPipeRadius ) / hotDynamicViscosity
hotK = 647.24995 / 1000 # W/m K interpolation
hotThermalDiffusivity = ( hotK / ( hotDensity * c) ) *1000
hotPr = hotDynamicViscosity / hotThermalDiffusivity
hotNu = 0.029 * hotReynolds**0.8 * hotPr**0.4
hotTransferCo = ( hotNu * hotK ) / (hotPipeRadius*2)

# Repeat for Cold Values
coldDynamicViscosity = 0.0017916 # N/m^2 at coldAv
coldReynolds = ( coldDensity*coldVelocity*2*coldPipeRadius ) / coldDynamicViscosity
coldK = 597.6422 / 1000 # W/m K interpolation
coldThermalDiffusivity = ( coldK / ( coldDensity * c) ) *1000
coldPr = coldDynamicViscosity / coldThermalDiffusivity
coldNu = 0.029 * coldReynolds**0.8 * coldPr**0.4
hydraulicDiameter = 0.020-0.012
coldTransferCo = ( coldNu * coldK ) / (hydraulicDiameter)#coldPipeRadius*2)

steelK = 15.1
r1 = 0.01/2 
r2 = 0.012/2
L = (steelK* (r1*hotTransferCo + r2*coldTransferCo ) + r1*r2*hotTransferCo*coldTransferCo * np.log(r2/r1)) / (2*np.pi *r1*r2 * hotTransferCo* coldTransferCo * steelK * R)







# Input Values Table
input_table = Table(show_header=True, header_style="bold cyan", title="Input Values", title_style="bold white")
input_table.add_column("Parameter", style="magenta", justify="center")
input_table.add_column("Hot", style="yellow", justify="center")
input_table.add_column("Cold", style="yellow", justify="center")
input_table.add_column("Unit", style="green", justify="center")
input_table.add_row("Flow Rate", str(round(hotFlowRate,5)), str(round(coldFlowRate, 5)), "m^3/sec")
input_table.add_row("Inlet Temp", str(hotInlet),str(coldInlet), "°C")
input_table.add_row("Outlet Temp", str(hotOutlet),str(coldOutlet), "°C")
input_table = Align.center(input_table, vertical="middle")

# Calculated Values
calculated_table = Table(show_header=True, header_style="bold cyan", title="Calculated Values", title_style="bold white")
calculated_table.add_column("Parameter", style="magenta", justify="center")
calculated_table.add_column("Hot", style="yellow", justify="center")
calculated_table.add_column("Cold", style="yellow", justify="center")
calculated_table.add_column("Unit", style="green", justify="center")
calculated_table.add_row("Average Temp", str(round(hotAv,3)),str(round(coldAv,3)), "°C")
calculated_table.add_row("Average Density", str(round(hotDensity,3)),str(round(coldDensity,3)), "kg/m^3")
calculated_table.add_row("Mass Flow Rate",  str(round(hotFlowRate*1000,3)),str(round(coldFlowRate*1000,3)), "g/sec")
calculated_table.add_row("Inlet Velocity", str(round(hotVelocity,3)),str(round(coldVelocity,3)) ,"m/s")
calculated_table.add_row("Heat Capacity", str(round(c,3)), str(round(c,3)), "J/kg °C")
calculated_table.add_row("Reynolds Number (Re)", str(round(hotReynolds,3)), str(round(coldReynolds,3)),"-")
calculated_table.add_row("Prandtl Number (Pr)", str(round(hotPr,3)),str(round(coldPr,3)),"-")
calculated_table.add_row("Nusselt Number (Nu)",str(round(hotNu,3)),str(round(coldNu,3)),"-")
calculated_table.add_row("Heat Transfer Coefficient", str(round(hotTransferCo,3)), str(round(coldTransferCo,3)),"-")
calculated_table = Align.center(calculated_table, vertical="middle")


# Output Values Table
output_table = Table(show_header=True, header_style="bold cyan", title="Output Values", title_style="bold white")
output_table.add_column("Parameter", style="magenta", justify="center")
output_table.add_column("Value", style="yellow", justify="center")
output_table.add_column("Unit", style="green", justify="center")
output_table.add_row("Heat Transfer Rate (Q)", str(round(Q,3)), "W")
output_table.add_row("Thermal Resistance (R)", str(round(R,3)),"°C/W")
output_table.add_row("Length", str(round(L,3)), "m")

output_table = Align.center(output_table, vertical="middle")


console = Console()
title = Text("\nDouble Pipe Heat Exchanger Calculations\n\n", style="b white u")
console.print(title, justify="center")
console.print(input_table )
console.print("")
console.print(calculated_table)
console.print("")
console.print(output_table)
console.print("")
console.print("The length of the double pipe heat exchanger is " + str(round(L*1000,5)) + " millimeters.\n", justify="center")
