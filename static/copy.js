/**
 * Copy functionality for RadExtract output
 * Modular, testable, and maintainable
 */

/**
 * Initialize the copy button with event listener
 */
export function initCopyButton() {
  const btn = document.getElementById('copy-output');
  if (!btn) return;

  // Add accessibility attributes
  btn.setAttribute('aria-label', 'Copy findings to clipboard');
  
  btn.addEventListener('click', async () => {
    const text = buildTextToCopy();
    if (!text) return;

    const succeeded = await copyToClipboard(text);
    if (succeeded) flashSuccess(btn);
  });

  // Initialize button state based on output availability
  updateCopyButtonState();
}

/**
 * Build the text to copy based on current mode and output
 * @returns {string} Text to copy, or empty string if nothing to copy
 */
function buildTextToCopy() {
  // ① Raw-JSON mode
  if (document.getElementById('raw-toggle')?.checked) {
    const rawOutput = document.getElementById('raw-output');
    const json = rawOutput?._jsonData;
    return json ? JSON.stringify(json, null, 2) : '';
  }

  // ② Pre-computed plain text (preferred path)
  const outputEl = document.getElementById('output-text');
  if (outputEl?.dataset.copy) {
    return outputEl.dataset.copy;
  }

  // ③ Fallback: parse DOM structure (legacy support)
  return parseDOMStructure(outputEl) || outputEl?.textContent || '';
}

/**
 * Parse DOM structure to extract formatted text (fallback method)
 * @param {HTMLElement} container - Output container element
 * @returns {string} Formatted text
 */
function parseDOMStructure(container) {
  if (!container || !container.children.length) return '';

  const sections = [];

  // Get all section headers and content
  const sectionHeaders = container.querySelectorAll('.section-header');
  sectionHeaders.forEach((header) => {
    sections.push(header.textContent);

    let nextElement = header.nextElementSibling;
    while (nextElement && !nextElement.classList.contains('section-header')) {
      if (nextElement.classList.contains('primary-label')) {
        sections.push('\n' + nextElement.textContent);
      } else if (nextElement.classList.contains('finding-list')) {
        nextElement.querySelectorAll('li').forEach((li) => {
          sections.push('• ' + li.textContent.trim());
        });
      } else if (nextElement.classList.contains('single-finding')) {
        sections.push('- ' + nextElement.textContent.trim());
      } else if (nextElement.textContent.trim()) {
        sections.push(nextElement.textContent.trim());
      }
      nextElement = nextElement.nextElementSibling;
    }
    sections.push(''); // Add blank line after each section
  });

  // Handle prefix content (like examination type)
  const allContent = container.children;
  if (
    allContent.length > 0 &&
    !allContent[0].classList.contains('section-header')
  ) {
    const prefixContent = [];
    for (let i = 0; i < allContent.length; i++) {
      if (allContent[i].classList.contains('section-header')) break;
      if (allContent[i].textContent.trim()) {
        prefixContent.push(allContent[i].textContent.trim());
      }
    }
    if (prefixContent.length > 0) {
      return prefixContent.join('\n') + '\n\n' + sections.join('\n');
    }
  }

  return sections
    .join('\n')
    .replace(/\n{3,}/g, '\n\n')
    .trim();
}

/**
 * Copy text to clipboard with fallback for older browsers
 * @param {string} text - Text to copy
 * @returns {Promise<boolean>} Success status
 */
async function copyToClipboard(text) {
  // Check if clipboard API is available and secure context
  if (navigator.clipboard && window.isSecureContext) {
    try {
      await navigator.clipboard.writeText(text);
      return true;
    } catch (err) {
      console.warn('Clipboard API failed, trying fallback:', err);
      return legacyCopy(text);
    }
  } else {
    // Use fallback for older browsers or insecure contexts
    return legacyCopy(text);
  }
}

/**
 * Legacy clipboard copy using execCommand
 * @param {string} text - Text to copy
 * @returns {boolean} Success status
 */
function legacyCopy(text) {
  const ta = Object.assign(document.createElement('textarea'), {
    value: text,
    style: 'position:fixed;left:-9999px',
  });
  document.body.appendChild(ta);
  ta.select();

  let ok = false;
  try {
    ok = document.execCommand('copy');
  } catch (err) {
    console.error('Legacy copy failed:', err);
  }

  document.body.removeChild(ta);
  return ok;
}

/**
 * Show success feedback on button
 * @param {HTMLElement} button - Copy button element
 */
function flashSuccess(button) {
  button.classList.add('copied');
  button.setAttribute('title', 'Copied!');

  setTimeout(() => {
    button.classList.remove('copied');
    button.setAttribute('title', 'Copy output to clipboard');
  }, 2000);
}

/**
 * Update copy button enabled/disabled state based on output availability
 */
export function updateCopyButtonState() {
  const btn = document.getElementById('copy-output');
  if (!btn) return;

  const outputText = document.getElementById('output-text');
  const hasOutput = outputText && outputText.textContent.trim().length > 0;

  btn.disabled = !hasOutput;
}
