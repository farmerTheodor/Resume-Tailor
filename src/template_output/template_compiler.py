import os
from pathlib import Path
import subprocess
from .template_loader import Template, TemplateTypes, OutputFormatTypes

DEFAULT_OUTPUT_PATH = Path("/workspace/output/sharable_resumes")


def compile_template(
    template: Template,
    data: str,
    output_file_path: Path | str = DEFAULT_OUTPUT_PATH,
):
    if isinstance(output_file_path, str):
        output_file_path = Path(output_file_path)

    if template.output_format_type == OutputFormatTypes.LATEX:
        compile_latex_template(data, output_file_path)
    else:
        raise ValueError(f"Unsupported resume format: {template.output_format_type}")


def compile_latex_template(data: str, output_file_path: Path | str):
    if isinstance(output_file_path, str):
        output_file_path = Path(output_file_path)

    if output_file_path.suffix == ".pdf":
        compile_latex_to_pdf(data, output_file_path)


def compile_latex_to_pdf(data: str, output_file_path: Path):
    intermediate_tex_path = Path(f"/tmp/{output_file_path.stem}.tex")
    with open(intermediate_tex_path, "w") as tex_file:
        tex_file.write(data)

    try:
        # pdflatex cli
        #  -output-directory specifies where to put the output pdf
        # the last argument is the path to the .tex file to compile to the pdf
        # the files name is taken from the .tex file name
        result = subprocess.run(
            [
                "pdflatex",
                f"-output-directory={output_file_path.parent}",
                str(intermediate_tex_path),
            ],
            timeout=10,
            capture_output=True,
        )

        if result.returncode != 0:
            raise RuntimeError(
                f"LaTeX compilation failed: {result.stderr.decode('utf-8')}"
            )

        temporary_file_suffixes = ["aux", "log", "out"]
        for suffix in temporary_file_suffixes:
            os.remove(output_file_path.parent / f"{output_file_path.stem}.{suffix}")

    finally:
        os.remove(intermediate_tex_path)
