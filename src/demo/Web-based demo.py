from pywebio import start_server
from pywebio.input import *
from pywebio.output import *
from pywebio.session import info as session_info
from transformers import AutoTokenizer, AutoModelForTokenClassification
import torch
from textblob import TextBlob

def demo():
    put_markdown("""# CAUASALITY DETECTION
    
    [Causality](https://en.wikipedia.org/wiki/Causality) (also called causation, or cause and effect) is the influence by which one event, process, state, or object (a cause) contributes to the production of another event, process, state, or object (an effect) where the cause is partly responsible for the effect, and the effect is partly dependent on the cause. 
    
    The source code of this application is [here](https://github.com/NLP-Final-Projects/causal-discovery/raw/main/src/demo)
    """)

    data = input_group("Initialization",
                       [select('Choose the Model?', ['BERT'], name = "model"),
                        input("INPUT SEQUENCE (IN PERSIAN)：", type=TEXT, name = "seq")
                        ])
    model_mode = data["model"]
    sequence = data["seq"]
        
    if model_mode == "BERT":
        model_address = "Cause_Effect_Detection_BERT"   # Specify by user   # Here you should specify the address of the Cause_Effect_Detection_BERT saved model
        tokenizer = AutoTokenizer.from_pretrained(model_address)
        model = AutoModelForTokenClassification.from_pretrained(model_address)
        
        label_list = ['O', 'B-CAUSE', 'I-CAUSE', 'B-EFFECT', 'I-EFFECT']

        
        # Drop-down selection
        tokens = tokenizer.tokenize(tokenizer.decode(tokenizer.encode(sequence)))
        inputs = tokenizer.encode(sequence, return_tensors="pt")

        outputs = model(inputs).logits
        predictions = torch.argmax(outputs, dim=2)
        out = [(token, label_list[prediction]) for token, prediction in zip(tokens, predictions[0].numpy())]
        CAUSE = []
        EFFECT = []
        for item in out:
            if item[1] == "B-CAUSE" or item[1] == "I-CAUSE":
                CAUSE.append(item[0])
            if item[1] == "B-EFFECT" or item[1] == "I-EFFECT":
                EFFECT.append(item[0])
        CAUSE = " ".join(CAUSE)       
        EFFECT = " ".join(EFFECT)       
        
    put_table([
        ['MODEL_NAME', model_mode],
        ['INPUT_SEQ', sequence],    
        ['MODEL_RAW_OUTPUT', out],  
        ['CAUSE-EFFECT-TABLE', put_table([['CAUSE', 'EFFECT'], [CAUSE, EFFECT]])]
    ])

def  check_language(seq):
    lang = TextBlob(seq)
    language = lang.detect_language()
    print(language)
    if language != "fa":
        return "PLEASE ENSURE THAT YOUR INPUT IS IN PERSIAN"    
 
if __name__ == '__main__':
    # while(True):
    #     demo()
    start_server(demo, debug=True, port=8080)
