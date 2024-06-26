import adafruit_tcs34725
import busio
import board

def get_color():
    # Initialize I2C bus
    i2c = busio.I2C(board.SCL, board.SDA)
    
    # Create an instance of the TCS34725 sensor
    sensor = adafruit_tcs34725.TCS34725(i2c)

    # Enable the sensor (it might be enabled by default)
    sensor.integration_time = 0xD5  # Integration time can be adjusted
    sensor.gain = 0x01  # Gain can be adjusted

    # Read the raw color values
    r, g, b, c = sensor.color_raw

    # Print the raw color values for debugging
    print(f"Raw color values - Red: {r}, Green: {g}, Blue: {b}, Clear: {c}")

    # Determine the detected color based on RGB values
    if r > 200 and g > 200 and b > 200:
        return "White"
    elif r > g and r > b:
        return "Red"
    elif g > r and g > b:
        return "Green"
    elif b > r and b > g:
        return "Blue"
    elif r > 100 and g > 100 and b < 100:
        return "Yellow"
    elif r > 100 and g < 100 and b > 100:
        return "Purple"
    elif r < 100 and g > 100 and b > 100:
        return "Cyan"
    else:
        return "Unknown"

# Example usage
detected_color = get_color()
print("Color detectado:", detected_color)
