FROM python:3.13

# Install dependencies

## Install latex
RUN apt update && apt install texlive-latex-base texlive-latex-recommended texlive-latex-extra texlive-fonts-recommended -y

## Install uv
RUN pip install uv

# Install container dependencies
COPY ./.devcontainer/requirements.txt ./requirements.txt
RUN uv pip install --system --no-cache -r requirements.txt

# Install program dependencies
COPY ./requirements.txt ./requirements.txt
RUN uv pip install --system --no-cache -r requirements.txt


# Set up helper aliases
RUN echo "source \"\${APP_PATH}/.devcontainer/aliases.sh\"" >> "$HOME/.bashrc"


# Put envirnonment variables prone to change here


# Set the default command for the container
ENTRYPOINT ["bash"]
USER "root"