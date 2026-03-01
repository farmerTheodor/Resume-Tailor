#!/usr/bin/bash

echo """ 
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
 XXXXXXX  ╦═╗╔═╗╔═╗╦ ╦╔╦╗╔═╗          
  =====   ╠╦╝║╣ ╚═╗║ ║║║║║╣           
  =====   ╩╚═╚═╝╚═╝╚═╝╩ ╩╚═╝          
  =====   ╔╦╗╔═╗╦╦  ╔═╗╦═╗            
  =====    ║ ╠═╣║║  ║ ║╠╦╝            
  =====    ╩ ╩ ╩╩╩═╝╚═╝╩╚═            
 XXXXXXX  Start: run_resume_tailor_ui 
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-                      
"""

# This file contains custom shell functions and aliases to streamline development
# Be aware that this script will run every time a new shell session is started. Do not put expensive operations in here directly.

# Auto completion works with these functions, so you can use tab completion to see available options.
# Name your functions and aliases in a way that you can tab complete them easily but also make sure they are descriptive.

# Here is an example of how to use this file. This function can be used to
# quickly update and freeze python requirements in a project

# export LLM_DEBUG_MODE="true"

export PYTHONPATH="/workspace${PYTHONPATH:+:$PYTHONPATH}"
alias clf='compile_latex_file'


function compile_latex_file {
    if [ -z "$1" ]; then
        echo "Usage: compile_latex_file <filename.tex>"
        return 1
    fi
    local filename="$1"
    local output_filepath="$OUTPUT_PATH"
    local sharable_resumes_filepath="$output_filepath/sharable_resumes"
    # Create default output directory if it doesn't exist
    if [ ! -d "$output_filepath" ]; then
        mkdir "$output_filepath"
    fi

    if [ ! -d "$sharable_resumes_filepath" ]; then
        mkdir "$sharable_resumes_filepath"
    fi

    # Compile the LaTeX file
    pdflatex -output-directory="$sharable_resumes_filepath" "$filename" 
    
    # Delete build artifacts
    rm "$sharable_resumes_filepath"/*.aux "$sharable_resumes_filepath"/*.log "$sharable_resumes_filepath"/*.out
    echo "Compilation of $filename completed."
}

function clean_pycache {
    find . -type d -name "__pycache__" -exec rm -r {} +
    echo "All __pycache__ directories have been removed."
}

function run_resume_tailor_ui {
    python /workspace/main.py
}

function list_alias_functions {
    grep -E '^function [a-zA-Z_][a-zA-Z0-9_]*' /workspace/.devcontainer/aliases.sh | sed 's/function \([a-zA-Z_][a-zA-Z0-9_]*\).*/\1/'
}