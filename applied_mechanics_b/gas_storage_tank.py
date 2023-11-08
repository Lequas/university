# This python script calculates the minimum diamater needed for the two bolts which fix a gas storage tank into the foundations at Port Botany.

import numpy as np

σ_allowable = 140000000  # Allowable shear stress in Pa
#wind_speed = 151.9 * (10 / 36)  # m/s     All time record
wind_speed = 92.5 * (10 / 36)  # m/s       Max for this year
FoS = 1.5
num_bolts = 2

radius = 3
width = 12
height = radius * 2
area = width * height

print(f'Tank:\nRadius = {radius}m\nHeight = {height}m\nWidth = {width}m\nArea = {area}m^2')

qs = 0.5 * 1.225 * wind_speed**2 

wind_load = qs * area
v = wind_load / num_bolts

d_min = np.sqrt((4 * v) / (np.pi * σ_allowable))

bolt_diameter = d_min * FoS * 1000  # Convert to mm

def find_next_standard_bolt(bolt_diameter):
    standard_bolt_sizes = {
        "M6": 6,
        "M8": 8,
        "M10": 10,
        "M12": 12,
        "M14": 14,
        "M16": 16,
        "M18": 18,
        "M20": 20,
        "M22": 22,
        "M24": 24,
        "M27": 27,
        "M30": 30,
        "M33": 33,
        "M36": 36,
        "M39": 39,
        "M42": 42,
        "M45": 45,
        "M48": 48,
    }

    sorted_bolt_sizes = sorted(standard_bolt_sizes.values())
    
    for size in sorted_bolt_sizes:
        if size > bolt_diameter:
            for key, value in standard_bolt_sizes.items():
                if value == size:
                    return f"{key} is the next standard bolt size up from {round(bolt_diameter,2)} mm."
    
    return "No standard bolt size found larger than the provided diameter."


print(f'Wind load: {round(wind_load,2)} N')
print(f'Bolt diameter calculated: {round(bolt_diameter, 2)} mm')
result = find_next_standard_bolt(bolt_diameter)
print(result)
