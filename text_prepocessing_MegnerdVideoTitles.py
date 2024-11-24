import pandas as pd
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK data files if not already downloaded
nltk.download('punkt_tab')
nltk.download('stopwords')

def preprocess_title(title):
    """
    Preprocess a single video title.
    Steps:
    1. Remove punctuation
    2. Convert to lowercase
    3. Tokenize the text
    4. Remove stopwords
    :param title: Original title as a string.
    :return: Preprocessed list of tokens.
    """
    # Remove punctuation
    title_no_punct = title.translate(str.maketrans('', '', string.punctuation))

    # Convert to lowercase
    title_lower = title_no_punct.lower()

    # Tokenize the text
    tokens = word_tokenize(title_lower)

    # Remove stopwords
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]

    return filtered_tokens

def preprocess_titles_in_dataframe(df):
    """
    Apply preprocessing to the 'Title' column of a DataFrame.
    :param df: Input DataFrame containing a 'Title' column.
    :return: DataFrame with a new 'Processed Title' column.
    """
    df['Processed Title'] = df['Title'].apply(preprocess_title)
    return df

def main():
    # Load the YouTube channel data
    input_file = r'C:\Users\nehla\OneDrive\Documents\Projects\Webscraping\YoutubeDataScrapping\Meghnerd_channel_data.xlsx'  # Replace with the actual file path
    df = pd.read_excel(input_file)

    print("\nOriginal Data:")
    print(df.head())

    # Preprocess the 'Title' column
    print("\nPreprocessing titles...")
    df = preprocess_titles_in_dataframe(df)

    # Save the updated DataFrame
    output_file = 'Meghnerd_channel_data_preprocessed.xlsx'
    df.to_excel(output_file, index=False)

    print("\nPreprocessed Data:")
    print(df.head())
    print(f"\nPreprocessed data has been saved to {output_file}")

if __name__ == "__main__":
    main()
