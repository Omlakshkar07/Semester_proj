import requests
from tqdm import tqdm
import os
import sys

def download_yolov9_weights(url="https://github.com/WongKinYiu/yolov9/releases/download/v0.1/yolov9-c.pt", output_path="yolov9-c.pt"):
    """
    Download YOLOv9 weights with progress bar and error handling
    
    Args:
        url (str): URL to download the weights from
        output_path (str): Path where to save the weights file
    """
    try:
        # Check if file already exists
        if os.path.exists(output_path):
            print(f"File {output_path} already exists. Skipping download.")
            return True
            
        # Send a HEAD request first to get the file size
        response = requests.head(url, allow_redirects=True)
        file_size = int(response.headers.get('content-length', 0))

        # Start the download
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Setup progress bar
        progress_bar = tqdm(
            total=file_size,
            unit='iB',
            unit_scale=True,
            desc=f"Downloading {output_path}"
        )

        # Write the file
        with open(output_path, 'wb') as file:
            for data in response.iter_content(chunk_size=1024):
                size = file.write(data)
                progress_bar.update(size)
        
        progress_bar.close()
        
        # Verify file size
        actual_size = os.path.getsize(output_path)
        if actual_size != file_size:
            raise Exception("Downloaded file size doesn't match expected size")
            
        print(f"\nSuccessfully downloaded {output_path}")
        return True

    except requests.exceptions.RequestException as e:
        print(f"Network error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        # Clean up partial download if it exists
        if os.path.exists(output_path):
            os.remove(output_path)
            print(f"Removed partial download: {output_path}")
    return False

if __name__ == "__main__":
    # Available YOLOv9 model versions
    models = {
        'yolov9-c': 'https://github.com/WongKinYiu/yolov9/releases/download/v0.1/yolov9-c.pt',
        'yolov9-e': 'https://github.com/WongKinYiu/yolov9/releases/download/v0.1/yolov9-e.pt',
        'yolov9-s': 'https://github.com/WongKinYiu/yolov9/releases/download/v0.1/yolov9-s.pt'
    }
    
    # Default to yolov9-c model
    model_url = models['yolov9-c']
    model_name = 'yolov9-c.pt'
    
    download_yolov9_weights(model_url, model_name)