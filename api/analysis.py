import os
import glob
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()   
GOOGLE_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash') # or 'gemini-2.0-pro'
def analyze_batch_files(directory: str) -> str:
    """
    Analyzes text files in a directory and generates a summary focused on political/election influence.

    Args:
        directory: The directory containing the text files to analyze.

    Returns:
        A string containing the summary of the files.
    """

    all_analyses = []
    file_paths = glob.glob(os.path.join(directory, "*.txt"))  # Get all .txt files

    if not file_paths:
        return "No text files found in the specified directory."

    for file_path in file_paths:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                analysis = f.read()
                all_analyses.append(analysis)
        except Exception as e:
            print(f"Error reading file {file_path}: {e}")
            # Consider logging the error instead of printing.

    # Combine all analyses into a single string
    combined_analysis = "\n\n".join(all_analyses)

    prompt = f"""You are a skilled social media analyst preparing a report on online influence operations in the context of an upcoming election. You have been provided with results from 440 separate analyses of Reddit posts.

Your objective is to synthesize a comprehensive report (8-9 paragraphs) that mirrors the analytical style of professional reports, focusing on quantifying results and clearly explaining observed phenomena. The report should focus on how these findings suggest potential influence operations, echoing the style and tone of the example article provided. The report should highlight data on reach and how engagement is being leveraged.

Specifically, your report should address the following:

**I. Data Overview:** Begin with an overview of the analyzed Reddit data (440 analyses), estimating the number of users represented and the total interactions observed. Mirror the data format of the sample report

**II. Context of the Online Discourse:** Based on the analysis, describe the broader domestic and geopolitical contexts of this online environment.  Are there key events or social movements that are driving online conversations?

**III. Tactics & Behaviors of Key Actors:** What specific tactics are actors (users, groups, subreddits) using to disseminate information (or misinformation)? How is engagement being manipulated?  Provide examples and, where possible, quantify the prevalence of these tactics.

**IV. Coordination & Networks:** Is there evidence of coordinated activity among accounts or subreddits?  Describe the structure of any identified networks, and quantify the number of accounts involved, if possible. Discuss how they leverage various methods, such as shared content and cross-posting.

**V. Key Narratives & Messaging:** What are the dominant narratives or themes being promoted? What narratives related to disinfo, misinformation, and propaganda are prevalent? Analyze how parties are using and leveraging these tactics.

**VI. Answering the Underlying Questions:** Concisely address these questions based on the synthesis of ALL analyses:
    * What are the primary sources and accounts involved in the dissemination of misleading posts?
    * What are the main topics addressed by the misleading posts?
    * What overarching narratives or themes do these posts convey?
    * Is there evidence to suggest that the actors involved in spreading misinformation have a history of similar activity?
    * Are there indications of coordinated attacks or collaboration among multiple actors?
    * Are there specific channels or communities that consistently feature this type of messaging?

**VII. Impact on Online Constituencies:** How are these tactics and narratives potentially impacting online constituencies (specific subreddits or user groups)?

**VIII. Actionable Insights for Platforms:** Based on your analysis, what actions could social media platforms take to mitigate the spread of misinformation and counter influence operations? Provide key considerations for transparency.

Remember, your analysis should be strictly based on the 440 analyses provided. Emulate the structured, data-driven style of the example report. Your report will be written for a professional analyst. DO NOT introduce external information or make assumptions not supported by the data. Focus on a higher-level synthesis.

Here are the 440 analyses:
{combined_analysis}
"""

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error during analysis: {e}")
        return f"Analysis failed: {e}"


if __name__ == "__main__":
    directory_path = "batch_analyses"  # Replace with the actual directory
    summary = analyze_batch_files(directory_path)
    print("\nSummary:\n", summary)