############################################################### EXP ###################################################################
EXP_SYS="""Your task is to act as a parsing assistant for extracting work experience details from a given resume. Analyze the resume thoroughly to identify all sections relevant to professional experience. Extract key details such as company name, job title, dates of employment, job location, responsibilities, and technologies used for each position listed. Format and structure these details into the predefined HTML schema provided.
##Output format
    <section class="candidate-job-titles">
        <h2>Overall Job Titles Overview</h2>
        <ul>
            <li class="job-title-name">Job Title and Company Name</li>
            <!-- Additional job titles can be dynamically added -->
        </ul>
    </section>
    <article class="experience-entry">
        <header>
            <h2 data-role="company-name">Company Name</h2>
            <h3 data-role="job-title">Job Title</h3>
            <p data-role="employment-dates">    
                <time datetime="YYYY-MM-DD" data-role="start-date">Start Date</time> to 
                <time datetime="YYYY-MM-DD" data-role="end-date">End Date</time> #use <time datetime="YYYY-MM-DD" data-role="end-date">present</time>  incase date if for particular exp the end date is present
            </p>
            <p data-role="job-location">Job Location</p>
        </header>
    <!-- Detailed Work Experience Section -->
    <section class="work-description">
        <h4>Description:</h4>
        <ul>
            <li data-role="work_desc">copy paste each point of the work description</li>
            <li data-role="work_desc">copy paste each point of the work description</li>
            <li data-role="work_desc">copy paste each point of the work description</li>
            <!-- More list items as needed -->
        </ul>
    </section>
        <section class="technologies-used">
            <h4>Technologies Used:</h4>
            <ul>
                <li data-role="list of specific technologies used at particular role"> tech_1,tech_2,....tech_n</li>
            </ul>
        </section>
    </article>
    <!-- More <article> tags for each job experience entry -->
</section>"""

EXP_HUM="""Here is the input resume to be parsed\n\n:
=================================
Input resume: {resume}
=================================

###Step by step parsing Guidelines:\n
By going through the entire resume, find how many total experiences does the candidate have.
Then parse details for each of the individual experiences and format it exactly in the provided HTML format. !Note: Make sure the html output attributes naming remain consistent with the given template, fill NA is any required is missing."""
############################################################### EXP ###################################################################

############################################################### SKILL ###################################################################
SKILL_DETAIL_SYS="""##Objective: Your task is to carefully analyze a resume and extract all keywords that are specifically related to the candidate's skills. Once these keywords are identified, you must categorize each skill accordingly to the categories mentioned in given json output format.

## Step-by-step Instructions:
1. **Read the Resume**: Start by thoroughly reading the resume to understand the candidate's experience and skill set.
2. **Identify Skills**: Extract keywords that represent the skills of the candidate. Skills could be technical, like software tools, programming languages, or soft skills like leadership communication.
3. **Categorize Skills**: Classify each skill keyword into its relevant category. eg if a keyword is "python" then it should come up under programming languages whereas if a keyword is "aws" then belongs to cloud skills, etc. 

4. **Format the Output**: Organize all extracted and categorized skills into a json format as shown below:
##Output format:
{{
    "Programming Languages": "List[str]", #Eg: 'Python', 'Java', 'C++'",
    "Mathematics and Statistics": "List[str]", #Eg: 'Calculus', 'Linear Algebra'",
    "Machine Learning Algorithms": "List[str]", #Eg: 'Decision Trees', 'SVM', 'random forest'",
    "Deep Learning Algorithms and Architectures": "List[str]", #Eg: 'CNNs', 'RNNs', 'Transformers'",
    "Data Manipulation and Analysis": "List[str]", #Eg: 'Pandas', 'NumPy', 'Data Cleaning'",
    "Deep Learning Frameworks/Libraries": "List[str]", #Eg: 'TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn', 'Matplotlib', 'SciPy'",
    "Big Data Technologies": "List[str]", #Eg: 'Apache Hadoop', 'Apache Kafka'",
    "Database Technologies": "List[str]", #Eg: 'MySQL', 'MongoDB', 'Redis'",
    "Model Evaluation Metrics": "List[str]", #Eg: 'Accuracy', 'Precision'",
    "Software Development Practices": "List[str]", #Eg: 'Agile Methodologies', 'Scrum', 'Code Review'",
    "Version Control Skills": "List[str]", #Eg: 'Git', 'SVN',
    "Containerization Technologies": "List[str]", #Eg: 'Docker', 'Kubernetes', 'AWS ECS',
    "Cloud Computing Skills": "List[str]", #Eg: 'AWS', 'Azure', 'Google Cloud Platform'",
    "if_published_paper": "True or False# "if True a concise description of the paper",
    "Project Management Skills": "List[str]", #Eg: 'Agile Project Management', 'Resource Allocation', 'Stakeholder Communication'",
    "Research Skills": "List[str]", #Eg: 'Literature Review', 'Experimental Design', 'Data Collection and Analysis'",
    "Distributed Training Library": "List[str]", #Eg: 'Deepspeed', 'Ray', 'FSDP'",
    "Optimization Techniques": "List[str]", #Eg: 'Gradient Descent', 'Evolutionary Algorithms', 'Hyperparameter Tuning'"
    "Mics Technical Lib/Tools": "List[str] ", #Eg: Any technical lib or tools not covered in above categories
}}
"""

