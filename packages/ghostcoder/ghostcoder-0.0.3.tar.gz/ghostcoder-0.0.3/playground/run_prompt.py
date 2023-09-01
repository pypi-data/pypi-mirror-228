import json
import logging
from typing import Dict

from langchain import HuggingFaceHub, SagemakerEndpoint
from langchain.callbacks import StreamingStdOutCallbackHandler, StdOutCallbackHandler
from langchain.callbacks.manager import CallbackManager
from langchain.llms import LlamaCpp, VertexAI
from langchain.llms.sagemaker_endpoint import LLMContentHandler

from ghostcoder import FileRepository
from ghostcoder.llm.base import LLMWrapper
from ghostcoder.callback import LogCallbackHandler
from ghostcoder.actions.write_code import WriteCodeAction
from ghostcoder.schema import Message, TextItem, FileItem

testdir = "/home/albert/repos/albert/aider/benchmarks/2023-08-30-19-00-47--ghostcoder--codellama-CodeLlama-34b-Instruct-hf/allergies"
callback = LogCallbackHandler(testdir + "/prompt_log")
from langchain.callbacks import StreamingStdOutCallbackHandler, StdOutCallbackHandler

callback_manager = CallbackManager([StreamingStdOutCallbackHandler(), StdOutCallbackHandler()])

def llama_cpp():
    llm_cpp = LlamaCpp(
        #model_path="/home/albert/repos/stuffs/llama.cpp/models/CodeLlama-13b-Python/ggml-model-q4_0.gguf",
        model_path="/home/albert/repos/stuffs/llama.cpp/models/CodeLlama-7b-Instruct/ggml-model-q4_0.gguf",
        temperature=0.0,
        max_tokens=4000,
        n_ctx=4000,
        top_p=1,
        callback_manager=callback_manager,
        verbose=True,
    )

logging.basicConfig(level=logging.INFO)

def huggingface():
pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=1024,
    temperature=0.0,
)

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

model_name_or_path = "TheBloke/Phind-CodeLlama-34B-v2-GPTQ"

model = AutoModelForCausalLM.from_pretrained(model_name_or_path,
                                             torch_dtype=torch.float16,
                                             device_map="auto",
                                             revision="main")

tokenizer = AutoTokenizer.from_pretrained(model_name_or_path, use_fast=True)

pipe = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    max_new_tokens=1024,
    temperature=0.01,
)


llm = HuggingFacePipeline(pipeline=pipe)

_length": 8096, "max_new_tokens": 1000},
)
    llm = HuggingFaceHub(
        repo_id="codellama/CodeLlama-34b-Instruct-hf",
        callback_manager=callback_manager,
        model_kwargs={"temperature": 0.01, "max_tokens": 4000, "max_length": 4000, "max_new_tokens": 4000})



class ContentHandler(LLMContentHandler):
    content_type = "application/json"
    accepts = "application/json"

    def transform_input(self, prompt: str, model_kwargs: Dict) -> bytes:
        input_str = json.dumps({prompt: prompt, **model_kwargs})
        return input_str.encode("utf-8")

    def transform_output(self, output: bytes) -> str:
        response_json = json.loads(output.read().decode("utf-8"))
        return response_json[0]["generated_text"]


content_handler = ContentHandler()



llm=LLMWrapper(SagemakerEndpoint(
    endpoint_name="huggingface-pytorch-tgi-inference-2023-08-31-08-56-05-901",
    #credentials_profile_name="credentials-profile-name",
    region_name="us-east-1",
    model_kwargs={"temperature": 1e-10},
    content_handler=content_handler
))


#llm = LLMWrapper(llm=VertexAI(model_name="code-bison", project="albert-test-368916", max_output_tokens=2048, callback_manager=callback_manager))

repository = FileRepository(repo_path=testdir, use_git=False)

action = WriteCodeAction(
    llm=llm,
    repository=repository,
    sys_prompt_id="expect_incomplete"
)

prompt = """# Instructions

Given a person's allergy score, determine whether or not they're allergic to a given item, and their full list of allergies.

An allergy test produces a single numeric score which contains the information about all the allergies the person has (that they were tested for).

The list of items (and their value) that were tested are:

- eggs (1)
- peanuts (2)
- shellfish (4)
- strawberries (8)
- tomatoes (16)
- chocolate (32)
- pollen (64)
- cats (128)

So if Tom is allergic to peanuts and chocolate, he gets a score of 34.

Now, given just that score of 34, your program should be able to say:

- Whether Tom is allergic to any one of those allergens listed above.
- All the allergens Tom is allergic to.

Note: a given score may include allergens **not** listed above (i.e.  allergens that score 256, 512, 1024, etc.).
Your program should ignore those components of the score.
For example, if the allergy score is 257, your program should only report the eggs (1) allergy.

Use the above instructions to modify the supplied files: allergies.py
Keep and implement the existing function or class stubs, they will be called from unit tests.
Only use standard python libraries, don't suggest installing any packages.
"""

result = action.execute(message=Message(sender="Human",
                                        items=[TextItem(text=prompt),
                                           FileItem(file_path="allergies.py")]))
