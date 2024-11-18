import os
from pathlib import Path
import html

def generate_logo_ticker(images_dir: str, base_url: str, output_file: str = "logo-ticker.html"):
    """
    Generate an HTML file with an infinitely scrolling logo ticker.
    Each image tag will be on a separate line for better readability.
    Supports both SVG and PNG image files.
    
    Args:
        images_dir: Directory containing SVG and PNG files
        base_url: Base URL for the image files
        output_file: Output HTML file name
    """
    # Get all SVG and PNG files from the directory
    image_files = []
    for extension in ['*.svg', '*.png']:
        for file in Path(images_dir).glob(f"**/{extension}"):
            relative_path = str(file.relative_to(images_dir))
            image_files.append(relative_path)
    
    # Sort files for consistent ordering
    image_files.sort()
    
    if not image_files:
        print(f"Warning: No SVG or PNG files found in {images_dir}")
        return
    
    # Calculate the total translation distance based on number of logos
    # Each logo takes 10rem of space (8rem width + 2rem margins)
    total_logos = len(image_files)
    translation_distance = total_logos * 10

    # CSS for the ticker animation with dynamic translation
    css = f"""
<style>
@keyframes ticker-kf {{
    0% {{
        transform: translateX(0);
    }}
    100% {{
        transform: translateX(-{translation_distance}rem);
    }}
}}

.img-ticker {{
    display: flex;
    margin-left: -1rem;
    margin-right: -1rem;
    animation: ticker-kf {total_logos}s linear infinite;
}}

.tickerlogo {{
    width: 8rem;
    flex: none;
    margin: 0 1rem 0 1rem;
    align-self: flex-start;
    max-width: 100%;
    height: auto;
}}
</style>
"""
    
    # Generate image tags, each on a new line with proper indentation
    image_tags = []
    for image_file in image_files:
        # Create the full URL by joining base_url and file path
        full_url = f"{base_url.rstrip('/')}/{image_file}"
        # Get file name for alt text
        file_name = Path(image_file).stem
        # Create the image tag with escaped URL and alt text, indented with 12 spaces
        image_tag = f'            <img class="tickerlogo" src="{html.escape(full_url)}" alt="{html.escape(file_name)} logo">'
        image_tags.append(image_tag)
    
    # Double the images to ensure smooth infinite scrolling
    #image_tags = image_tags * 2
    
    # Join image tags with newlines
    images_html = '\n'.join(image_tags)
    
    # Generate the complete HTML with proper formatting
    html_content = f"""{css}
<!-- Wrap the slider in div with overflow hidden to hide scrollbars -->
<div style="overflow: hidden; width: 100%;">
<!-- The slider itself is a flex grid -->
<div class="img-ticker">
<!-- Each image is a grid column with width 8rem and horizontal margin 2rem = 10rem -->
{images_html}
</div>
</div>
"""
    
    # Create output directory if it doesn't exist
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write the HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated logo ticker HTML file: {output_file}")
    print(f"Found {len(image_files)} image files")

if __name__ == "__main__":
    # Example usage
    images_dir = "images"  # Directory containing SVG and PNG files
    base_url = "https://raw.githubusercontent.com/dcg-ai/logos/refs/heads/main/images/"
    generate_logo_ticker(images_dir, base_url)