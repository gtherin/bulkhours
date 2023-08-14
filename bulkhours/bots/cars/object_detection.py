import transformers
from PIL import Image
import torch
import cv2

model_name = "facebook/detr-resnet-50"
model_name = "hustvl/yolos-tiny"

if model_name == "facebook/detr-resnet-50":
    from transformers import DetrImageProcessor, DetrForObjectDetection
    processor = DetrImageProcessor.from_pretrained(model_name)
    model = DetrForObjectDetection.from_pretrained(model_name)
else:
    processor = transformers.YolosImageProcessor.from_pretrained("hustvl/yolos-tiny")
    model = transformers.YolosForObjectDetection.from_pretrained('hustvl/yolos-tiny')


def estimate_age():
    import requests
    from PIL import Image
    from io import BytesIO

    from transformers import ViTFeatureExtractor, ViTForImageClassification

    # Get example image from official fairface repo + read it in as an image
    r = requests.get('https://github.com/dchen236/FairFace/blob/master/detected_faces/race_Asian_face0.jpg?raw=true')
    im = Image.open(BytesIO(r.content))
    print()

    # Init model, transforms
    model = ViTForImageClassification.from_pretrained('nateraw/vit-age-classifier')
    transforms = ViTFeatureExtractor.from_pretrained('nateraw/vit-age-classifier')

    # Transform our image and pass it through the model
    inputs = transforms(im, return_tensors='pt')
    output = model(**inputs)

    # Predicted Class probabilities
    proba = output.logits.softmax(1)

    # Predicted Classes
    preds = proba.argmax(1)
    print("AAAAAAAAAAAAAaa", preds, proba)


estimate_age()

colors = {"person": (255, 0, 255), "default": (0, 255, 255)}
font = cv2.FONT_HERSHEY_SIMPLEX
stroke = 2 

# default webcam
stream = cv2.VideoCapture(0)


while(True):
    # Capture frame-by-frame
    (grabbed, frame) = stream.read()

    # convert the image from NumPy array into a PIL image
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(img)

    inputs = processor(images=image, return_tensors="pt")
    outputs = model(**inputs)

    target_sizes = torch.tensor([image.size[::-1]])
    results = processor.post_process_object_detection(outputs, target_sizes = target_sizes, threshold = 0.9)[0]

    for score, label, box in zip(results["scores"], results["labels"], results["boxes"]):
        box = [round(i, 2) for i in box.tolist()]
        olabel = model.config.id2label[label.item()]
        print(f"Detected {olabel} with confidence {round(score.item(), 3)} at location {box}")

        if olabel == "person":
            print("person detected")
        color = colors[olabel] if olabel in colors else colors["default"]

        # draw the bounding box
        cv2.rectangle(frame, 
                      (int(box[0]), int(box[1])),   # x1, y1
                      (int(box[2]), int(box[3])),   # x2, y2
                      color, 
                      stroke)
        
        # display the label
        cv2.putText(frame, 
                    model.config.id2label[label.item()], # label
                    (int(box[0]), int(box[1]-10)),       # x1, y1
                    font, 
                    1, 
                    color, 
                    stroke, 
                    cv2.LINE_AA)

    # Show the frame
    cv2.imshow("Image", frame)
    key = cv2.waitKey(1) & 0xFF    
    if key == ord("q"):    # Press q to break out of the loop
        break

# Cleanup
stream.release()
cv2.waitKey(1)
cv2.destroyAllWindows()
cv2.waitKey(1)