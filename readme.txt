# Circle System Templates Scraper Scripts

## scrape_circle_automation_templates.py
- Scrapes the main Automation Templates listing page on community.theaiautomators.com.
- Extracts all post titles and URLs, saving them to automation_templates_links.json.
- Uses Circle cookies for authentication.

## extract_context_engineering_strategies_in_n8n.py
- Downloads all text, images, downloadable files, and YouTube videos from the "Context Engineering Strategies in n8n" page.
- Saves content into a subfolder under System Templates named Context_Engineering_Strategies_in_n8n.
- Outputs a markdown file Context_Engineering_Strategies_in_n8n.md with all page content, local image links, and file links.
- Downloads any YouTube video(s) in the content to Context_Engineering_Strategies_in_n8n.mp4.
- Downloads any downloadable files (e.g., JSON blueprints) and links them in the markdown.
- Uses Circle cookies for authentication.

## Prerequisites
- Python 3.x
- selenium, webdriver-manager, beautifulsoup4, requests, markdownify, yt-dlp
- Chrome browser installed
- A valid Circle cookies file

## Usage
Run each script from the Circle directory. See each script's comments for configuration and output details.
