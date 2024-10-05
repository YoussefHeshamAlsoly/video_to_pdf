import os
import datetime
import cv2
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from util.progress_bar import progress_bar
import threading


def save_frames_as_images(method, frames, output_path):
    if not frames:
        print("No frames to export.")
        return [], ""
    
    current_time = datetime.datetime.now().strftime("%d.%m.%Y__%H.%M.%S")
    
    # Folder to store frames (for manual processing/backup if needed)
    # if output_path == None:
    if output_path != None and os.path.exists(output_path) and os.path.isdir(output_path):
        original_frames_folder = f"Extracted_Frames_{method}_{current_time}"
        original_frames_folder = os.path.join(output_path, original_frames_folder)
    else:
        original_frames_folder = f"Extracted_Frames_{method}_{current_time}"
    
    if not os.path.exists(original_frames_folder):
        os.makedirs(original_frames_folder)

    image_paths = []
    print(f"Saving extracted frames to folder '{os.path.abspath(original_frames_folder)}'")
    
    max_threads = max(1, os.cpu_count() // 4)  # Ensure at least one thread is used
    
    def save_frame(i, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image_path = os.path.join(original_frames_folder, f"frame_{i}.jpeg")
        Image.fromarray(rgb_frame).save(image_path)
        image_paths.append(image_path)
        progress_bar(len(image_paths), len(frames))

    threads = []
    for i, frame in enumerate(frames):
        thread = threading.Thread(target=save_frame, args=(i, frame))
        threads.append(thread)
        thread.start()

        # Limit number of concurrent threads
        if len(threads) >= max_threads:
            for thread in threads:
                thread.join()
            threads = []
    
    # Ensure all threads complete
    for thread in threads:
        thread.join()

    progress_bar(len(frames), len(frames))

    return image_paths, current_time


def combine_images_to_pdf(method, image_paths, output_path, current_time):
    if not image_paths:
        print("No images to combine into a PDF.")
        return

    # if output_path == None:
    if output_path != None and os.path.exists(output_path) and os.path.isdir(output_path):
        pdf_path = f"output_frames_{method}_{current_time}.pdf"
        pdf_path = os.path.join(output_path, pdf_path)
    else:
        pdf_path = f"output_frames_{method}_{current_time}.pdf"

    c = canvas.Canvas(pdf_path)

    def process_image(image_path):
        image = Image.open(image_path)
        width, height = image.size
        c.setPageSize((width, height))
        c.drawImage(image_path, 0, 0, width=width, height=height)
        c.showPage()
    
    print("\nCreating a PDF from extracted images")

    try:
        threads = []
        for i, image_path in enumerate(image_paths):
            progress_bar(i, len(image_paths))
            
            # Create a thread for each image processing task
            thread = threading.Thread(target=process_image, args=(image_path,))
            threads.append(thread)
            thread.start()

        # Ensure all threads complete
        for thread in threads:
            thread.join()

        progress_bar(len(image_paths), len(image_paths))
        c.save()
        print(f"\nPDF exported successfully to {pdf_path}")

    except MemoryError:
        print("Program crashed.\nToo many pages. Consider a different threshold")
    except Exception as e:
        print("Program crashed due to the following error")
        print(e)

