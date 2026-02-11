import os
import logging # For logging errors and information
import shutil # For moving corrupted images
from PIL import Image, UnidentifiedImageError

# Create logs directory if it doesn't exist
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) # Get the project root directory i.e., three levels up from data_loader.py -- src/preprocessing/data_loader.py > src > preprocessing > project root named 'malaria_detection_project'. The __file__ variable points to the current file path which is data_loader.py
logs_dir = os.path.join(project_root, 'outputs', 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir, exist_ok=True)


# Configure logging
logging.basicConfig(
    filename=os.path.join(logs_dir, 'data_loader.log'), # Log file path i.e., malaria_detection_project/logs/data_loader.log
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class MalariaDataLoader:
    
    def __init__(self, root_dir):
        
        self.root_dir = root_dir
        self.classes = ['Parasitized', 'Uninfected']
        self.data = []
        self.corrupted_dir = os.path.join(self.root_dir, 'corrupted') # Directory to store corrupted images
        os.makedirs(self.corrupted_dir, exist_ok=True) # Create corrupted directory if it doesn't exist
        
    # Function to check if directories exist    
    def verify_directories(self):
        '''Verify if the required directories exist.'''
        
        for cls in self.classes:
            path = os.path.join(self.root_dir, cls) # Construct the path to the class directory
            
            if not os.path.exists(path):
                logging.error(f'Directory not found: {path} - Please check the dataset path.')
                raise FileNotFoundError(f'Directory {path} not found.')
     
    # Function to load images from directories        
    def clean_load_data_image(self):
        '''Load images data from the root directory and move corrupted image or non-image to corrupted folder.'''
        
        for cls in self.classes: 
            
            path = os.path.join(self.root_dir, cls) # Construct the path to the class directory
            
            # Iterate through each image in the class directory
            for img_name in os.listdir(path): # List all files in the class directory
                img_path = os.path.join(path, img_name) # Full path to the image which is root_dir/class_name/image_name
                
                # Process only image files with valid extensions
                if img_name.lower().endswith(('.png', '.jpg', '.jpeg','.gif')):
                    # Open and load the image and append image and class to data list
                    try:
                        img = Image.open(img_path).convert('RGB') # Convert image to RGB format
                        self.data.append((img, cls)) 
                    
                    except UnidentifiedImageError:
                        logging.warning(f'Corrupted image moved: {img_path}')
                        self._moved_to_corrupted(img_path) # Move corrupted image to corrupted directory
                        
                    except Exception as e:
                        logging.error(f'Unexpected error occurred while loading image {img_path}: {e}')
                        self._moved_to_corrupted(img_path) # Move corrupted image to corrupted directory

                # Handle non-image files(.txt, .csv, Thumbs.db, etc.)
                else:
                    logging.warning(f'Non-image file moved: {img_path}')
                    self._move_to_corrupted(img_path) # Move non-image files to corrupted directory
    # Helper function to move corrupted images
    def _move_to_corrupted(self, file_path):
        """Move bad images to corrupted folder"""
        try:
            dest_path = os.path.join(self.corrupted_dir, os.path.basename(file_path))
            shutil.move(file_path, dest_path)
            logging.info(f"Moved {file_path} → {dest_path}")
        except Exception as e:
            logging.error(f"Failed to move {file_path} to corrupted/: {e}")

                    
    # Function for summary of loaded data
    def data_summary(self):
        '''
        Print the summary of loaded data.
        '''
        counts = {
            cls: 0 for cls in self.classes # Initialize count dictionary for each class
        }
        for _, label in self.data:
            counts[label] += 1 # Increment the count for the corresponding class
            
        logging.info(f'Dataset summary: {counts}')
        
        return counts
    
    
# Example usage
if __name__ == "__main__":
    project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__))) # Get the project root directory i.e., three levels up from data_loader.py -- src/preprocessing/data_loader.py > src > preprocessing > project root named 'malaria_detection_project'. The __file__ variable points to the current file path which is data_loader.py
    dataset_path = os.path.join(project_root, 'data', 'raw') # Path to the dataset
    data_loader = MalariaDataLoader(dataset_path) # Initialize the data loader
    
    try:
        data_loader.verify_directories() # Verify if directories exist
        data_loader.clean_load_data_image() # Load and clean data
        summary = data_loader.data_summary() # Print data summary
        print(f'Dataset summary: {summary}')
        
    except FileNotFoundError as fnf_error:
        print(f'Error: {fnf_error}')
        
    except Exception as e:
        print(f'An unexpected error occurred: {e}')