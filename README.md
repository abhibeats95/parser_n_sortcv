# CV Sorting Application

Welcome to the CV Sorting Application! This project uses LangChain to parse and sort CVs based on job descriptions. The application employs two parsers: one for parsing job descriptions and another for parsing CVs. This is the first commit of the project, providing the foundational functionality to parse and sort documents.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Job Description Parser**: Extracts key information from job descriptions.
- **CV Parser**: Extracts relevant information from CVs.
- **Sorting Mechanism**: Sorts CVs based on their relevance to the job descriptions.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/cv-sorting-application.git
    cd cv-sorting-application
    ```

2. Create and activate a virtual environment (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Ensure you have your job descriptions and CVs in the appropriate format (e.g., text files, PDFs).

2. Run the application:
    ```bash
    python main.py
    ```

3. Follow the on-screen instructions to input the job description and CVs.

4. The application will output the sorted list of CVs based on their relevance to the job description.

## Run CV Parser:

1. **Running the Application**:
   - Execute the script with the necessary arguments specifying the input directory for CVs and the output directory for JSON files. Optionally, you can include flags to customize how skills are parsed from the resumes.

   - **Flags Description**:
     - `--parse_skill_fm_section`: Enables parsing of skills from the specific skills section of the resume.
     - `--parse_skills_as_cate`: Enables parsing of skills by scanning the entire resume and categorizing them into subcategories (e.g., programming languages skills, cloud skills).

    - **LLM setup in .env**
    Specify the model provider and model name

   - **Example Command**:
     ```bash
     python parser_cv.py <input_directory> <output_directory> [--parse_skill_fm_section] [--parse_skills_as_cate]
     ```

2. **Output**:
   - The script will process each CV and generate a JSON file in the specified output directory for each resume. These files will include detailed structured data extracted from the resumes, such as personal information, experience, education, and skills.


## File Structure
yet to be decided