import os
import json
import json_repair
import argparse
from tqdm import tqdm 

from utils import _read_pdf_w_pypdf, initialize_llm, get_runnable
from utils import parse_exp_details, parse_education_details

from prompts import (EXP_SYS, EXP_HUM,
                     SKILL_SPECIFIC_SYS, SKILL_SPECIFIC_HUM,
                     SKILL_DETAIL_SYS, SKILL_DETAIL_HUM, SKILL_LIST_SYS, SKILL_LIST_HUM,
                     EDU_SYS, EDU_HUM, PRD_SYS, PRD_HUM)


def main(data_dir, output_dir, parse_skill_fm_section=False, parse_skills_as_cate=False):
    """
    Processes and extracts detailed information from CVs stored in a specified directory using an LLM.

    Parameters:
        data_dir (str): Directory containing PDF resumes.
        output_dir (str): Directory where the extracted details will be saved as JSON files.
        parse_skill_fm_section (bool): Flag to parse skills from a specific section (default False).
        parse_skills_as_cate (bool): Flag to parse skills as categories (default False).

    This function:
    - Iterates over each PDF resume in the data directory.
    - Initializes an LLM with specific parameters.
    - Extracts various details like personal information, experience, skills, and education from each CV.
    - Saves each CV's extracted data as a JSON file in the output directory."""
    try:
        # Check if output directory exists, create it if not
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Fetch the list of files in the directory
        file_names = os.listdir(data_dir)
        if not file_names:
            raise FileNotFoundError("No files found in the specified data directory.")

        # Process each file with a progress bar
        for file_name in tqdm(file_names, desc="Processing Resumes", unit="file"):
            file_path = os.path.join(data_dir, file_name)
            resume_text = _read_pdf_w_pypdf(file_path)
            llm = initialize_llm()
            cv_details = {}

            # Extract details as previously coded
            prd_parse_chain = get_runnable(llm, PRD_SYS, PRD_HUM)
            msg_prd = prd_parse_chain.invoke({'resume': resume_text})
            cv_details['PERSONAL_INFO'] = json_repair.loads(msg_prd)

            # Similar extraction for experience, education, and skills
            exp_parse_chain = get_runnable(llm, EXP_SYS, EXP_HUM)
            msg_exp = exp_parse_chain.invoke({'resume': resume_text})
            cv_details['EXPERIENCE'] = parse_exp_details(msg_exp)

            edu_parse_chain = get_runnable(llm, EDU_SYS, EDU_HUM)
            msg_edu = edu_parse_chain.invoke({'resume': resume_text})
            cv_details['EDUCATION'] = parse_education_details(msg_edu)

            if parse_skill_fm_section:
                skill_parse_chain = get_runnable(llm, SKILL_SPECIFIC_SYS, SKILL_SPECIFIC_HUM)
            elif parse_skills_as_cate:
                skill_parse_chain = get_runnable(llm, SKILL_DETAIL_SYS, SKILL_DETAIL_HUM)
            else:
                skill_parse_chain = get_runnable(llm, SKILL_LIST_SYS, SKILL_LIST_HUM)
            msg_skills = skill_parse_chain.invoke({'resume': resume_text})
            cv_details['SKILLS'] = json_repair.loads(msg_skills)

            # Save the cv_details as json in the output directory
            output_file_path = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}_details.json")
            with open(output_file_path, 'w') as json_file:
                json.dump(cv_details, json_file, ensure_ascii=False, indent=4)

    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process CVs to extract information.")
    parser.add_argument('data_dir', type=str, help='Directory containing PDF resumes.')
    parser.add_argument('output_dir', type=str, help='Output directory for JSON files.')
    parser.add_argument('--parse_skill_fm_section', action='store_true', help='Flag to parse skills from a specific section.')
    parser.add_argument('--parse_skills_as_cate', action='store_true', help='Flag to parse skills as categories.')
    args = parser.parse_args()

    main(args.data_dir, args.output_dir, args.parse_skill_fm_section, args.parse_skills_as_cate)
