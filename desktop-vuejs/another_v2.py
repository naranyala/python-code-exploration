from webui import webui
import os

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

# Path handling - makes it work regardless of where you run the script from
current_dir = os.path.dirname(os.path.abspath(__file__))


# html_file_path = os.path.join(current_dir, 'index.html')
# html_file_path = os.path.join(current_dir, './templates/draggable/index.html')

# html_source = "./templates/draggable/index.html"
# html_source = "./templates/accordion/index.html"
# html_source = "./templates/bottom-sheets/index.html"
# html_source = "./templates/treeview/index.html"
# html_source = "./templates/blog/index.html"
# html_source = "./templates/blog2/index.html"
# html_source = "./templates/blog3/index.html"
# html_source = "./templates/chart-demo-1/index.html"
# html_source = "./templates/chart-demo-2/index.html"
# html_source = "./templates/io-jobportal/index.html"
html_source = "./templates/io-jobportal2/index.html"
# html_source = "./templates/docs-python/index.html"
# html_source = "./templates/todo-app/index.html"
# html_source = "./templates/studio/index.html"
# html_source = "./templates/endless-grid/index.html"
# html_source = "./templates/star-wars-opening/index.html"
# html_source = "./templates/lyrics-editor/index.html"
# html_source = "./templates/lyrics-editor2/index.html"

html_file_path = os.path.join(current_dir, html_source)

my_window = webui.Window()
my_window.show(load_html_file(html_file_path))
webui.wait()
