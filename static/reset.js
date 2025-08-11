// reset.js
export function initClearButton() {
  const clearBtn = document.getElementById('clear-input');
  const inputArea = document.getElementById('input-text');
  const outputBox = document.getElementById('output-text');
  const rawBox = document.getElementById('raw-output');
  const outputContainer = document.getElementById('output-text-container');
  const instructionsEl = document.getElementById('instructions');
  const promptOutput = document.getElementById('prompt-output');

  if (!clearBtn || !inputArea) return;

  // Add accessibility attributes
  clearBtn.setAttribute('aria-label', 'Clear input text');

  // Update button state based on input content
  function updateClearButtonState() {
    if (inputArea.value.trim()) {
      clearBtn.disabled = false;
    } else {
      clearBtn.disabled = true;
    }
  }

  // Initialize button state
  updateClearButtonState();

  // Monitor input changes
  inputArea.addEventListener('input', updateClearButtonState);

  clearBtn.addEventListener('click', async () => {
    // 1. Clear user input
    inputArea.value = '';

    // 2. Hide or empty outputs
    if (outputBox) {
      outputBox.textContent = '';
      outputBox.dataset.copy = ''; // Clear the copy data
    }

    if (rawBox) {
      rawBox.style.display = 'none';
      rawBox.textContent = '';
      rawBox._jsonData = null;
    }

    // 3. Clear any error messages (look for error message simple)
    const errorBox = outputContainer?.querySelector('.error-message-simple');
    if (errorBox) {
      errorBox.remove();
    }

    // 4. Reset ancillary UI
    const copyBtn = document.getElementById('copy-output');
    if (copyBtn) {
      copyBtn.disabled = true;
    }

    // 5. Hide prompt output if visible
    if (promptOutput) {
      promptOutput.style.display = 'none';
      promptOutput.textContent = '';
    }

    // 6. Show instructions again
    if (instructionsEl) {
      instructionsEl.style.display = 'block';
    }

    // 7. Flash success animation
    await flashSuccess(clearBtn);

    // 8. Update button state
    updateClearButtonState();

    // 9. Return focus to input for quick re-entry
    inputArea.focus();
  });

  // Export the update function so it can be called externally
  return { updateClearButtonState };
}

// Export a standalone update function that can be called from other modules
export function updateClearButtonState() {
  const clearBtn = document.getElementById('clear-input');
  const inputArea = document.getElementById('input-text');

  if (!clearBtn || !inputArea) return;

  if (inputArea.value.trim()) {
    clearBtn.disabled = false;
  } else {
    clearBtn.disabled = true;
  }
}

// Flash success animation (similar to copy button)
async function flashSuccess(button) {
  button.classList.add('cleared');
  await new Promise((resolve) => setTimeout(resolve, 1500));
  button.classList.remove('cleared');
}
