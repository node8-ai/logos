import os
from pathlib import Path
import html

def generate_logo_ticker(images_dir: str, base_url: str, output_file: str = "logo-ticker.html"):
    """
    Generate an HTML file with an infinitely scrolling logo ticker.
    
    Args:
        images_dir: Directory containing SVG files
        base_url: Base URL for the SVG files
        output_file: Output HTML file name
    """
    # CSS for the ticker animation
    css = """
<style>
@keyframes ticker-kf {
    0% {
        transform: translateX(0);
    }
    100% {
        transform: translateX(-60rem);
    }
}

.img-ticker {
    display: flex;
    margin-left: -1rem;
    margin-right: -1rem;
    animation: ticker-kf 10s linear infinite;
}

.tickerlogo {
    width: 8rem;
    flex: none;
    margin: 0 1rem 0 1rem;
    align-self: flex-start;
    max-width: 100%;
    height: auto;
}
</style>
"""
    
    # Get all SVG files from the directory
    svg_files = []
    for file in Path(images_dir).glob("**/*.svg"):
        relative_path = str(file.relative_to(images_dir))
        svg_files.append(relative_path)
    
    # Generate image tags
    image_tags = []
    for svg_file in svg_files:
        # Create the full URL by joining base_url and file path
        full_url = f"{base_url.rstrip('/')}/{svg_file}"
        # Create the image tag with escaped URL
        image_tag = f'<img class="tickerlogo" src="{html.escape(full_url)}">'
        image_tags.append(image_tag)
    
    # Double the images to ensure smooth infinite scrolling
    image_tags = image_tags * 2
    
    # Generate the complete HTML
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Logo Ticker</title>
    {css}
</head>
<body>
    <!-- Wrap the slider in div with overflow hidden to hide scrollbars -->
    <div style="overflow: hidden; width: 100%;">
        <!-- The slider itself is a flex grid -->
        <div class="img-ticker">
            <!-- Each image is a grid column with width 8rem and horizontal margin 2rem = 10rem -->
            {''.join(image_tags)}
        </div>
    </div>
</body>
</html>
"""
    
    # Write the HTML file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Generated logo ticker HTML file: {output_file}")

if __name__ == "__main__":
    # Example usage
    images_dir = "images"  # Directory containing SVG files
    base_url = "https://raw.githubusercontent.com/dcg-ai/logos/refs/heads/main/images/"
    generate_logo_ticker(images_dir, base_url)