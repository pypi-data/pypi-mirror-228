import pandas as pd
from datasets import load_dataset
from transformers import AutoTokenizer 


def dataprep(model_name = "",out_tokeniser = "",dataset_name = "",dataset_arg=""):
    # need one parameter for getting the tokenizer:
    if out_tokeniser:
       tokenizer = out_tokeniser
    else:
       tokenizer = AutoTokenizer.from_pretrained(model_name)


    # for downloading dataset
    if dataset_arg:
        dataset = dataset_arg
    else:
        dataset = load_dataset(dataset_name,split='train')


    # the function to be modified
    def tokenize_function(examples):
        if "question" in examples and "answer" in examples:
          text = examples["question"][0] + examples["answer"][0]
        elif "input" in examples and "output" in examples:
          text = examples["input"][0] + examples["output"][0]
        elif "instruction" in examples and "response" in examples:
          text = examples["instruction"][0] + examples["response"][0]
        else:
          text = examples["text"][0]


        tokenizer.pad_token = tokenizer.eos_token
        tokenize_inputs = tokenizer(
            text,
            return_tensors = 'np',
            padding = True
        )
        max_length = min(
            tokenize_inputs["input_ids"].shape[1],2048
        )
        tokenizer.truncation_side = 'left'
        tokenise_inputs = tokenizer(
            text,
            return_tensors = 'np',
            truncation = True,
            max_length = max_length
        )
        return tokenise_inputs


    # mapping 
    tokenized_dataset = dataset.map(
        tokenize_function,
        batched=True,
        batch_size=1,
        drop_last_batch=True
    )


    # adding label
    tokenized_dataset = tokenized_dataset.add_column("labels", tokenized_dataset["input_ids"])
    
    return tokenized_dataset


