# Resume Screener

## Overview
The Resume Screener is a deep learning-based tool designed to evaluate the similarity between your resume and a given job description. This helps job seekers enhance the accuracy and relevance of their applications by identifying how well their resume aligns with specific job requirements.

## Features
- **Deep Learning-Based Similarity Analysis:** Uses advanced machine learning algorithms to compare resumes with job descriptions.
- **Customizable Metrics:** Allows users to tweak similarity thresholds for precise matching.
- **User-Friendly Interface:** Simple and intuitive design for seamless user experience.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd resume_screener
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv env
   source env/bin/activate   # On Windows: env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Requirements
The `requirements.txt` file includes the following dependencies:
```
Flask==2.3.2
sentence-transformers
pdfplumber==0.5.28
torch==2.0.1
```

## Usage

1. Place your resume and job description files in the designated folder (e.g., `input/`).
2. Run the script:
   ```bash
   python resume_screener.py --resume <resume_path> --job_description <job_description_path>
   ```
3. View the similarity score and insights provided by the tool.

## Example

```bash
python resume_screener.py --resume sample_resume.pdf --job_description job_desc.txt
```
**Output:**
```
Similarity Score: 85%
Insights: Strong match in technical skills and experience. Consider tailoring the resume to emphasize leadership abilities.
```

## Dependencies
- Python >= 3.7
- Flask==2.3.2
- sentence-transformers
- pdfplumber==0.5.28
- torch==2.0.1

## Contributing
We welcome contributions! Please fork the repository and submit a pull request with your changes. Ensure your code follows the project's style guide and includes necessary tests.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For questions or suggestions, please contact:
- **Author:** Ashish Kumar
- **Email:** [your_email@example.com](mailto:your_email@example.com)
