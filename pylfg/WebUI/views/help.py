from fastapi import FastAPI, HTMLResponse

app = FastAPI()

@app.get("/help")
def help_view():
    return HTMLResponse("""
    <!DOCTYPE html>
    <html>
        <head>
            <title>PyLFG Help</title>
            <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.0/css/bulma.min.css" integrity="sha512-lCjOjOivb+aJjG8gjGjE2CjCj7VYUoIqHl1/lW6sJGZmWf1s+A5E/9lK2LXKf+PuEjQqcgRpqcjUJ7m/Nb/fAw==" crossorigin="anonymous" />
        </head>
        <body>
            <div class="container has-text-centered">
                <h1 class="title">PyLFG Help</h1>
                <p>This is the help page for PyLFG. Here you can find information on how to use the application and troubleshoot common issues.</p>
                <h2 class="subtitle">Getting Started</h2>
                <p>To get started with PyLFG, navigate to the input page by clicking on the "Input" link in the navigation bar. On the input page, you can enter a sentence to be parsed and select a grammar to use for parsing.</p>
                <h2 class="subtitle">Common Issues</h2>
                <p>If you are experiencing issues with PyLFG, please check the following:</p>
                <ul>
                    <li>Ensure that you have selected a grammar before attempting to parse a sentence</li>
                    <li>Ensure that the sentence you are trying to parse is grammatically correct</li>
                    <li>Ensure that the grammar you are using is compatible with the sentence you are trying to parse</li>
                </ul>
                <h2 class="subtitle">Contact Us</h2>
                <p>If you are still experiencing issues with PyLFG or have any questions or feedback, please contact us at pylfg@example.com.</p>
            </div>
        </body>
    </html>
    """, media_type="text/html")
