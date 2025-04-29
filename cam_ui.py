import tkinter as tk
from tkinter import Label
import requests
from PIL import Image, ImageTk
import io

# Replace with the actual IP address of your ESP32-CAM stream
camera_url = "http://192.168.1.48/stream"  # Adjust the URL as needed

# Create the main window
root = tk.Tk()
root.title("ESP32-CAM Stream Viewer")

# Set window size
root.geometry("640x480")

# Create a label to display the image
label = Label(root)
label.pack()

# Function to get the next JPEG frame from the MJPEG stream
def get_mjpeg_frame():
    try:
        # Make a request to the camera stream URL
        response = requests.get(camera_url, stream=True)
        byte_data = b""
        
        # Read data in chunks
        for chunk in response.iter_content(chunk_size=1024):
            byte_data += chunk
            
            # Check if the chunk contains the boundary for an image frame
            if b'\xff\xd8' in byte_data and b'\xff\xd9' in byte_data:
                # We have a complete JPEG frame
                start_idx = byte_data.find(b'\xff\xd8')  # JPEG start byte
                end_idx = byte_data.find(b'\xff\xd9') + 2  # JPEG end byte
                
                # Extract the complete image data
                jpeg_data = byte_data[start_idx:end_idx]
                
                # Convert to an image using PIL
                img = Image.open(io.BytesIO(jpeg_data))
                return img
                
                # Reset byte_data for the next frame
                byte_data = byte_data[end_idx:]
        
        return None
    except Exception as e:
        print(f"Error fetching frame: {e}")
        return None

# Update the UI with the next frame
def update_frame():
    img = get_mjpeg_frame()
    
    if img:
        # Resize to fit the window size
        img = img.resize((640, 480))
        
        # Convert image to ImageTk format and update the label
        img_tk = ImageTk.PhotoImage(img)
        label.config(image=img_tk)
        label.image = img_tk

    # Call the update_frame function every 100ms to keep updating the stream
    root.after(100, update_frame)

# Start the stream
update_frame()

# Start the Tkinter main loop
root.mainloop()
