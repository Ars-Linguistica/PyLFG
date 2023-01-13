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
      body: JSON.stringify({ rule: ruleInput.value }),
      headers: { "Content-Type": "application/json" }
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
      body: JSON.stringify({ rule: ruleInput.value }),
      headers: { "Content-Type": "application/json" }
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
      body: JSON.stringify({ rule: ruleInput.value }),
      headers: { "Content-Type": "application/json" }
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
body: JSON.stringify({ entry: lexiconInput.value }),
headers: { "Content-Type": "application/json" }
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
body: JSON.stringify({ entry: lexiconInput.value }),
headers: { "Content-Type": "application/json" }
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
body: JSON.stringify({ entry: lexiconInput.value }),
headers: { "Content-Type": "application/json" }
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
body: JSON.stringify({ sentence: interactivePrompt.value }),
headers: { "Content-Type": "application/json" }
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
body: JSON.stringify({ constraint: constraintInput.value }),
headers: { "Content-Type": "application/json" }
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
body: JSON.stringify({ constraint: constraintInput.value }),
headers: { "Content-Type": "application/json" }
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
body: JSON.stringify({ constraint: constraintInput.value }),
headers: { "Content-Type": "application/json" }
})
.then(response => response.json())
.then(data => {
if (data.success) {
// Update the constraint list
updateConstraintList();
} else {
alert("Error deleting constraint: " + data.error);
}