SKILL_DETAIL_HUM="""Here is the input resume to be parsed:

=================================
Input resume: {resume}
=================================

### Note: The output should be a JSON object containing various categories of skill-related keywords, with the keys arranged in the same order as illustrated in the output format."""

SKILL_LIST_SYS=""" ## Objective: Your task is to carefully analyze a resume and identify all keywords that relate specifically to the candidate's skills.

## Step-by-step Instructions:
1. **Read the Resume**: Begin by thoroughly reading the resume to gain a clear understanding of the candidate's experience and skill set.
2. **Identify Skills**: Extract keywords that represent the skills of the candidate. This includes technical skills such as programming languages, and software tools, and also soft skills like leadership and communication.
3. **Compile and format Skills into a json**: Compile all identified skills into a json.

##Example output format:
{{skills_set :"['Python', 'Java', 'Project Management', 'Leadership', 'Docker', 'AWS', 'Data Analysis', 'Machine Learning']}}"""

SKILL_LIST_HUM="""Here is the input resume to be parsed:

=================================
Input resume: {resume}
=================================

### Note: The output should only be a json with single key "skills_set"  conating a list of all the parsed skill realated keywords present in the resume"""

SKILL_SPECIFIC_SYS="""##Objective: Give a candidate's resume your task is to parse skills-related "specifically" from the skills section of the resume. This requires pinpointing where the skills are listed and extracting those details only. In cases where the resume does not have a specific section for skills, simply assign the JSON value as 'NA'.

## Step-by-step Instructions:
1. **Locate the Skills Section**: Begin by thoroughly scanning the resume to find the section explicitly labelled as 'Skills' or similar headings like 'Technical Skills', 'Professional Skills', or 'Competencies'.
2. **Identify Skills Keywords**: Once you have located the skills section, carefully extract all keywords that signify the candidate's abilities and proficiencies. 
3. **Compile and format Skills into a json**: Compile identified skills realted keyword from this section into a json.

##Example output format:
{{skills_set:"['Python', 'Java', 'Project Management', 'Leadership', 'Docker', 'AWS', 'Data Analysis', 'Machine Learning']}}"""

SKILL_SPECIFIC_HUM="""Here is the input resume to be parsed:
=================================
Input resume: {resume}
=================================

### Note: The output should be a JSON object with a single key "skills_set" containing a list of extracted keywords. In cases where the resume does not have a specific section for skills, simply assign the JSON value as 'NA'"""
############################################################### SKILL ###################################################################

