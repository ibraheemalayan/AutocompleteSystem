async function fetchSuggestions(inputField) {
    const currentText = inputField.value;
    const lastChar = currentText.slice(-1);
    const endpoint = (lastChar === ' ') ? "/predict_next_word" : "/complete_word";

    const response = await fetch(endpoint, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ current_text: currentText })
    });

    const data = await response.json();
    updateDropdown(data.options, inputField); // Pass inputField for positioning
}

function updateDropdown(options, inputField) {
    const dropdown = document.getElementById("suggestions");
    dropdown.innerHTML = ''; // Clear previous options

    const rect = inputField.getBoundingClientRect();
    dropdown.style.top = `${rect.bottom + window.scrollY}px`;
    dropdown.style.left = `${rect.left + window.scrollX}px`;

    if (options.length === 0) {
        dropdown.style.display = 'none';
        return;
    }

    if (options.length === 0) {
        dropdown.style.display = 'none';
        return;
    }

    const currentText = inputField.value;
    const words = currentText.split(' ');
    const lastWord = words[words.length - 1]; 
    const endpoint = (lastWord === '') ? "/predict_next_word" : "/complete_word"; // Determine if last character is space
    const isCompletingWord = endpoint === "/complete_word";

    options.forEach(option => {
        const item = document.createElement('div');
        item.classList.add("px-2", "py-1", "cursor-pointer", "hover:bg-gray-100");
        item.textContent = option;
        item.onclick = () => {
            if (isCompletingWord) {
                // Replace the last word (prefix) with the clicked suggestion
                const newText = currentText.slice(0, -lastWord.length) + option + ' ';
                inputField.value = newText;
            } else {
                // Add the clicked suggestion as a new word with space
                inputField.value = currentText.trim() + ' ' + option + ' ';
            }
            dropdown.style.display = 'none';
        };
        dropdown.appendChild(item);
    });

    dropdown.style.display = 'block';
}
