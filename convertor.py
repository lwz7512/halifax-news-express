import glob
import os
import json
import shutil
from datetime import datetime


def convert_json_to_markdown():
    """Convert JSON files in the data folder to Markdown format."""
    
    data_dir = 'data'
    output_dir = 'markdown_news'
    docs_dir = 'docs'
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    # Get the full path of the data directory relative to the current working directory
    data_dir = os.path.join(os.getcwd(), data_dir)
    # Use the glob module to find all files in the current directory with a ".json" extension.
    json_files = glob.glob(data_dir + '/*.json')
    # Sort the json files by creation time in descending order
    for json_path in sorted(json_files, key=os.path.getctime, reverse=True):
        # get the filename from the json_path
        filename = os.path.basename(json_path)
        
        # Read JSON file
        with open(json_path, 'r') as f:
            articles = json.load(f)
        
        # Create markdown filename (replace .json with .md)
        md_filename = filename.replace('.json', '.md')
        md_path = os.path.join(output_dir, md_filename)
        # Get the category from the filename
        category = md_filename.split('_')[1]
        # Get the date from the filename, remove the .md extension
        date = md_filename.split('_')[2][:-3]
        
        # Convert json file to markdown file
        with open(md_path, 'w') as f:
            f.write(f"# Halifax News Articles - {filename[3:-5]}\n\n")
            f.write(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
            
            for article in articles:
                # Write article title
                f.write(f"## {article['title']}\n\n")
                
                # Write metadata
                f.write(f"**Authors:** {', '.join(article['authors'])}\n\n")
                f.write(f"**Published:** {article['publish_date']}\n\n")
                
                if 'keywords' in article:
                    f.write(f"**Keywords:** {', '.join(article['keywords'])}\n\n")

                # Write summary
                f.write(f"**Summary:** {article['summary']}\n\n")
                
                # Write URL
                f.write(f"**Source:** [{article['url']}]({article['url']})\n\n")
                
                # Add separator between articles
                f.write("---\n\n")
        
        # print(f"Created markdown file: {md_path}")

        # Create index markdown file for the category inside docs folder
        index_path = os.path.join(docs_dir, category, 'index.md')
        with open(index_path, 'a') as f:
            # write the article link in the index markdown file
            f.write(f"[{category.capitalize()} {date}]({md_filename})\n\n")
        
        # copy the md_filename to the docs folder
        # print(f"Copying {md_filename} to {os.path.join(docs_dir, category, md_filename)}")
        shutil.copy(md_path, os.path.join(docs_dir, category, md_filename))
                
