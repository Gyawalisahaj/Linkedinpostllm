import json
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from llm_helper import llm

# --- DYNAMIC PATH LOGIC ---
# Finds the directory where this script is saved
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Builds absolute paths to the data files
DEFAULT_RAW_PATH = os.path.join(BASE_DIR, 'data', 'raw_posts.json')
DEFAULT_PROCESSED_PATH = os.path.join(BASE_DIR, 'data', 'processed_post.json')

def process_post(raw_file_path=DEFAULT_RAW_PATH, processed_file_path=DEFAULT_PROCESSED_PATH):
    enriched_posts = []
    
    if not os.path.exists(raw_file_path):
        raise FileNotFoundError(f"Input file not found at: {raw_file_path}")

    # 1. Extract raw metadata from each post
    with open(raw_file_path, encoding='utf-8') as file:
        posts = json.load(file)
        for post in posts:
            metadata = extract_metadata(post['text'])
            post_with_metadata = post | metadata
            enriched_posts.append(post_with_metadata)

    # 2. Unify tags across all posts for consistency
    unified_tags = get_unified_tags(enriched_posts)

    # 3. Apply the unified tags back to the posts
    for post in enriched_posts:
        current_tags = post.get("tags", [])
        # Map original tags to their unified versions
        new_tags = {unified_tags.get(tag, tag) for tag in current_tags}
        post['tags'] = list(new_tags)

    # 4. Save the final enriched dataset
    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(processed_file_path), exist_ok=True)
    
    with open(processed_file_path, encoding='utf-8', mode="w") as outfile:
        json.dump(enriched_posts, outfile, indent=4)
    
    print(f"Success! Processed data saved to: {processed_file_path}")

def get_unified_tags(post_with_metadata):
    unique_tags = set()
    for post in post_with_metadata:
        unique_tags.update(post.get('tags', []))

    unique_tags_list = ', '.join(unique_tags)
    template = '''I will give you a list of tags. You need to unify tags with the following requirements:
    1. Tags are unified and merged to create a shorter list. 
       Example: "Jobseekers", "Job Hunting" -> "Job Search".
    2. Each tag should follow Title Case convention.
    3. Output must be a valid JSON object. No preamble.
    4. Mapping: {{"original_tag": "unified_tag"}}
    
    Tags: {tags}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={"tags": unique_tags_list})
    
    try:
        json_parser = JsonOutputParser()
        return json_parser.parse(response.content)
    except OutputParserException:
        raise OutputParserException("Failed to parse unified tags from LLM response.")

def extract_metadata(post):
    template = '''
    Extract metadata from this LinkedIn post. 
    1. Return valid JSON only. No preamble. 
    2. Keys: line_count (int), language (string), tags (list of strings). 
    3. Max 2 tags.
    4. Language: English or Nepali.
    
    Post: {post}
    '''
    pt = PromptTemplate.from_template(template)
    chain = pt | llm
    response = chain.invoke(input={'post': post})

    try: 
        json_parser = JsonOutputParser()
        return json_parser.parse(response.content)
    except OutputParserException:
        # Fallback in case of parsing error
        return {"line_count": 0, "language": "Unknown", "tags": []}

if __name__ == "__main__":
    process_post()