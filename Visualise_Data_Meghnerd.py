import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud, STOPWORDS
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords as nltk_stopwords
import string

def load_data(file_path):
    """
    Load the preprocessed YouTube data from an Excel file.
    """
    try:
        df = pd.read_excel(file_path)
        print("Data loaded successfully!")
        return df
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None

def preprocess_title(title):
    """
    Preprocess a single video title:
    - Lowercase the text
    - Remove punctuation
    - Tokenize the words
    - Remove stopwords
    """
    stop_words = set(nltk_stopwords.words('english'))
    if pd.isnull(title):
        return ""
    # Lowercase
    title = title.lower()
    # Remove punctuation
    title = title.translate(str.maketrans("", "", string.punctuation))
    # Tokenize
    tokens = word_tokenize(title)
    # Remove stopwords
    tokens = [word for word in tokens if word not in stop_words]
    # Rejoin tokens to form a processed string
    return " ".join(tokens)

def preprocess_titles(df):
    """
    Apply title preprocessing to the Title column.
    """
    df['Processed Title'] = df['Title'].apply(preprocess_title)
    return df

def visualize_views_distribution(df, save_path="views_distribution.png"):
    """
    Visualize the distribution of video views and save as an image.
    """
    df['Views'] = pd.to_numeric(df['Views'], errors='coerce')
    plt.figure(figsize=(10, 6))
    sns.histplot(df['Views'], bins=30, kde=True, color='blue')
    plt.title('Distribution of Video Views', fontsize=16)
    plt.xlabel('Views', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.grid(True)
    plt.savefig(save_path)  # Save the plot as an image
    plt.close()
    print(f"View distribution saved as {save_path}")

def visualize_duration_categories(df, save_path="duration_categories.png"):
    """
    Visualize the count of videos in each duration category and save as an image.
    """
    plt.figure(figsize=(12, 8))
    ax = sns.countplot(x='Duration (Category)', data=df, palette='viridis', order=df['Duration (Category)'].value_counts().index)
    plt.title('Video Count by Duration Category', fontsize=16, pad=20)
    plt.xlabel('Duration Category', fontsize=14, labelpad=10)
    plt.ylabel('Count', fontsize=14)
    plt.xticks(rotation=45)
    plt.grid(True, axis='y')
    
    # Adjust bottom margin to prevent x-axis label cutoff
    plt.subplots_adjust(bottom=0.2)
    
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight', dpi=300, pad_inches=0.5)
    plt.close()
    print(f"Duration category plot saved as {save_path}")

def top_performing_videos(df, n=10, save_path="top_videos.png"):
    """
    Display the top N videos by views in a bar chart and save as an image.
    """
    df['Views'] = pd.to_numeric(df['Views'], errors='coerce')
    top_videos = df.nlargest(n, 'Views')
    
    # Create figure with larger size and more width for labels
    plt.figure(figsize=(16, 10))
    
    # Create the plot
    ax = sns.barplot(
        x='Views',
        y='Title',
        data=top_videos,
        palette='coolwarm'
    )
    
    # Truncate long titles to prevent overflow
    ax.set_yticklabels([label.get_text()[:50] + '...' if len(label.get_text()) > 50 else label.get_text() 
                        for label in ax.get_yticklabels()])
    
    plt.title(f'Top {n} Performing Videos by Views', fontsize=16, pad=20)
    plt.xlabel('Views', fontsize=14)
    plt.ylabel('Video Title', fontsize=14)
    
    # Adjust left margin to prevent y-axis label cutoff
    plt.subplots_adjust(left=0.3)
    
    plt.tight_layout()
    plt.savefig(save_path, bbox_inches='tight', dpi=300, pad_inches=0.5)
    plt.close()
    print(f"Top performing videos plot saved as {save_path}")

def generate_wordcloud(df, save_path="wordcloud.png"):
    """
    Generate and save a word cloud for the Title column.
    """
    # Combine all processed titles into a single string
    text = ' '.join(df['Processed Title'].dropna().tolist())
    
    # Set stopwords
    stopwords = set(STOPWORDS)
    
    # Generate the WordCloud
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        stopwords=stopwords,
        colormap='viridis'
    ).generate(text)
    
    # Save the WordCloud
    plt.figure(figsize=(12, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud of Processed Video Titles', fontsize=16)
    plt.savefig(save_path)  # Save the word cloud as an image
    plt.close()
    print(f"Word cloud saved as {save_path}")

def save_data_for_tableau(df, output_path="Meghnerd_channel_data_for_tableau.csv"):
    """
    Save the data in a format compatible with Tableau (CSV), including processed titles.
    """
    df.to_csv(output_path, index=False)
    print(f"Data saved for Tableau at {output_path}")

def main():
    file_path = 'Meghnerd_channel_data.xlsx'
    
    # Load the data
    df = load_data(file_path)
    if df is None:
        return

    # Preprocess titles
    df = preprocess_titles(df)

    # Save visualizations
    visualize_views_distribution(df)
    visualize_duration_categories(df)
    top_performing_videos(df)
    generate_wordcloud(df)

    # Save data for Tableau
    save_data_for_tableau(df)

if __name__ == "__main__":
    main()
