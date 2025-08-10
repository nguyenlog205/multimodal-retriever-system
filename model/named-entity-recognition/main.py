from transformers import AutoTokenizer, AutoModelForMaskedLM

tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
model = AutoModelForMaskedLM.from_pretrained("vinai/phobert-base")

import py_vncorenlp

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
print("Base directory:", BASE_DIR)

def prepare_vncorenlp_model():
    # Define the directory to save the model
    _VNCORENLP_DIR = os.path.join(BASE_DIR, "model", "vncorenlp")
    _MODEL_FILE = os.path.join(_VNCORENLP_DIR, "VnCoreNLP-1.1.1.jar")

    # Download the model if it does not exist
    if not os.path.exists(_MODEL_FILE):
        print(f"Downloading VnCoreNLP model to {_VNCORENLP_DIR}...")
        py_vncorenlp.download_model(save_dir=_VNCORENLP_DIR)

    # Load the model
    print(f"Loading VnCoreNLP model from {_VNCORENLP_DIR}...")
    model = py_vncorenlp.VnCoreNLP(save_dir=_VNCORENLP_DIR)
    
    return model


model = prepare_vncorenlp_model()
annotated_text = model.annotate_text("Ông Nguyễn Khắc Chúc đang làm việc tại Đại học Quốc gia Hà Nội. Bà Lan, vợ ông Chúc, cũng làm việc tại đây.")
model.print_out(annotated_text)