import customtkinter as ctk
import ollama
import threading
import argparse
import sys

# --- CONFIGURATION ---
MY_RESUME_CONTENT = """
NAME: Luigui Gallardo-Becerra
POSITION: Bioinformatician | Molecular Biologist
WEBSITE: www.lmgb.xyz
CONTACT: luiguimichelgallardo@gmail.com | +1 619 602 0725
GITHUB: LuiguiGallardo | LINKEDIN: luiguigallardo

ABOUT:
Experienced Bioinformatician and Data Scientist with 6+ years of expertise in genomics, transcriptomics, and microbiome analysis. Skilled in developing scalable pipelines (Snakemake, Nextflow), managing large-scale NGS datasets, and implementing machine learning for biological data. 13+ peer-reviewed publications.

EXPERIENCE:
1. Research Assistant (Bioinformatics & Data Science) | Institute of Biotechnology, UNAM (2019 - 2025)
- Designed automated pipelines using Snakemake, Nextflow, Python, and Bash.
- Analyzed WGS, RNA-seq, 16S, metagenomic, and metatranscriptomic datasets.
- Applied machine learning to identify biomarkers in high-dimensional omics datasets.
- Administered HPC clusters and managed Linux/SLURM environments.

2. Data Engineer | Appen (2016 - 2018)
- Developed automated ETL pipelines for high-volume datasets.
- Implemented QC workflows for machine-learning model development.

3. Software Engineer (Internship) | Dept. of Computer Science, CUCEI (2016)
- Developed cloud-based web apps using ASP.NET Core for clinical data management.

EDUCATION:
- Ph.D. in Computational Biology, UNAM (2019 - 2025)
- M.Sc. in Computational Biology, UNAM (2016 - 2019)
- B.Sc. in Molecular Biology, University of Guadalajara (2012 - 2016)

TECHNICAL SKILLS:
- Languages: Python, R, Bash, SQL, Perl, C++, Java.
- Bioinformatics: Snakemake, Nextflow, QIIME2, Bioconductor, Samtools, BLAST.
- NGS: Illumina/PacBio, Read Alignment, Variant Calling, De Novo Assembly.
- Data Science: Machine Learning, Statistical Modeling, ggplot2, seaborn, matplotlib, Tableau, and R Shiny

PUBLICATIONS:
- 14 total peer-reviewed papers including Microb Ecol (2025), Anim Microbiome (2025), and Microb Cell Fact (2020).
"""

# --- SHARED LOGIC ---
def generate_prompt(position, company, job, resume):
    """Centralized prompt to ensure CLI and GUI produce the same quality."""
    return f"""
    Write a professional and polished cover letter for the {position} role at {company}. 
    Length: Approximately 200-250 words.
    Tone: Formal, authoritative, common American English.

    GUIDELINES:
    - Use "Dear Hiring Manager" or "Dear {company} Team."
    - Avoid "AI-isms" like "tapestry," "delve," or "passionate advocate."
    - Focus on "Technical Fit": Use your PhD and 6+ years of experience as the foundation.
    - Style: Use strong, professional verbs like "Spearheaded," "Engineered," "Optimized," and "Collaborated."
    
    STRUCTURE:
    1. INTRODUCTION: State the specific position and your high-level qualifications (PhD + Bioinformatician).
    2. TECHNICAL CORE: Connect your specific experience with {company}'s needs (Nextflow, Snakemake, HPC, NGS). 
    3. RESEARCH IMPACT: Briefly mention it.
    4. CLOSING: A professional request for an interview and a formal sign-off.

    JOB POST: {job}
    RESUME: {resume}
    """

def run_llm_core(position, company, job, resume):
    """The actual call to Ollama."""
    prompt = generate_prompt(position, company, job, resume)
    response = ollama.generate(model='llama3.1:8b', prompt=prompt)
    return response['response']

