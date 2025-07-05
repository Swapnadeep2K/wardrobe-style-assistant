from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from transformers import VisionEncoderDecoderModel, ViTImageProcessor, AutoTokenizer
from PIL import Image
import torch
import io
import re
import json

app = FastAPI()

# Fashion rules
rules = {
    "type": ["kurti", "shirt", "t-shirt", "dress", "jeans", "skirt", "saree", "hoodie", "top", "jacket"],
    "category": ["topwear", "bottomwear", "outerwear", "ethnic", "onepiece"],
    "gender": ["male", "female", "unisex"],
    "color_primary": ["red", "blue", "black", "white", "green", "yellow", "pink", "purple", "brown", "beige", "grey"],
    "color_secondary": ["white", "blue", "black", "pink", "beige", "green", "grey"],
    "pattern": ["solid", "floral", "striped", "checked", "graphic", "printed"],
    "fabric": ["cotton", "denim", "silk", "linen", "wool", "chiffon", "polyester", "leather"],
    "sleeve_length": ["sleeveless", "half sleeves", "3/4 sleeves", "full sleeves", "long sleeves", "short sleeves"],
    "sleeve_type": ["puff", "cap", "regular", "balloon"],
    "neck_type": ["round", "v-neck", "collared", "boat", "halter", "high neck"],
    "fit_type": ["slim", "regular", "loose", "oversized", "skinny"],
    "garment_length": ["crop", "knee length", "midi", "long", "ankle length", "floor length"],
    "closure_type": ["buttons", "zip", "drawstring", "open"],
    "embellishment": ["embroidery", "lace", "sequin", "ripped", "frills", "pleated"],
    "style": ["casual", "formal", "ethnic", "partywear", "streetwear", "sporty", "vintage"],
    "occasion": ["daily", "party", "beach", "wedding", "work", "activewear"],
    "season": ["summer", "winter", "spring", "monsoon", "autumn", "all-season"]
}


def extract_attributes(text, rules):
    result = {key: None for key in rules}
    for key, values in rules.items():
        for value in values:
            if re.search(rf"\b{re.escape(value.replace('-', ' '))}\b", text.replace('-', ' ')):
                result[key] = value
                break
    return result


@app.post("/predict/")
async def predict(file: UploadFile = File(...)):
    try:
        # Load image
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

        # Load model components
        model_name = "nlpconnect/vit-gpt2-image-captioning"
        model = VisionEncoderDecoderModel.from_pretrained(model_name)
        processor = ViTImageProcessor.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        device = torch.device("cpu")
        model.to(device)

        # Process and generate
        pixel_values = processor(images=image, return_tensors="pt").pixel_values.to(device)
        output_ids = model.generate(pixel_values, max_length=20)
        caption = tokenizer.decode(output_ids[0], skip_special_tokens=True).lower()

        attributes = extract_attributes(caption, rules)
        return JSONResponse(content={"caption": caption, "attributes": attributes})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})