import * as d3 from "d3";


document.addEventListener("DOMContentLoaded", function() {
            // Get references to the input fields and buttons
            const interactivePrompt = document.getElementById("interactive-prompt");
            const ruleInput = document.getElementById("rule-input");
            const addRuleButton = document.getElementById("add-rule-button");
            const editRuleButton = document.getElementById("edit-rule-button");
            const deleteRuleButton = document.getElementById("delete-rule-button");
            const lexiconInput = document.getElementById("lexicon-input");
            const addLexiconButton = document.getElementById("add-lexicon-button");
            const editLexiconButton = document.getElementById("edit-lexicon-button");
            const deleteLexiconButton = document.getElementById("delete-lexicon-button");
            const constraintInput = document.getElementById("constraint-input");
            const addConstraintButton = document.getElementById("add-constraint-button");
            const editConstraintButton = document.getElementById("edit-constraint-button");
            const deleteConstraintButton = document.getElementById("delete-constraint-button");

            // Add event listeners to the buttons
            addRuleButton.addEventListener("click", function() {
                // Send an HTTP request to the server to add the rule
                fetch("/add-rule", {
                        method: "POST",
                        body: JSON.stringify({
                            rule: ruleInput.value
                        }),
                        headers: {
                            "Content-Type": "application/json"
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Update the rule list
                            updateRuleList();
                        } else {
                            alert("Error adding rule: " + data.error);
                        }
                    });
            });

            editRuleButton.addEventListener("click", function() {
                // Send an HTTP request to the server to edit the selected rule
                fetch("/edit-rule", {
                        method: "POST",
                        body: JSON.stringify({
                            rule: ruleInput.value
                        }),
                        headers: {
                            "Content-Type": "application/json"
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Update the rule list
                            updateRuleList();
                        } else {
                            alert("Error editing rule: " + data.error);
                        }
                    });
            });

            deleteRuleButton.addEventListener("click", function() {
                // Send an HTTP request to the server to delete the selected rule
                fetch("/delete-rule", {
                        method: "POST",
                        body: JSON.stringify({
                            rule: ruleInput.value
                        }),
                        headers: {
                            "Content-Type": "application/json"
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Update the rule list
                            updateRuleList();
                        } else {
                            alert("Error deleting rule: " + data.error);
                        }
                    });
            });

            addLexiconButton.addEventListener("click", function() {
                // Send an HTTP request to the server to add the lexicon entry
                fetch("/add-lexicon", {
                        method: "POST",
                        body: JSON.stringify({
                            entry: lexiconInput.value
                        }),
                        headers: {
                            "Content-Type": "application/json"
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Update the lexicon list
                            updateLexiconList();
                        } else {
                            alert("Error adding lexicon entry: " + data.error);
                        }
                    });
            });

            editLexiconButton.addEventListener("click", function() {
                // Send an HTTP request to the server to edit the selected lexicon entry
                fetch("/edit-lexicon", {
                        method: "POST",
                        body: JSON.stringify({
                            entry: lexiconInput.value
                        }),
                        headers: {
                            "Content-Type": "application/json"
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Update the lexicon list
                            updateLexiconList();
                        } else {
                            alert("Error editing lexicon entry: " + data.error);
                        }
                    });
            });

            deleteLexiconButton.addEventListener("click", function() {
                // Send an HTTP request to the server to delete the selected lexicon entry
                fetch("/delete-lexicon", {
                        method: "POST",
                        body: JSON.stringify({
                            entry: lexiconInput.value
                        }),
                        headers: {
                            "Content-Type": "application/json"
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Update the lexicon list
                            updateLexiconList();
                        } else {
                            alert("Error deleting lexicon entry: " + data.error);
                        }
                    });
            });

            // Add event listener to the interactive prompt
            interactivePrompt.addEventListener("keydown", function(event) {
                if (event.key === "Enter") {
                    // Send an HTTP request to the server to analyze the sentence
                    fetch("/analyze-sentence", {
                            method: "POST",
                            body: JSON.stringify({
                                sentence: interactivePrompt.value
                            }),
                            headers: {
                                "Content-Type": "application/json"
                            }
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.success) {
                                // Update the parse tree and f/e-structure views
                                updateParseTreeView(data.parse_tree);
                                updateFStructureView(data.f_structure);
                                updateEStructureView(data.e_structure);
                            } else {
                                alert("Error analyzing sentence: " + data.error);
                            }
                        });
                }
            });

            // Add event listeners to the constraint input and buttons
            addConstraintButton.addEventListener("click", function() {
                // Send an HTTP request to the server to add the constraint
                fetch("/add-constraint", {
                        method: "POST",
                        body: JSON.stringify({
                            constraint: constraintInput.value
                        }),
                        headers: {
                            "Content-Type": "application/json"
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Update the constraint list
                            updateConstraintList();
                        } else {
                            alert("Error adding constraint: " + data.error);
                        }
                    });
            });

            editConstraintButton.addEventListener("click", function() {
                // Send an HTTP request to the server to edit the selected constraint
                fetch("/edit-constraint", {
                        method: "POST",
                        body: JSON.stringify({
                            constraint: constraintInput.value
                        }),
                        headers: {
                            "Content-Type": "application/json"
                        }
                    })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            // Update the constraint list
                            updateConstraintList();
                        } else {
                            alert("Error editing constraint: " + data.error);
                        }
                    });
            });

            deleteConstraintButton.addEventListener("click", function() {
                        // Send an HTTP request to the server to delete the selected constraint
                        fetch("/delete-constraint", {
                                method: "POST",
                                body: JSON.stringify({
                                    constraint: constraintInput.value
                                }),
                                headers: {
                                    "Content-Type": "application/json"
                                }
                            })
                            .then(response => response.json())
                            .then(data => {
                                    if (data.success) {
                                        // Update the constraint list
                                        updateConstraintList();
                                    } else {
                                        alert("Error deleting constraint: " + data.error);
                                    }

// Add search input and button to the production rule section
const ruleSearchInput = document.createElement("input");
ruleSearchInput.setAttribute("placeholder", "Search production rules");
production_rule_section.appendChild(ruleSearchInput);
const ruleSearchButton = document.createElement("button");
ruleSearchButton.textContent = "Search";
production_rule_section.appendChild(ruleSearchButton);

// Add search input and button to the lexicon entry section
const lexiconSearchInput = document.createElement("input");
lexiconSearchInput.setAttribute("placeholder", "Search lexicon entries");
lexicon_entry_section.appendChild(lexiconSearchInput);
const lexiconSearchButton = document.createElement("button");
lexiconSearchButton.textContent = "Search";
lexicon_entry_section.appendChild(lexiconSearchButton);

// Add click event listener to the rule search button
ruleSearchButton.addEventListener("click", function() {
    // Send an HTTP request to the server with the search query
    fetch("/search-rules", {
            method: "POST",
            body: JSON.stringify({
                query: ruleSearchInput.value
            }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update the rule list with the search results
                updateRuleList(data.rules);
            } else {
                alert("Error searching for rules: " + data.error);
            }
        });
});

// Add click event listener to the lexicon search button
lexiconSearchButton.addEventListener("click", function() {
    // Send an HTTP request to the server with the search query
    fetch("/search-entries", {
            method: "POST",
            body: JSON.stringify({
                query: lexiconSearchInput.value
            }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update the lexicon list with the search results
                updateLexiconList(data.entries);
            } else {
                alert("Error searching for entries: " + data.error);
            }
        });
});


// Add a section to display the history of inputs and outputs
const historySection = document.createElement("section");
historySection.innerHTML = "<h1>History</h1>";
const historyList = document.createElement("ul");
historySection.appendChild(historyList);
document.body.appendChild(historySection);

// Add a function to update the history section
function updateHistory(input, output) {
    const historyItem = document.createElement("li");
    historyItem.innerHTML = "Input: " + input + "<br>" + "Output: " + output;
    historyList.appendChild(historyItem);
}

// Send a request to the server to log the input and output
interactivePrompt.addEventListener("submit", function(event) {
    event.preventDefault();
    fetch("/log", {
            method: "POST",
            body: JSON.stringify({
                input: interactivePrompt.value
            }),
            headers: {
                "Content-Type": "application/json"
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update the history section with the latest input and output
                updateHistory(interactivePrompt.value, data.output);
            } else {
                alert("Error logging input and output: " + data.error);
            }
        });
});


function createVisualizations() {
    // Use D3.js to create the parse tree and f-structure visualizations
    const parseTreeContainer = d3.select("#parse_tree");
    const fStructureContainer = d3.select("#f_structure");

    const parseTree = d3.tree()
        .size([parseTreeContainer.node().clientWidth, parseTreeContainer.node().clientHeight]);

    const fStructure = d3.tree()
        .size([fStructureContainer.node().clientWidth, fStructureContainer.node().clientHeight]);

    // Get data for parse tree and f-structure from the server
    fetch('/parse-tree-data')
        .then(response => response.json())
        .then(data => {
            const parseTreeRoot = d3.hierarchy(data);
            parseTree(parseTreeRoot);
            parseTreeContainer.selectAll("path")
                .data(parseTreeRoot.links())
                .enter()
                .append("path")
                .attr("d", d3.linkHorizontal()
                    .x(d => d.y)
                    .y(d => d.x));
            parseTreeContainer.selectAll("text")
                .data(parseTreeRoot.descendants())
                .enter()
                .append("text")
                .attr("x", d => d.y)
                .attr("y", d => d.x)
                .text(d => d.data.name);
        });

    fetch('/f-structure-data')
        .then(response => response.json())
        .then(data => {
            const fStructureRoot = d3.hierarchy(data);
            fStructure(fStructureRoot);
            fStructureContainer.selectAll("path")
                .data(fStructureRoot.links())
                .enter()
                .append("path")
                .attr("d", d3.linkHorizontal()
                    .x(d => d.y)
                    .y(d => d.x));
            fStructureContainer.selectAll("text")
                .data(fStructureRoot.descendants())
                .enter()
                .append("text")
                .attr("x", d => d.y)
                .attr("y", d => d.x)
                .text(d => d.data.name);
        });
}

document.addEventListener("DOMContentLoaded", function() {
    createVisualizations();
    // ...rest of the code
});


@app.route('/export', methods=['GET'])
def export():
    data = {'grammar': grammar, 'lexicon': lexicon}
    json_data = json.dumps(data)
    return json_data