# --- CLI MODE ---
def start_cli(args):
    try:
        # Check if job is a file path or direct text
        try:
            with open(args.job, 'r') as f:
                job_desc = f.read()
        except:
            job_desc = args.job

        result = run_llm_core(args.position, args.company, job_desc, MY_RESUME_CONTENT)
        print("\n" + "="*30 + "\n")
        print(result)
        print("\n" + "="*30 + "\n")
    except Exception as e:
        print(f"Error: {e}")

# --- GUI MODE ---
ctk.set_appearance_mode("dark") 
ctk.set_default_color_theme("blue")

class CoverLetterApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Cover Letter Generator")
        self.geometry("800x900")

        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.pack(pady=10, padx=20, fill="x")

        self.label_pos = ctk.CTkLabel(self.top_frame, text="Target Position:")
        self.label_pos.grid(row=0, column=0, padx=10, pady=10)
        self.pos_input = ctk.CTkEntry(self.top_frame, placeholder_text="e.g. Senior Bioinformatician", width=250)
        self.pos_input.grid(row=0, column=1, padx=10, pady=10)

        self.label_comp = ctk.CTkLabel(self.top_frame, text="Company Name:")
        self.label_comp.grid(row=0, column=2, padx=10, pady=10)
        self.comp_input = ctk.CTkEntry(self.top_frame, placeholder_text="e.g. Illumina", width=250)
        self.comp_input.grid(row=0, column=3, padx=10, pady=10)

        self.label_job = ctk.CTkLabel(self, text="Job Description", font=("Arial", 14, "bold"))
        self.label_job.pack(pady=(10, 0))
        self.job_input = ctk.CTkTextbox(self, height=150, width=750)
        self.job_input.pack(pady=5)

        self.label_resume = ctk.CTkLabel(self, text="Resume Content", font=("Arial", 14, "bold"))
        self.label_resume.pack(pady=(10, 0))
        self.resume_input = ctk.CTkTextbox(self, height=150, width=750)
        self.resume_input.pack(pady=5)
        self.resume_input.insert("1.0", MY_RESUME_CONTENT.strip())

        self.gen_button = ctk.CTkButton(self, text="Generate Concise Cover Letter", font=("Arial", 14, "bold"), height=40, command=self.start_generation)
        self.gen_button.pack(pady=20)

        self.output_text = ctk.CTkTextbox(self, height=250, width=750, fg_color="#1e1e1e", font=("Consolas", 12))
        self.output_text.pack(pady=5)

    def start_generation(self):
        self.gen_button.configure(state="disabled", text="Processing...")
        self.output_text.delete("1.0", ctk.END)
        threading.Thread(target=self.run_llm_gui).start()

    def run_llm_gui(self):
        try:
            result = run_llm_core(
                self.pos_input.get().strip(),
                self.comp_input.get().strip(),
                self.job_input.get("1.0", ctk.END).strip(),
                self.resume_input.get("1.0", ctk.END).strip()
            )
            self.after(0, lambda: self.finish_generation(result))
        except Exception as e:
            self.after(0, lambda: self.finish_generation(f"Error: {str(e)}"))
    
    def finish_generation(self, result):
        self.output_text.insert("1.0", result)
        self.gen_button.configure(state="normal", text="Generate Concise Cover Letter")

# --- EXECUTION ---
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a professional cover letter via GUI or CLI.")
    parser.add_argument("-p", "--position", help="The job title")
    parser.add_argument("-c", "--company", help="The company name")
    parser.add_argument("-j", "--job", help="The job description text or path to a .txt file")

    args = parser.parse_args()

    # If any CLI arguments are provided, don't launch the GUI
    if args.position or args.company or args.job:
        if not all([args.position, args.company, args.job]):
            print("Error: For CLI mode, you must provide -p, -c, and -j.")
            sys.exit(1)
        start_cli(args)
    else:
        # Launch GUI
        app = CoverLetterApp()
        app.mainloop()