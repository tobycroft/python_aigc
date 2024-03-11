from flask import Blueprint
from transformers import pipeline

import tuuz.Ret

StudyController = Blueprint("gemini", __name__)


@StudyController.post('/')
def slash():
    return "/"


@StudyController.post('/text')
async def text():
    generate_text = pipeline(
        model="Stevross/Astrid-LLama-3B-GPU",
        torch_dtype="auto",
        trust_remote_code=True,
        use_fast=False,
        device_map={"": "cuda:0"},
    )

    res = generate_text(
        "Why is drinking water so healthy?",
        min_new_tokens=2,
        max_new_tokens=256,
        do_sample=False,
        num_beams=1,
        temperature=float(0.3),
        repetition_penalty=float(1.2),
        renormalize_logits=True
    )
    print(res[0]["generated_text"])
    return tuuz.Ret.success(0, text)
