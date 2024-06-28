import adafruit_tcs34725
import busio
import board

def get_color():
    try:
        # Initialize I2C bus
        i2c = busio.I2C(board.SCL, board.SDA)

        # Create an instance of the TCS34725 sensor
        sensor = adafruit_tcs34725.TCS34725(i2c)

        # Enable the sensor
        sensor.integration_time = 0xD5
        sensor.gain = 0x01

        # Read the raw color values
        r, g, b, c = sensor.color_raw

        # Normalize the values
        max_val = max(r, g, b)
        r_norm = r / max_val
        g_norm = g / max_val
        b_norm = b / max_val

        # Print the raw and normalized color values for debugging
        print(f"Raw color values - Red: {r}, Green: {g}, Blue: {b}, Clear: {c}")
        print(f"Normalized values - Red: {r_norm:.2f}, Green: {g_norm:.2f}, Blue: {b_norm:.2f}")

        # Determine the detected color based on normalized RGB values
        if r_norm > 0.8 and g_norm > 0.8 and b_norm > 0.8:
            color = "White"
        elif r_norm > 0.6 and r_norm > g_norm and r_norm > b_norm and g < 25:
            color = "Orange"
        elif b_norm > 0.6 and b_norm > g_norm and b_norm > r_norm:
            color = "Blue"
        elif max(r_norm, g_norm, b_norm) < 0.4:
            color = "Gray"
        else:
            color = "Unknown"

        return color

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

while True:
    print(get_color())