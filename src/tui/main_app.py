from pathlib import Path
from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, TextArea
from textual.reactive import reactive
from textual.worker import Worker, WorkerState
from textual.binding import Binding
import os

from src.resume_tailor import tailor_resume_to_job_description
from textual import work

DEFAULT_TEMPLATE_PATH = Path(
    os.getenv("DEFAULT_TEMPLATE_PATH", "/workspace/resume_templates/test_format")
)


class ResumeTailor(App):
    BINDINGS = [
        Binding("ctrl+q", "quit", "Quit", priority=True),
        Binding("ctrl+v", "paste", "Paste", priority=True, show=False),
        Binding("ctrl+enter", "submit", "Submit", priority=True),
        Binding("ctrl+a", "select_all", "Select All", priority=True, show=False),
    ]

    CSS = """
        TextArea#job-description-input {
            height: 100%;
            width: 100%;
            border: solid green;
            border-title-align: center;
            border-subtitle-align: left;
            content-align: right bottom;
        }
    """

    resume_template: reactive[Path] = reactive(
        DEFAULT_TEMPLATE_PATH,
        init=False,
    )

    def compose(self) -> ComposeResult:
        yield Header(name="Resume Tailor")

        with TextArea(
            placeholder="Paste job description here...",
            id="job-description-input",
        ) as text_area:
            text_area.border_subtitle = f"Template: {self.resume_template}"
        yield Footer()

    def watch_resume_template(self, new_path: Path) -> None:
        main_container = self.query_one("#job-description-input", TextArea)
        main_container.border_subtitle = f"Template: {new_path}"

    def action_submit(self) -> None:
        job_description = self.query_one("#job-description-input", TextArea).text
        if job_description.strip() == "":
            self.notify("Please enter a job description before submitting.")
            return

        self.tailor_resume_task(job_description, self.resume_template)
        self.query_one("#job-description-input", TextArea).text = ""

    def action_select_all(self) -> None:
        text_area = self.query_one("#job-description-input", TextArea)
        text_area.select_all()

    @work(
        exclusive=False,
        thread=True,
        group="resume_generation",
    )
    async def tailor_resume_task(
        self, job_description: str, resume_template: Path
    ) -> None:
        try:
            self.notify("generating resume...")
            tailor_resume_to_job_description(job_description, resume_template)
            self.notify(
                "Resume generated successfully!\n Check /workspace/output/sharable_resumes for the output."
            )

        except Exception:
            self.notify("Error generating resume")

    def on_worker_state_changed(self, event: Worker.StateChanged) -> None:
        if event.worker.group == "resume_generation":
            main_container = self.query_one("#job-description-input", TextArea)
            if event.state in (WorkerState.RUNNING, WorkerState.PENDING):
                main_container.border_title = "Resume Tailoring in progress..."
            else:
                main_container.border_title = ""


def run_tui():
    app = ResumeTailor()
    app.run()


if __name__ == "__main__":
    run_tui()
