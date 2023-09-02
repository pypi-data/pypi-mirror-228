from transformers import AutoTokenizer, AutoModelForCausalLM,BitsAndBytesConfig
import ray
import torch
import os
import ray
from typing import Any,Any,Dict, List,Tuple,Generator
import types
from byzerllm.utils import generate_instruction_from_history,compute_max_new_tokens

from pyjava.api.mlsql import DataServer
from .. import BlockRow

def stream_chat(self,tokenizer,ins:str, his:List[Tuple[str,str]]=[],  
        max_length:int=1024, 
        top_p:float=0.95,
        temperature:float=0.1,**kwargs):
        
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")    
    role_mapping = {        
        "user":"User",        
        "assistant":"Assistant",
    }
    fin_ins = generate_instruction_from_history(ins,his,role_mapping=role_mapping)     
    tokens = tokenizer(fin_ins, return_token_type_ids=False,return_tensors="pt").to(device)
    max_new_tokens = compute_max_new_tokens(tokens,max_length)

    response = self.generate(
        input_ids=tokens["input_ids"],
        max_new_tokens=max_new_tokens,
        repetition_penalty=1.05,
        temperature=temperature,
        attention_mask=tokens.attention_mask,
        eos_token_id=tokenizer.eos_token_id,
        pad_token_id=tokenizer.eos_token_id,
        bos_token_id=tokenizer.bos_token_id
    )
    answer = tokenizer.decode(response[0][tokens["input_ids"].shape[1]:], skip_special_tokens=True)
    return [(answer,"")]


def init_model(model_dir,infer_params:Dict[str,str]={},sys_conf:Dict[str,str]={}):     
    quatization = infer_params.get("quatization","false") == "true"
                              
    pretrained_model_dir = os.path.join(model_dir,"pretrained_model")
    adaptor_model_dir = model_dir
    is_adaptor_model = os.path.exists(pretrained_model_dir)
    
    if not is_adaptor_model:        
        pretrained_model_dir = model_dir

    tokenizer = AutoTokenizer.from_pretrained(pretrained_model_dir)
    tokenizer.padding_side="right"
    tokenizer.pad_token_id=0
    tokenizer.bos_token_id = 1

    if quatization:
        nf4_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=False,
            bnb_4bit_compute_dtype=torch.bfloat16,
        )
        model = AutoModelForCausalLM.from_pretrained(
            pretrained_model_dir,
            trust_remote_code=True,            
            device_map="auto",
            quantization_config=nf4_config,
        )

    else:
        model = AutoModelForCausalLM.from_pretrained(pretrained_model_dir,trust_remote_code=True,
                                                device_map='auto',                                                
                                                torch_dtype=torch.bfloat16                                                
                                                )
    if is_adaptor_model:
        from peft import PeftModel
        model = PeftModel.from_pretrained(model, adaptor_model_dir)

    model.eval()  
    if quatization:
        model = torch.compile(model)
    
    # falcon is not support yet in optimum
    # model = model.to_bettertransformer()    
    model.stream_chat = types.MethodType(stream_chat, model)     
    return (model,tokenizer)


def sft_train(data_refs:List[DataServer],
              train_params:Dict[str,str],
              conf: Dict[str, str])->Generator[BlockRow,Any,Any]:
    from ..utils.sft import sft_train as common_sft_train
    return common_sft_train(data_refs,train_params,conf) 



