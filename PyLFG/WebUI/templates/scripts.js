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
                // Check if the app is running locally or online
                if (window.location.hostname === "localhost") {
                    // Send an HTTP request to the local server to add the rule
                    fetch("http://localhost:5000/add-rule", {
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
                } else {
                    // Send an HTTP request to the online server to add the rule
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
                }
            });

            editRuleButton.addEventListener("click", function() {
                // Check if the app is running locally or online
                if (window.location.hostname === "localhost") {
                    // Send an HTTP request to the local server to edit the selected rule
                    fetch("http://localhost:5000/edit-rule", {
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
                } else {
                    // Send an HTTP request to the online server to edit the selected rule
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
                }
            });

            deleteRuleButton.addEventListener("click", function() {
                // Check if the app is running locally or online
                if (window.location.hostname === "localhost") {
                    // Send an HTTP request to the local server to delete the selected rule
                    fetch("http://localhost:5000/delete-rule", {
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
                } else {
                    // Send an HTTP request to the online server to delete the selected rule
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
                                alert("Error deleting rule: "
                                    data.error);
                            }
                        });
                }
            });