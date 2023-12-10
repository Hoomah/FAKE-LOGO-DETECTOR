import cv2
from skimage.metrics import structural_similarity as ssim
import os
from tkinter import filedialog
from tkinter import Tk

# Get the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# Resize function
def resize_image(img, width, height):
    return cv2.resize(img, (width, height))

try:
    # Use Tkinter to open a file dialog for image selection
    root = Tk()
    root.withdraw()  # Hide the main window
    uploaded_img_path = filedialog.askopenfilename(title="Select an image for comparison", filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    root.destroy()  # Close the Tkinter window after selection

    if not uploaded_img_path:
        print("No image selected. Exiting.")
        exit()

    # Load the uploaded image
    uploaded_img = cv2.imread(uploaded_img_path)

    if uploaded_img is None:
        raise ValueError(f"Error: Uploaded image not loaded: {uploaded_img_path}")

    # Resize the uploaded image to a consistent size
    resize_width = 100  # Set your desired width
    resize_height = 100  # Set your desired height
    uploaded_img_resized = resize_image(uploaded_img, resize_width, resize_height)

    # Path to the dataset folder containing real logo images
    dataset_folder = os.path.join(current_dir, "real_logos")

    # Iterate through the images in the dataset folder
    for filename in os.listdir(dataset_folder):
        if filename.endswith(('.jpg', '.jpeg', '.png')):  # Filter out non-image files
            # Construct path for the dataset image
            dataset_img_path = os.path.join(dataset_folder, filename)

            # Load the dataset image
            dataset_img = cv2.imread(dataset_img_path)

            if dataset_img is None:
                raise ValueError(f"Error: Dataset image not loaded: {dataset_img_path}")

            # Resize the dataset image to a consistent size
            dataset_img_resized = resize_image(dataset_img, resize_width, resize_height)

            # Calculate SSIM for the pair of images with an explicitly specified window size (e.g., 3x3)
            similarity_index, _ = ssim(uploaded_img_resized, dataset_img_resized, full=True, win_size=3)

            # Set a threshold for the SSIM
            threshold = 0.70  # Adjust this threshold as needed

            # Check if the logos are fake or real based on the threshold
            if similarity_index > threshold:
                print(f"Real logo detected. Similarity: {similarity_index}")
                break  # Stop comparing once a match is found
    else:
        print("Fake logo detected")

except Exception as e:
    print(f"An error occurred: {e}")
