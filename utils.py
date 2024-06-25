import tiktoken
from bs4 import BeautifulSoup
import PyPDF2
import os
from langchain_openai import AzureChatOpenAI
from langchain_openai import ChatOpenAI
from langchain_google_vertexai import VertexAI
from langchain_core.output_parsers import JsonOutputParser,StrOutputParser
from dotenv import load_dotenv
from typing import Optional,Any, List
from langchain.prompts import ChatMessagePromptTemplate, ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate


def num_tokens_from_string(string: str, encoding_name: str = "cl100k_base") -> int:
    """
    Computes the number of tokens in a string using a specified encoding.

    Parameters:
        string (str): The input string to be tokenized.
        encoding_name (str): The name of the token encoding model (default is 'cl100k_base').

    Returns:
        int: The number of tokens in the input string as determined by the encoding model.
    """
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens

def _read_pdf_w_pypdf(file_path: str) -> str:
    """
    Extracts and concatenates text from all pages of a PDF file using PyPDF2.

    Parameters:
        file_path (str): The path to the PDF file from which text is to be extracted.

    Returns:
        str: The concatenated text extracted from all the pages of the PDF file.

    Note:
        This function directly extracts text without any text normalization or preprocessing.
    """
    parsed_text = ''

    # Open the PDF file
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        for page_number in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_number]
            # Extract text directly without normalization
            extracted_text = page.extract_text() or ""
            parsed_text += extracted_text

    return parsed_text

def initialize_llm():
    """
    Initializes a large language model (LLM) based on the specified provider

    Raises:
        ValueError: If an unsupported provider is specified.
    """
    
    if  os.getenv("MODEL_PROVIDER")=='openai':
        llm = ChatOpenAI(
            api_key=os.getenv("OPEN_API_KEY"),
            model=os.getenv("MODEL_NAME"),
            max_tokens=os.getenv("MAX_TOKENS")
        )
    elif os.getenv("model_provider")=='google':
        llm = VertexAI(model_name=os.getenv("MODEL_NAME"))

    elif os.getenv("model_provider")=='azure_openai':
        llm = AzureChatOpenAI(
            azure_endpoint=os.getenv("LLM_AZURE_OPENAI_ENDPOINT"),
            openai_api_version=os.getenv("LLM_OPENAI_API_VERSION"),
            api_key=os.getenv("LLM_AZURE_OPENAI_API_KEY"),
            azure_deployment=os.getenv("MODEL_NAME"),
            max_tokens=os.getenv("MAX_TOKENS")
        )
    else:
        raise ValueError("Unsupported provider. Please choose 'openai', 'google', or 'azure'.")

    return llm


def get_runnable(llm: Any, system_message: str, human_message : str) -> Any:
    """
    Constructs a runnable pipeline for a language model (LLM) based on provided system and human message templates.

    Parameters:
        llm (Any): An instance of a large language model.
        system_message_list (List[str]): A list of template strings for system messages.
        human_message_list (List[str]): A list of template strings for human messages."""
    
    # Generate prompt templates for system and human messages
    system_template = SystemMessagePromptTemplate.from_template(system_message)
    human_template = HumanMessagePromptTemplate.from_template(human_message)
    prompt = ChatPromptTemplate.from_messages([system_template, human_template])

    # Initialize the output parser
    output_parser = StrOutputParser()

    # Compose the runnable pipeline
    runnable = prompt | llm | output_parser

    return runnable


def parse_exp_details(chain_output):

    soup = BeautifulSoup(chain_output, 'html.parser')

    # Initialize JSON structure
    resume_data = {}

    # Process job titles section
    job_titles_section = soup.find('section', class_='candidate-job-titles')
    job_titles = [li.text.strip() for li in job_titles_section.find_all('li', class_='job-title-name')]
    resume_data['job_titles'] = job_titles

    # Process experience entries
    experience_entries = []
    for idx,article in enumerate(soup.find_all('article', class_='experience-entry')):
        entry = {}
        entry['company_name'] = article.find('h2', attrs={"data-role": "company-name"}).text.strip()
        entry['job_title'] = article.find('h3', attrs={"data-role": "job-title"}).text.strip()
        try:
            end_date = article.find('time', attrs={"data-role": "end-date"}).text.strip()
        except AttributeError:  # Assuming the AttributeError if the element is not found
            
            end_date = 'NA'
        entry['employment_dates'] = {
            'start_date': article.find('time', attrs={"data-role": "start-date"}).text.strip(),
            'end_date': end_date
        }
        entry['job_location'] = article.find('p', attrs={"data-role": "job-location"}).text.strip()
        
        # Work description
        work_desc_items = article.find('section', class_='work-description').find_all('li', attrs={"data-role": "work_desc"})
        entry['work_description'] = [li.text.strip() for li in work_desc_items]
        
        # Technologies used
        technologies_items = article.find('section', class_='technologies-used').find_all('li', attrs={"data-role": "list of specific technologies used at particular role"})
        entry['technologies_used'] = [li.text.split(',') for li in technologies_items]
        
        experience_entries.append(entry)

    resume_data['experience_entries'] = experience_entries

    return resume_data


def parse_education_details(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Initialize JSON structure
    resume_data = {}

    # Process education overview section
    education_section = soup.find('section', class_='candidate-education-history')
    degree_names = [li.text.strip() for li in education_section.find_all('li', class_='degree-name')]
    resume_data['education_overview'] = degree_names

    # Process individual education entries
    education_entries = []
    for article in soup.find_all('article', class_='education-entry'):
        entry = {}
        entry['institution_name'] = article.find('h2', attrs={"data-role": "institution-name"}).text.strip()
        entry['degree_title'] = article.find('h3', attrs={"data-role": "degree-title"}).text.strip()

        # Course duration
        start_date = article.find('time', attrs={"data-role": "start-date"}).text.strip()
        try:
            end_date = article.find('time', attrs={"data-role": "end-date"}).text.strip()
        except AttributeError:  # Handling if the end date is not present
            end_date = 'present'
        entry['course_duration'] = {'start_date': start_date, 'end_date': end_date}

        entry['location'] = article.find('p', attrs={"data-role": "location"}).text.strip()

        # Detailed course information
        course_details_items = article.find('section', class_='course-details').find_all('li')
        entry['major-name'] = None
        entry['additional_details'] = {}

        for li in course_details_items:
            detail_key = li['data-role']
            detail_value = li.text.split(': ')[1] if ':' in li.text else li.text
            
            if detail_key == 'major-name':
                entry['major-name'] = detail_value
            else:
                entry['additional_details'][detail_key] = detail_value

        education_entries.append(entry)

    resume_data['education_entries'] = education_entries

    return resume_data