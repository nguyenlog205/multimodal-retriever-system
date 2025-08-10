from transformers import AutoTokenizer, AutoModelForMaskedLM

tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base")
model = AutoModelForMaskedLM.from_pretrained("vinai/phobert-base")

def named_entity_recognition(input: str):

    return None



