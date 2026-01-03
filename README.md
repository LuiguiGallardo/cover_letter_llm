# Cover Letter Generator

Generate professional cover letters using a local LLM. Supports GUI and CLI.

## Requirements
- Python 3
- [Ollama](https://ollama.com/) with `llama3.1:8b` model (`ollama pull llama3.1:8b`)
- Dependencies: `pip install customtkinter ollama`

## Usage

### GUI Mode
Run without arguments:
```bash
python main.py
```

### CLI Mode
```bash
python main.py -p "Job Title" -c "Company" -j "Job Description or file path"
```
