from django.shortcuts import render
import torch
from PIL import Image
import torchvision.transforms as transforms
import torch.nn.functional as F
from malariaApp.models import PredictionModel
import os
from django.conf import settings

# Create your views here.

MODEL_PATH = os.path.join(settings.BASE_DIR, 'malaria_cnn_quantized_model.pt')

# Load quantized TorchScript model
model = torch.jit.load(MODEL_PATH, map_location=torch.device('cpu'))
model.eval()

transforms = transforms.Compose([
    transforms.Resize((150, 150)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
]) 

classes = ['Parasitized', 'Uninfected']

def index(request):
    return render(request, 'malariaApp/index.html')

def predict(request):
    
    if request.method == 'POST' and request.FILES.get('image'):
        # Get the uploaded image
        image_file = request.FILES['image'] # Django InMemoryUploadedFile
        image_file = Image.open(image_file).convert('RGB') # Ensure image is in RGB format
        image_file = transforms(image_file).unsqueeze(0)  # Add batch dimension
        
        with torch.no_grad():
            output = model(image_file) # Get model output
            probabilities = F.softmax(output,dim=1) # # convert logits to probabilities
            confidence, predicted = torch.max(output, 1) # Get class with highest probability
            result = classes[predicted.item()] # Map to class name
            confidence_score = probabilities[0][predicted.item()].item() * 100
            
        # Save prediction to database
        prediction_entry = PredictionModel(
            image=request.FILES['image'],
            result=result,
            confidence = confidence_score
        )
        prediction_entry.save()
        
        # Fetch last 5 predictions for table display
        row_predictions = PredictionModel.objects.order_by('-id')[:5]
        
        dict = {
            'result': result,
            'confidence': confidence_score,
            'row_predictions': row_predictions,
            'image_url': prediction_entry.image.url
        }
        return render(request, 'malariaApp/result.html', context=dict)
    
    return render(request, 'malariaApp/index.html')