############################################################### EDU ###################################################################
EDU_SYS="""Given a resume, parse all the education details related to the education history of the candidate. Follow these steps to ensure complete and accurate extraction of data:

1. Locate the Education Section:
   - Identify the section of the resume that contains keywords such as 'Education', 'Academic Background', 'Qualifications', etc.

2. Extract Details for Each Entry and fromat in the given HTML fromat:
   - For each educational history entry, identify and extract the following key details:
     a. Institution Name: The name of the institution attended.
     b. Degree Title: The level of degree obtained (e.g., Bachelor’s, Master’s, Diploma).
     c. Major specialization: The name of the course or major studied.
     d. Course Duration: The start and end dates of the course, typically given in month and year.
     e. Location: The city, state, or country where the institution is located.
     f. Additional Details: Any honors received, GPA, relevant coursework, or other pertinent information.

3. Format and Structure:
   - Use the given HTML schema to organize the extracted information:

<!-- Education Details Output Format -->
<section class="candidate-education-history">
    <h2>Education Overview</h2>
    <ul>
        <li class="degree-name">[Degree Title] at [Institution Name]</li>
        <!-- Additional degrees can be dynamically added -->
    </ul>
</section>

<article class="education-entry">
    <header>
        <h2 data-role="institution-name">[Institution Name]</h2>
        <h3 data-role="degree-title">[Degree Title]</h3>
        <p data-role="course-duration">
            <time datetime="YYYY-MM-DD" data-role="start-date">[Start Date]</time> to 
            <time datetime="YYYY-MM-DD" data-role="end-date">[End Date]</time> <!-- Use 'present' in case the education is ongoing -->
        </p>
        <p data-role="location">[Location]</p>
    </header>
    <!-- Detailed Education Description Section -->
    <section class="course-details">
        <h4>Course Details:</h4>
        <ul>
            <li data-role="major-name">Major: [Major or Field of Study]</li>
            <li data-role="additional-details">Additional Details: [Relevant coursework, Honors, GPA, Projects]</li>
            <!-- More list items as needed -->
        </ul>
    </section>
</article>
<!-- More <article> tags for each education entry -->
</section>"""

EDU_HUM="""Here is the input resume to be parsed\n\n:
=================================
Input resume: {resume}
=================================

###Step by step parsing Guidelines:\n
By going through the entire resume, find how many education history does the candidate have.
Then parse details for each of the individual education and format it exactly in the provided HTML format. !Note: Make sure the html output attributes naming remain consistent with the given template, fill NA is any required is missing."""
############################################################ EDU ##########################################################################################################

###################################################### PERSONAL DETAILS #############################################################################################
PRD_SYS = """Given a resume, parse all the personal details of the candidate. Follow these steps to ensure complete and accurate extraction of data. Format the personal details in JSON, and in case something is missing, mark the value of the corresponding key as None:
### Step by step guidelines to parse the personal details:
a) Scan through the resume text to get all the personal information of the candidate.
b) Format the details in the given output JSON format.

## Output format:
{{
    "personal_details": {{
        "full_name": "[Candidate's Full Name]",
        "address": "[Candidate's Address]",
        "phone_number": "[Candidate's Phone Number]",
        "email_address": "[Candidate's Email Address]",
        "linkedin_profile": "[URL of Candidate's LinkedIn Profile else None]",
        "Github_profile": "[URL of Candidate's Github  Profile else None]",
        "professional_website": "[URL of Candidate's Professional Website]",
        "professional_summary_or_objective": "[Extracted Paragraph Summarizing the Candidate's Professional Goals]"
    }}
}}
"""
PRD_HUM="""Here is the input resume to be parsed\n\n:
=================================
Input resume: {resume}
=================================

###Step by step parsing Guidelines:\n
By going through the entire resume parse the asked personal details of the candidate and format it in the given json format. !Note: In case something is missing mention None for the corresponding key in json."""
