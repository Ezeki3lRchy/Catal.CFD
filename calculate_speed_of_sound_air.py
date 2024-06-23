import math


def calculate_speed_of_sound(temperature_kelvin):
    # Define constants
    gamma = 1.4  # Adiabatic index for air
    R = 287.0  # Gas constant for air (J/(kg·K))

    # Convert Celsius temperature to Kelvin
    temperature_kelvin = temperature_kelvin

    # Calculate the speed of sound
    speed_of_sound = math.sqrt(gamma * R * temperature_kelvin)

    return speed_of_sound


def calculate_mach_number(object_speed, temperature_kelvin):
    # Calculate the speed of sound at the given temperature
    speed_of_sound = calculate_speed_of_sound(temperature_kelvin)

    # Calculate the Mach number
    mach_number = object_speed / speed_of_sound

    return mach_number


# Example: Calculate the Mach number at 20 degrees Celsius for an object traveling at 340 m/s
temperature_kelvin = 393
object_speed = 4000  # speed of the object in m/s
mach_number = calculate_mach_number(object_speed, temperature_kelvin)
print(
    f"At {temperature_kelvin} Kelvin, an object traveling at {object_speed} m/s has a Mach number of {mach_number:.2f}")
