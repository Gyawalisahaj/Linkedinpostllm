import pandas as pd
import json 
import os

class FewShotPosts:
    def __init__(self, file_path=None):
        # If no path is provided, calculate it relative to this script
        if file_path is None:
            # os.path.dirname(os.path.abspath(__file__)) gets the folder where few_shot.py lives
            base_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(base_dir, "data", "processed_post.json")
        
        self.df = None
        self.unique_tags = None
        self.load_posts(file_path)

    def load_posts(self, file_path):
        # Safety check: helpful for debugging on Linux
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Could not find processed_post.json at {file_path}. "
                                    f"Ensure you ran the preprocessor first!")

        with open(file_path, encoding="utf-8") as f:
            post = json.load(f)
            self.df = pd.json_normalize(post)
            self.df["length"] = self.df["line_count"].apply(self.categorize_length)
            
            # Extract unique tags efficiently
            all_tags = self.df['tags'].explode().unique()
            self.unique_tags = set(all_tags)

    def categorize_length(self, line_count):
        if line_count < 5:
            return "Short"
        elif 5 <= line_count <= 10:
            return "Medium"
        else:
            return "Long"

    def get_tags(self):
        # Filter out nan values from tags
        return {tag for tag in self.unique_tags if pd.notna(tag)}

    def get_languages(self):
        # Return only English and Nepali languages
        allowed_languages = ["English", "Nepali"]
        available = sorted([lang for lang in self.df['language'].unique() if lang in allowed_languages])
        return available

    def get_filtered_posts(self, length, language, tag):
        df_filtered = self.df[
            (self.df['language'] == language) &
            (self.df['length'] == length) &
            (self.df['tags'].apply(lambda tags: tag in tags))
        ]
        return df_filtered.to_dict(orient='records')

if __name__ == "__main__":
    fs = FewShotPosts()
    # Note: Ensure these values exist in your JSON or it will return an empty list
    posts = fs.get_filtered_posts("Medium", "Nepali", "Job Search")
    print(posts)