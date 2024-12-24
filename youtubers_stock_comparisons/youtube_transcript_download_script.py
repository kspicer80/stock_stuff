import re
import spacy
from youtube_transcript_api import YouTubeTranscriptApi

nlp = spacy.load("en_core_web_lg")

def get_youtube_transcript(video_id):
    """
    Fetch the transcript for a given YouTube video ID.
    Returns:
        A list of dictionaries, where each dictionary represents a segment of the transcript 
        with keys like 'text', 'start', and 'duration'.
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        print(f"Error fetching transcript for {video_id}: {e}")
        return None

def extract_ticker_symbols(text):
    """
    Extract potential stock ticker symbols from the given text.
    Args:
        text (str): The text to search through.
    Returns:
        list: A list of potential stock ticker symbols.
    """
    # Regular expression pattern for stock ticker symbols (e.g., AAPL, TSLA)
    pattern = r'\b[A-Z]{1,5}\b'
    return re.findall(pattern, text)

def extract_company_names(text):
    """
    Extract potential company names from the given text using spaCy.
    Args:
        text (str): The text to search through.
    Returns:
        list: A list of potential company names.
    """
    doc = nlp(text)
    company_names = [ent.text for ent in doc.ents if ent.label_ == "ORG"]
    return company_names

# Example usage
video_id = "AAaVjzEj1F8&t=2s" 
transcript = get_youtube_transcript(video_id)

if transcript:
    # Process the transcript (e.g., save to file, analyze text)
    full_text = " ".join(segment['text'] for segment in transcript)
    
    ticker_symbols = extract_ticker_symbols(full_text)
    print("Extracted Ticker Symbols:")
    for symbol in ticker_symbols:
        print(symbol)
    
    company_names = extract_company_names(full_text)
    print("Extracted Company Names:")
    for name in company_names:
        print(name)
