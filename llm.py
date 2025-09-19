from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

class LocalLLM:
    def __init__(self, model_name="EleutherAI/gpt-neo-125M"):
        print("🔄 Carregando modelo local, pode levar alguns segundos...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float32  # força CPU
        )
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device=-1,  # -1 força CPU
            max_new_tokens=64,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )
        print("✅ Modelo carregado!")

    def chat(self, prompt: str) -> str:
        response = self.pipe(prompt)
        return response[0]["generated_text"]
