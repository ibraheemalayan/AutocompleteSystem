var suggested_options_arr = [];
var inputField = document.getElementById("autoTextField");
var currentFocus = -1;

async function fetchSuggestions() {
  const currentText = inputField.value;
  const lastChar = currentText.slice(-1);
  const endpoint = lastChar === " " ? "/predict_next_word" : "/complete_word";

  const response = await fetch(endpoint, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ current_text: currentText }),
  });

  const data = await response.json();
  suggested_options_arr = data.options;
}

// handler for input change
inputField.addEventListener("input", async function (e) {
  console.log("typing", e.target.value);

  let currentText = inputField.value;
  let words = currentText.split(" ");
  let lastWord = words[words.length - 1];
  let isCompletingWord = lastWord !== "";

  if (!currentText) {
    console.log("no text");
    return false;
  }

  console.log("currentText", currentText);
  console.log("lastWord", lastWord);
  console.log("isCompletingWord", isCompletingWord);

  await fetchSuggestions();

  /*close any already open lists of autocompleted values*/
  closeAllLists();
  currentFocus = -1;

  /*create a DIV element that will contain the items (values):*/
  var suggestions_menu = document.createElement("DIV");

  suggestions_menu.setAttribute("id", this.id + "autocomplete-list");
  suggestions_menu.setAttribute(
    "class",
    "autocomplete-items top-full left-0 w-full bg-white border rounded shadow-md"
  );

  /*append the DIV element as a child of the autocomplete container:*/
  this.parentNode.appendChild(suggestions_menu);

  /*for each item in the array...*/
  var i;
  for (i = 0; i < suggested_options_arr.length; i++) {
    let suggestion_div = document.createElement("DIV");
    suggestion_div.setAttribute(
      "class",
      "px-3 py-2 cursor-pointer hover:bg-gray-200"
    );

    /*check if the item starts with the same letters as the text field value:*/
    if (
      suggested_options_arr[i].substr(0, lastWord.length).toUpperCase() ==
      lastWord.toUpperCase()
    ) {
      suggestion_div.innerHTML =
        "<strong>" +
        suggested_options_arr[i].substr(0, lastWord.length) +
        "</strong>";
      suggestion_div.innerHTML += suggested_options_arr[i].substr(
        lastWord.length
      );
    } else {
      suggestion_div.innerHTML = suggested_options_arr[i];
    }

    suggestion_div.innerHTML +=
      "<input type='hidden' value='" + suggested_options_arr[i] + "'>";

    /*execute a function when someone clicks on the item value (DIV element):*/
    suggestion_div.addEventListener("click", function (e) {
      /*insert the value for the autocomplete text field:*/
      let option = this.getElementsByTagName("input")[0].value;

      if (isCompletingWord) {
        const newText = currentText.slice(0, -lastWord.length) + option;
        inputField.value = newText;
      } else {
        inputField.value = currentText.trim() + " " + option;
      }
      /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
      closeAllLists();
      fetchSuggestions();
    });

    suggestions_menu.appendChild(suggestion_div);
  }
});

// handler for keydown event
inputField.addEventListener("keydown", function (e) {
  var x = document.getElementById(this.id + "autocomplete-list");
  if (x) x = x.getElementsByTagName("div");

  if (e.keyCode == 40) {
    // If the arrow DOWN key is pressed
    currentFocus++;
    addActive(x);
  } else if (e.keyCode == 38) {
    //up

    // If the arrow UP key is pressed
    currentFocus--;
    addActive(x);
  } else if (e.keyCode == 13) {
    e.preventDefault();
    if (currentFocus > -1) {
      if (x) x[currentFocus].click();
    }
  }
});

function addActive(x) {
  if (!x) return false;
  removeActive(x);
  if (currentFocus >= x.length) currentFocus = 0;
  if (currentFocus < 0) currentFocus = x.length - 1;
  /*add class "autocomplete-active":*/
  x[currentFocus].classList.add("autocomplete-active");
  x[currentFocus].classList.add("bg-blue-300");
}

function removeActive(x) {
  /*a function to remove the "active" class from all autocomplete items:*/
  for (var i = 0; i < x.length; i++) {
    x[i].classList.remove("autocomplete-active");
    x[i].classList.remove("bg-blue-300");
  }
}

function closeAllLists(elmnt) {
  var x = document.getElementsByClassName("autocomplete-items");
  for (var i = 0; i < x.length; i++) {
    if (elmnt != x[i] && elmnt != inputField) {
      x[i].parentNode.removeChild(x[i]);
    }
  }
}

// close the dropdown when user clicks outside
document.addEventListener("click", function (e) {
  closeAllLists(e.target);
});
