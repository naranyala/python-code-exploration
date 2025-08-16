from webui import webui
import os
import argparse

def load_html_file(file_path):
    try:
        # Verify the file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"HTML file not found at: {file_path}")

        # Read the file
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    except Exception as e:
        print(f"Error loading HTML file: {e}")
        # Fallback HTML
        return """
        <html>
            <body>
                <h1>Error Loading Page</h1>
                <p>Failed to load the requested HTML file.</p>
            </body>
        </html>
        """

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Display HTML content in a WebUI window.')
    parser.add_argument('--html-path', type=str,
                       help='Full path to the HTML file to display',
                       default=None)

    args = parser.parse_args()

    # Determine which HTML path to use
    if args.html_path:
        html_file_path = args.html_path
    else:
        # Default path if no argument is provided
        current_dir = os.path.dirname(os.path.abspath(__file__))
        html_source = "./templates/dashboard/index.html"
        html_file_path = os.path.join(current_dir, html_source)

    my_window = webui.Window()
    my_window.show(load_html_file(html_file_path))
    webui.wait()

if __name__ == "__main__":
    main()
