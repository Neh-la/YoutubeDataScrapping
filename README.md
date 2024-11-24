# YouTube Channel Data Analysis Project

This project is designed to scrape and analyze YouTube channel data, specifically focusing on visualizing various metrics and insights from channel content.

## Features

- Data collection from YouTube channels
- Data preprocessing and cleaning
- Comprehensive data visualization including:
  - Video views distribution
  - Duration category analysis
  - Top performing videos analysis
  - Word cloud generation from video titles

## Visualizations

The project generates several visualizations:
1. **Views Distribution**: Histogram showing the distribution of video views
2. **Duration Categories**: Bar chart showing video count by duration category
3. **Top Performing Videos**: Bar chart of the most viewed videos
4. **Word Cloud**: Visual representation of common words in video titles

## Requirements

```
pandas
matplotlib
seaborn
wordcloud
nltk
```

## Project Structure

- `Visualise_Data_Meghnerd.py`: Main script for data visualization
- `Meghnerd_channel_data.xlsx`: Input data file
- Generated output files:
  - `views_distribution.png`
  - `duration_categories.png`
  - `top_videos.png`
  - `wordcloud.png`
  - `Meghnerd_channel_data_for_tableau.csv`

## Usage

1. Ensure you have the required packages installed
2. Place your YouTube channel data in an Excel file named `Meghnerd_channel_data.xlsx`
3. Run the visualization script:
   ```python
   python Visualise_Data_Meghnerd.py
   ```

## Output

The script generates several visualization files:
- Distribution plots of video metrics
- Category analysis visualizations
- Performance analysis charts
- Word cloud of video titles
- Tableau-compatible CSV file for further analysis

## Data Processing

The project includes:
- Title text preprocessing
- Data cleaning and formatting
- Categorical data analysis
- Numerical data visualization

## Contributing

Feel free to fork this repository and submit pull requests for any improvements.
