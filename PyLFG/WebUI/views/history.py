from fastapi import FastAPI, HTTPException
from typing import List

app = FastAPI()

@app.get("/history")
async def get_history():
    """
    Retrieve the user's parse history
    """
    # Retrieve the parse history from the database or from a stored variable
    parse_history = [
        {"sentence": "The dog chased the cat", "grammar": "English", "c-structure": True, "f-structure": False, "date": "2022-01-01"},
        {"sentence": "Le chat a poursuivi le chien", "grammar": "French", "c-structure": False, "f-structure": True, "date": "2022-01-02"},
        {"sentence": "Der Hund jagte die Katze", "grammar": "German", "c-structure": True, "f-structure": True, "date": "2022-01-03"},
    ]
    return {
        "parse_history": parse_history
    }

@app.delete("/history/{id}")
async def delete_history(id: int):
    """
    Delete a parse history entry
    """
    try:
        # Delete the specified entry from the database or stored variable
        pass
    except:
        raise HTTPException(status_code=404, detail="Parse history entry not found")

@app.get("/history-view")
def history_view():
    """
    Serve the history view HTML template
    """
    return """
        <div class="container" id="history-container">
            <h1 class="title">Parse History</h1>
            <table class="table" id="history-table">
                <thead>
                    <tr>
                        <th>Sentence</th>
                        <th>Grammar</th>
                        <th>C-Structure</th>
                        <th>F-Structure</th>
                        <th>Date</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody>
                    <tr hx-get="/history" hx-target="#history-table" hx-swap="outerHTML">
                        <td>Loading...</td>
                    </tr>
                </tbody>
            </table>
        </div>
        <script>
            function deleteHistoryEntry(event) {
                event.preventDefault();
                const id = event.target.dataset.id;
                htmx.delete("/history/" + id, {target: "#history-container", replace: "#history-table"});
            }
        </script>
    """
