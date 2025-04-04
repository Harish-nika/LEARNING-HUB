# 📄 BondDocExtractor: Fine-Tune an LLM on 1M+ Financial Bond PDFs

This project enables scalable training of a language model to extract structured data from large-scale unstructured bond documents (PDFs). It uses a step-by-step QLoRA-based fine-tuning approach on real financial fixed-income bond documents.

---

## 📊 Objective

Train and deploy an LLM to extract structured JSON data (like issuer, ISIN, coupon rate, etc.) from unstructured financial bond PDFs — using a scalable, bootstrapped labeling and fine-tuning process.

---

## 📌 Project Overview

```
Raw PDFs
   │
   ├─▶ Text + Layout Extraction (pdfplumber)
   │
   ├─▶ JSON Auto-Labeling using GPT/Gemini
   │
   ├─▶ QLoRA Fine-Tuning (Axolotl)
   │
   └─▶ Deploy for Inference (Ollama / LangChain / API)
```

---

## ✅ PHASE 1: Data Preparation

### 1.1 Organize PDFs

Place your documents inside a directory:
```
/data/bonds_batch_1/*.pdf
```

### 1.2 Extract Text from PDFs (with Layout)

```python
import pdfplumber, json
from pathlib import Path

def extract_text_from_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        return "\n".join([p.extract_text() or '' for p in pdf.pages])

pdf_dir = Path("/data/bonds_batch_1")
with open("raw_bonds_batch1.jsonl", "w") as f:
    for pdf_path in pdf_dir.glob("*.pdf"):
        text = extract_text_from_pdf(pdf_path)
        json.dump({"input": text}, f)
        f.write("\n")
```

---

## 🤖 PHASE 2: Auto-Labeling with GPT / Gemini

### 2.1 Prompt-Based Labeling
Use OpenAI or Gemini APIs to generate structured JSON fields:
```python
prompt = f"""
### Task:
Extract bond details in JSON.

### Document:
{text[:3000]}

### Output:
{{
  "issuer": "...",
  "isin": "...",
  ...
}}
"""
```

Output file should be a `.jsonl`:
```json
{
  "instruction": "Extract bond details.",
  "input": "Issuer: ABC Corp\nISIN: ...",
  "output": {
    "issuer": "ABC Corp",
    "isin": "US1234567890"
  }
}
```

---

## 🔧 PHASE 3: QLoRA Fine-Tuning with Axolotl

### 3.1 Install Axolotl

```bash
git clone https://github.com/OpenAccess-AI-Collective/axolotl
cd axolotl
pip install -e .
```

### 3.2 Create Config File

**`configs/qlora_bonds.yaml`**
```yaml
base_model: meta-llama/Meta-Llama-3-8B-Instruct
load_in_4bit: true
adapter: qlora
datasets:
  - path: ./train_bonds.jsonl
    type: alpaca
lora_r: 64
lora_alpha: 16
lora_dropout: 0.05
num_epochs: 3
cutoff_len: 4096
val_set_size: 0.05
output_dir: ./output/qlora-bond-model
gradient_accumulation_steps: 4
per_device_train_batch_size: 2
bf16: true
```

### 3.3 Launch Training

```bash
accelerate launch axolotl/scripts/train.py configs/qlora_bonds.yaml
```

---

## 🚀 PHASE 4: Inference / Deployment

### 4.1 Use Fine-Tuned Model

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("output/qlora-bond-model", device_map="auto")
tokenizer = AutoTokenizer.from_pretrained("output/qlora-bond-model")

prompt = "### Instruction:\nExtract bond details\n\n### Document:\n<bond text>\n\n### Output:"
tokens = tokenizer(prompt, return_tensors="pt").to(model.device)
output = model.generate(**tokens, max_new_tokens=512)
print(tokenizer.decode(output[0], skip_special_tokens=True))
```

### 4.2 Serve Model via

- [ ] 🧠 Ollama (local inference)
- [ ] 🧠 vLLM / TGI for scalable APIs
- [ ] 🧠 LangChain + Streamlit for PDF UI

---

## 🔁 PHASE 5: Iterative Bootstrapping

| Step | Sample Count |
|------|--------------|
| Manually label | 1,000 |
| Auto-label via GPT | 10,000 |
| Fine-tune | ✅ |
| Use model to label next batch | 100,000 |
| Retrain model | ✅ |
| Repeat for full 1M | ♻️ |

---

## 📂 Directory Structure

```
bond-extractor/
├── data/
│   └── bonds_batch_1/*.pdf
├── extracted/
│   └── raw_bonds_batch1.jsonl
├── labeled/
│   └── train_bonds.jsonl
├── configs/
│   └── qlora_bonds.yaml
├── output/
│   └── qlora-bond-model/
└── README.md
```

---

## 🧹 TODOs

- [ ] PDF parallel extractor (Ray or multiprocessing)
- [ ] Auto-labeling script using OpenAI/Gemini API
- [ ] Fine-tuning wrapper
- [ ] Deployment using Ollama or vLLM

---

## 📬 Contact

Built by Harish Kumar  
GitHub: [harish-nika](https://github.com/harish-nika)  
Email: harishkumar56278@gmail.com

---

## 🏑️ License

MIT License

