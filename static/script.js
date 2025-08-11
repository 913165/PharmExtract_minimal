/**
 * @fileoverview Interactive radiology report structuring demo interface.
 *
 * This script provides the frontend functionality for the radiology report
 * structuring application, including sample report loading, API communication,
 * and interactive hover-to-highlight functionality between structured output
 * and original input text.
 */

// Import copy functionality
import { initCopyButton, updateCopyButtonState } from './copy.js';
// Import clear functionality
import { initClearButton, updateClearButtonState } from './reset.js';

document.addEventListener('DOMContentLoaded', function () {
  // === CONFIGURATION CONSTANTS ===
  const GRID_CONFIG = {
    MOBILE_MIN_WIDTH: 120,
    DESKTOP_MIN_WIDTH: 160,
    MOBILE_BREAKPOINT: 768,
    NARROW_BREAKPOINT: 360,
    MAX_LABEL_LENGTH: 60,
    BALANCE_DELAY: 100,
    RESIZE_DEBOUNCE: 250,
  };

  const UI_CONFIG = {
    SCROLL_SMOOTH_BEHAVIOR: 'smooth',
    SCROLL_OFFSET_BUFFER: 100,
  };

  // === GLOBAL STATE ===
  // Variables are declared where they're first used to avoid redeclaration errors

  // === UTILITY FUNCTIONS ===

  /**
   * Checks if the device is a touch-only device (no hover capability).
   * Uses CSS media queries to accurately detect hover capability rather than just touch presence.
   * @returns {boolean} True if it's a touch-only device, false if it can hover
   */
  const isTouchDevice = () =>
    !window.matchMedia('(hover: hover) and (pointer: fine)').matches;

  /**
   * Clears all highlights from text spans.
   */
  function clearAllHighlights() {
    const spans = document.querySelectorAll('.text-span.highlight');
    spans.forEach((span) => {
      span.classList.remove('highlight');
      span.dataset.highlighted = 'false';
    });
    clearInputHighlight();
  }

  // Add global click handler to clear highlights when clicking outside on mobile
  document.addEventListener('click', function (e) {
    if (isTouchDevice() && !e.target.classList.contains('text-span')) {
      clearAllHighlights();
    }
  });

  const predictButton = document.getElementById('predict-button');
  const inputText = document.getElementById('input-text');
  const outputTextContainer = document.getElementById('output-text');
  const instructionsEl = document.querySelector('.instructions');
  const loadingOverlay = document.getElementById('loading-overlay');
  let processingLoadingTimer = null;
  let originalInputText = '';

  // Disable virtual keyboard on mobile devices
  let allowInputFocus = false;

  if (isTouchDevice()) {
    // Prevent focus to avoid virtual keyboard, except during programmatic highlighting
    inputText.addEventListener('focus', function (e) {
      if (!allowInputFocus) {
        e.target.blur();
      }
    });
  }

  let sampleReportsData = null;
  let currentSampleId = null;

  // Model dropdown elements
  const modelSelect = document.getElementById('model-select');
  const modelNameSpan = document.getElementById('model-name');
  const modelLink = document.getElementById('model-link');

  /**
   * Mapping of model IDs to their display information.
   * @const {Object<string, {text: string, link: string}>}
   */
  const modelInfo = {
    'gemini-2.5-flash': {
      text: 'Gemini 2.5 Flash',
      link: 'https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-5-flash',
    },
    'gemini-2.5-pro': {
      text: 'Gemini 2.5 Pro',
      link: 'https://cloud.google.com/vertex-ai/generative-ai/docs/models/gemini/2-5-pro',
    },
  };

  /**
   * Updates the model information display based on the selected model.
   */
  function updateModelInfo() {
    const selectedModel = modelSelect.value;
    if (modelNameSpan)
      modelNameSpan.textContent = modelInfo[selectedModel].text;
    if (modelLink) modelLink.href = modelInfo[selectedModel].link;
  }

  if (modelSelect) {
    modelSelect.addEventListener('change', updateModelInfo);
    updateModelInfo();
  }

  // Cache optimization elements
  const cacheToggle = document.getElementById('cache-toggle');

  // LX Toggle elements
  const promptToggle = document.getElementById('prompt-toggle');
  const rawToggle = document.getElementById('raw-toggle');

  // Initialize copy functionality
  initCopyButton();

  // Initialize clear functionality
  initClearButton();

  /**
   * Detect mobile devices and update placeholder text
   * Mobile UX does not have text entry to avoid disrupting the user interaction
   * with extractions in the output - users can only select from samples
   */
  function updatePlaceholderForMobile() {
    const isMobile =
      /iPhone|iPad|iPod|Android/i.test(navigator.userAgent) ||
      (navigator.maxTouchPoints && navigator.maxTouchPoints > 0);

    if (isMobile) {
      inputText.placeholder = 'Please select a sample from above...';
    }
  }

  updatePlaceholderForMobile();

  /**
   * Updates model dropdown state based on cache toggle.
   * When cache is enabled, model dropdown is disabled since cache is model-specific.
   */
  function updateModelDropdownState() {
    if (modelSelect && cacheToggle) {
      modelSelect.disabled = cacheToggle.checked;
      // Add visual indication
      if (cacheToggle.checked) {
        modelSelect.style.opacity = '0.6';
        modelSelect.style.cursor = 'not-allowed';
      } else {
        modelSelect.style.opacity = '1';
        modelSelect.style.cursor = 'pointer';
      }
    }
  }

  /**
   * Handles cache toggle changes.
   */
  if (cacheToggle) {
    cacheToggle.addEventListener('change', updateModelDropdownState);
    updateModelDropdownState();
  }

  /**
   * Updates LX toggles state based on content availability.
   * Disables toggles when input is empty or no output is generated.
   */
  function updateLXToggleStates() {
    const hasInput = inputText && inputText.value.trim().length > 0;
    const hasOutput =
      outputTextContainer && outputTextContainer.textContent.trim().length > 0;

    if (promptToggle) {
      promptToggle.disabled = !hasInput;
      if (!hasInput) {
        promptToggle.checked = false;
        promptToggle.style.opacity = '0.5';
        promptToggle.style.cursor = 'not-allowed';
      } else {
        promptToggle.style.opacity = '1';
        promptToggle.style.cursor = 'pointer';
      }

      // Synchronize mobile toggle state
      const mobilePromptToggle = document.getElementById(
        'prompt-toggle-mobile',
      );
      if (mobilePromptToggle) {
        mobilePromptToggle.disabled = !hasInput;
        mobilePromptToggle.checked = promptToggle.checked;
        mobilePromptToggle.style.opacity = promptToggle.style.opacity;
        mobilePromptToggle.style.cursor = promptToggle.style.cursor;
      }
    }

    if (rawToggle) {
      rawToggle.disabled = !hasOutput;
      if (!hasOutput) {
        rawToggle.checked = false;
        rawToggle.style.opacity = '0.5';
        rawToggle.style.cursor = 'not-allowed';
      } else {
        rawToggle.style.opacity = '1';
        rawToggle.style.cursor = 'pointer';
      }

      // Synchronize mobile toggle state
      const mobileRawToggle = document.getElementById('raw-toggle-mobile');
      if (mobileRawToggle) {
        mobileRawToggle.disabled = !hasOutput;
        mobileRawToggle.checked = rawToggle.checked;
        mobileRawToggle.style.opacity = rawToggle.style.opacity;
        mobileRawToggle.style.cursor = rawToggle.style.cursor;
      }
    }
  }

  updateLXToggleStates();
  updateCopyButtonState();

  /**
   * Loads sample reports from the static JSON file.
   * @returns {Promise<void>}
   */
  async function loadSampleReports() {
    try {
      const response = await fetch('/static/sample_reports.json');
      const data = await response.json();
      sampleReportsData = data;
      initializeSampleButtons();
    } catch (error) {
      console.error('Failed to load sample reports:', error);
    }
  }

  /**
   * Initializes the sample report buttons in the UI.
   */
  function initializeSampleButtons() {
    if (!sampleReportsData || !sampleReportsData.samples) return;

    const sampleButtonsContainer = document.querySelector('.sample-buttons');
    if (!sampleButtonsContainer) return;

    sampleButtonsContainer.innerHTML = '';

    const sortedSamples = [...sampleReportsData.samples].sort((a, b) =>
      a.title.localeCompare(b.title),
    );

    sortedSamples.forEach((sample) => {
      const button = document.createElement('button');
      button.className = 'sample-button';
      button.setAttribute('data-sample-id', sample.id);

      // Use 'type' for pharmaceutical, fallback to 'modality' or blank
      const metaLabel = sample.type || sample.modality || '';

      button.innerHTML = `
                <div class="sample-button-content">
                    <div class="sample-title">${sample.title}</div>
                    <div class="sample-meta">
                        <span class="sample-modality">${metaLabel}</span>
                    </div>
                </div>
            `;

      const modalitySpan = button.querySelector('.sample-modality');
      if (modalitySpan && metaLabel) {
        modalitySpan.classList.add(`mod-${metaLabel.toLowerCase().replace(/\s+/g, '-')}`);
      }

      button.addEventListener('click', function () {
        loadSampleReport(sample);
        document
          .querySelectorAll('.sample-button.active')
          .forEach((btn) => btn.classList.remove('active'));
        this.classList.add('active');
      });

      sampleButtonsContainer.appendChild(button);
    });

    setTimeout(() => {
      balanceByColumnCount();
    }, GRID_CONFIG.BALANCE_DELAY);
  }

  /**
   * Balances sample button rows by calculating optimal column count for even distribution.
   * Keeps row-wise reading order while achieving visual balance (e.g., 5+5 instead of 6+4).
   * Uses responsive sizing for better mobile experience.
   */
  function balanceByColumnCount() {
    const container = document.querySelector('.sample-buttons');
    if (!container) {
      console.warn('Sample buttons container not found');
      return;
    }

    const cards = container.querySelectorAll('.sample-button').length;
    const styles = getComputedStyle(container);
    const gap = parseFloat(styles.columnGap) || 12;

    const viewport = window.innerWidth;
    const minWidth =
      viewport <= GRID_CONFIG.MOBILE_BREAKPOINT
        ? GRID_CONFIG.MOBILE_MIN_WIDTH
        : GRID_CONFIG.DESKTOP_MIN_WIDTH;

    const containerWidth = container.clientWidth;
    const columnsFit = Math.max(
      1,
      Math.floor((containerWidth + gap) / (minWidth + gap)),
    );

    if (viewport <= GRID_CONFIG.NARROW_BREAKPOINT) {
      return;
    }

    // Find the column count that provides the most even distribution
    let bestCols = columnsFit;
    let bestRem = cards % columnsFit;

    for (let cols = columnsFit - 1; cols >= 1; cols--) {
      const rem = cards % cols;
      if (rem === 0) {
        bestCols = cols;
        break; // Perfect distribution found
      }
      if (rem > bestRem) continue; // Worse distribution, skip
      bestCols = cols;
      bestRem = rem;
    }

    // Mobile-specific logic: prefer 2-3 columns for better touch targets
    if (viewport <= GRID_CONFIG.MOBILE_BREAKPOINT) {
      if (bestCols === 1 && columnsFit >= 2) {
        bestCols = 2; // Force at least 2 columns on mobile
      } else if (bestCols > 3 && cards >= 6) {
        // If we have many columns, prefer 2-3 for mobile UX
        const cols2Rem = cards % 2;
        const cols3Rem = cards % 3;
        if (cols2Rem <= cols3Rem) {
          bestCols = 2;
        } else {
          bestCols = 3;
        }
      }
    }

    // Always apply the balanced column count for optimal visual distribution
    container.style.gridTemplateColumns = `repeat(${bestCols}, minmax(${minWidth}px, 1fr))`;
  }

  /**
   * Loads a sample report into the input area and automatically processes it.
   * @param {Object} sample - The sample report data object
   */
  function loadSampleReport(sample) {
    scrollToOutput();

    // Normalize line endings for sample text
    inputText.value = sample.text.replace(/\r\n?/g, '\n');

    // Update clear button state after loading sample
    updateClearButtonState();

    outputTextContainer.innerHTML = '';
    instructionsEl.style.display = 'block';
    currentSampleId = sample.id;

    // Automatically enable cache for sample reports
    if (cacheToggle) {
      cacheToggle.checked = true;
      // Trigger the change event to update model dropdown state
      updateModelDropdownState();
    }

    setTimeout(() => {
      predictButton.click();
    }, 100);
  }

  loadSampleReports();

  let resizeTimeout;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
      balanceByColumnCount();
    }, GRID_CONFIG.RESIZE_DEBOUNCE);
  });

  /**
   * Updates the cache status display in the UI.
   * @returns {Promise<void>}
   */
  async function updateCacheStatus() {
    try {
      const response = await fetch('/cache/stats');
      const stats = await response.json();
      const statusEl = document.getElementById('cache-status');
      if (statusEl && stats.total_entries > 0) {
        statusEl.textContent = `(${stats.sample_entries} samples cached)`;
      } else if (statusEl) {
        statusEl.textContent = '';
      }
    } catch (e) {
      console.log('Cache stats not available');
    }
  }

  updateCacheStatus();

  inputText.addEventListener('input', function () {
    if (
      currentSampleId &&
      inputText.value !==
        sampleReportsData?.samples?.find((s) => s.id === currentSampleId)?.text
    ) {
      currentSampleId = null;
      document
        .querySelectorAll('.sample-button.active')
        .forEach((btn) => btn.classList.remove('active'));
    }

    // Uncheck cache when input text is modified (cache no longer applies)
    if (cacheToggle && cacheToggle.checked) {
      cacheToggle.checked = false;
      updateModelDropdownState(); // Re-enable model dropdown
      updateCacheStatus(); // Update cache status display
    }

    // Update LX toggle states based on input content
    updateLXToggleStates();
    updateCopyButtonState();
  });

  predictButton.addEventListener('click', async function () {
    predictButton.disabled = true;
    predictButton.textContent = 'Processing...';
    const cacheEnabled = cacheToggle ? cacheToggle.checked : true;

    if (processingLoadingTimer) clearTimeout(processingLoadingTimer);
    // Show loading overlay after 200ms
    processingLoadingTimer = setTimeout(() => {
      if (loadingOverlay) {
        loadingOverlay.style.display = 'flex';
        const loaderMessage = document.querySelector('.loader-message');

        if (loaderMessage) {
          const modelText =
            (modelSelect && modelInfo[modelSelect.value]?.text) ||
            'Gemini 2.5 Flash';
          loaderMessage.textContent = `Running LangExtract with ${modelText}...`;
        }

        if (typeof gsap !== 'undefined') {
          startLoaderAnimation();
        }
      }
    }, 200);
    inputText.value = inputText.value.replace(/\r\n?/g, '\n');

    originalInputText = inputText.value;
    outputTextContainer.innerHTML = '';
    updateLXToggleStates(); // Disable toggles when output is cleared
    updateCopyButtonState();

    try {
      const useCache = cacheEnabled;

      const headers = { 'Content-Type': 'text/plain' };
      if (modelSelect) {
        headers['X-Model-ID'] = modelSelect.value;
      }
      if (useCache) {
        headers['X-Use-Cache'] = 'true';
        if (currentSampleId) {
          headers['X-Sample-ID'] = currentSampleId;
        }
      } else {
        headers['X-Use-Cache'] = 'false';
      }

      const response = await fetch('/predict', {
        method: 'POST',
        headers: headers,
        body: originalInputText,
      });

      if (!response.ok) {
        const errorText = await response.text();
        let errorJson;
        try {
          errorJson = JSON.parse(errorText);
        } catch (parseError) {
          throw new Error(errorText || 'unknown error');
        }

        const error = new Error(errorJson.error || 'unknown error');
        error.details = errorJson;
        throw error;
      }

      // Stop the initial overlay timer so it doesn't overwrite cache message
      if (processingLoadingTimer) {
        clearTimeout(processingLoadingTimer);
        processingLoadingTimer = null;
      }

      const data = await response.json();

      // Handle cached results with simulated loading
      if (data.from_cache) {
        // Ensure overlay is visible (may not be if response was quick)
        if (loadingOverlay && loadingOverlay.style.display === 'none') {
          loadingOverlay.style.display = 'flex';
          if (typeof gsap !== 'undefined') {
            startLoaderAnimation();
          }
        }

        // Update loading message for cached results
        const loaderMessage = document.querySelector('.loader-message');
        if (loaderMessage) {
          loaderMessage.textContent =
            'Loading LangExtract Result from Cache...';
        }

        // Add 1-2 second delay for cached results to simulate loading
        const delay = Math.random() * 1000 + 2000; // 2-3 seconds
        await new Promise((resolve) => setTimeout(resolve, delay));
      }

      if (data.sanitized_input && data.sanitized_input !== originalInputText) {
        const inputText = document.getElementById('input-text');
        if (inputText) {
          inputText.value = data.sanitized_input;
          updateClearButtonState();
        }
      }

      if (data.text) {
        if (
          data.segments &&
          Array.isArray(data.segments) &&
          data.segments.length > 0
        ) {
          renderSegments(data.segments);
          updateLXToggleStates(); // Enable/update toggles when output is generated
          updateCopyButtonState();

          // Update raw / prompt panes
          const rawOutput = document.getElementById('raw-output');
          const promptOutput = document.getElementById('prompt-output');

          if (rawToggle && rawOutput) {
            const rawData = data.annotated_document_json || {
              error: 'No annotated document data available',
              available_data: data,
            };

            rawOutput.innerHTML = '';

            const formatter = new JSONFormatter(rawData, {
              hoverPreviewEnabled: true,
              animateOpen: false,
              animateClose: false,
              theme: 'light',
              open: true,
            });

            const renderedElement = formatter.render();
            rawOutput.appendChild(renderedElement);
            rawOutput._jsonFormatter = formatter;
            rawOutput._jsonData = rawData;

            setTimeout(() => {
              try {
                if (formatter.openAtDepth) {
                  formatter.openAtDepth(3);
                }
              } catch (e) {
                // Ignore errors if formatter doesn't support openAtDepth
              }

              const togglers = rawOutput.querySelectorAll(
                '.json-formatter-toggler',
              );
              togglers.forEach((toggler) => {
                try {
                  toggler.click();
                } catch (e) {
                  // Ignore click errors on JSON formatter togglers
                }
              });
            }, 10);

            rawToggle.checked = false;
            rawOutput.style.display = 'none';
            outputTextContainer.style.display = 'block';
          }

          if (promptOutput) {
            const promptText = data.raw_prompt || 'Prompt data not available.';
            if (typeof marked !== 'undefined' && data.raw_prompt) {
              // Render markdown with syntax highlighting support
              promptOutput.innerHTML = marked.parse(promptText);
            } else {
              // Fallback to plain text
              promptOutput.textContent = promptText;
            }
            promptToggle.checked = false;
            showPromptView(false);
          }

          const hasIntervals = data.segments.some(
            (segment) => segment.intervals && segment.intervals.length > 0,
          );

          instructionsEl.style.display = 'block';
          if (!hasIntervals) {
            instructionsEl.innerHTML =
              '<p><strong>Note:</strong> Hover functionality is not available for this result.</p>';
          }
        } else {
          outputTextContainer.textContent = data.text;
          instructionsEl.style.display = 'none';
        }
      } else {
        outputTextContainer.textContent = 'No content returned from server.';
        instructionsEl.style.display = 'none';
      }
    } catch (error) {
      if (error.details && typeof error.details === 'object') {
        if (error.details.error === 'Empty input') {
          const friendlyMessage = [
            '<div class="error-message-simple" role="alert">',
            '    <h3>📝 Input Required</h3>',
            '    <p>Please paste or type a radiology report in the input area.</p>',
            '    <p class="suggestion">You can try one of the sample reports below to see how the structuring works.</p>',
            '</div>',
          ].join('\n');
          outputTextContainer.innerHTML = friendlyMessage;
        } else if (
          error.details.error === 'Input too long' &&
          error.details.max_length
        ) {
          const friendlyMessage = [
            '<div class="error-message-simple" role="alert">',
            '    <h3>⚠️ Input Too Long</h3>',
            `    <p>Your input contains <strong>${originalInputText.length.toLocaleString()}</strong> characters, `,
            `    but this demo is limited to <strong>${error.details.max_length.toLocaleString()}</strong> characters `,
            "    to reduce the load on this demo's Gemini API key.</p>",
            '    <p class="suggestion">Try using a shorter excerpt from your report, or focus on the most relevant sections.</p>',
            '    <div class="deploy-note">',
            '        <strong>💡 Tip:</strong> If you deploy the source code with your own Gemini API key, you can modify this limit.',
            '    </div>',
            '</div>',
          ].join('\n');
          outputTextContainer.innerHTML = friendlyMessage;
        } else {
          let errorMessage = `Error: ${error.details.error}\n\n`;
          errorMessage += `${error.details.message}`;

          if (error.details.max_length) {
            errorMessage += `\n\nMaximum allowed length: ${error.details.max_length} characters`;
          }

          outputTextContainer.textContent = errorMessage;
        }
      } else {
        outputTextContainer.textContent = `Error: ${error.message}`;
      }
      instructionsEl.style.display = 'none';
    } finally {
      if (processingLoadingTimer) {
        clearTimeout(processingLoadingTimer);
        processingLoadingTimer = null;
      }
      if (loadingOverlay) loadingOverlay.style.display = 'none';

      const message = document.querySelector('.loader-message');
      const spinner = document.querySelector('.spinner');
      if (message && spinner) {
        gsap.killTweensOf([message, spinner]);
        gsap.set([message, spinner], { clearProps: 'all' });
      }
      predictButton.disabled = false;
      predictButton.textContent = 'Process';

      updateCacheStatus();
    }
  });

  /**
   * Renders segments as interactive elements in the output container.
   * @param {Array<Object>} segments - Array of segment objects from the API response
   */
  function renderSegments(segments) {
    outputTextContainer.innerHTML = '';
    const plainTextParts = []; // Collect plain text for data-copy

    const segmentsByType = {
      prefix: segments.filter((seg) => seg.type === 'prefix'),
      body: segments.filter((seg) => seg.type === 'body'),
      suffix: segments.filter((seg) => seg.type === 'suffix'),
    };

    if (segmentsByType.prefix.length > 0) {
      // Check if there's an Examination segment that should get a header
      const examinationSegments = segmentsByType.prefix.filter(
        (seg) => seg.label && seg.label.toLowerCase() === 'examination',
      );
      const otherPrefixSegments = segmentsByType.prefix.filter(
        (seg) => !seg.label || seg.label.toLowerCase() !== 'examination',
      );

      // Render Examination segments with content as header (no "EXAMINATION:" prefix)
      if (examinationSegments.length > 0) {
        examinationSegments.forEach((segment) => {
          let content = segment.content;
          // Remove various examination prefixes
          const examPrefixes = ['EXAMINATION:', 'EXAM:', 'STUDY:'];
          const upperContent = content.toUpperCase();

          for (const prefix of examPrefixes) {
            if (upperContent.startsWith(prefix)) {
              content = content.substring(prefix.length).trim();
              break;
            }
          }

          // Use the clean content as the header text (capitalized)
          if (content) {
            appendSectionHeader(content.toUpperCase());
            plainTextParts.push(content.toUpperCase());
          }
        });
        outputTextContainer.appendChild(document.createElement('br'));
      }

      // Render other prefix segments normally
      if (otherPrefixSegments.length > 0) {
        otherPrefixSegments.forEach((segment) => {
          outputTextContainer.appendChild(createSegmentElement(segment));
          plainTextParts.push(segment.content);
        });
        outputTextContainer.appendChild(document.createElement('br'));
      }
    }

    if (segmentsByType.body.length > 0) {
      appendSectionHeader('FINDINGS:');
      plainTextParts.push('\nFINDINGS:');

      const groupMap = new Map();
      segmentsByType.body.forEach((seg) => {
        const rawLabel = seg.label || 'Other';
        const parts = rawLabel.split(':');
        const primary = parts[0].trim();
        const sub = parts.slice(1).join(':').trim();
        if (!groupMap.has(primary)) groupMap.set(primary, []);
        groupMap.get(primary).push({ segment: seg, sublabel: sub });
      });

      groupMap.forEach((items, primary) => {
        const primaryHeader = document.createElement('div');
        primaryHeader.className = 'primary-label';
        primaryHeader.textContent = primary;
        outputTextContainer.appendChild(primaryHeader);
        plainTextParts.push('\n' + primary);

        if (items.length === 1) {
          const p = document.createElement('p');
          p.className = 'single-finding';
          const labelSpan = document.createElement('span');
          labelSpan.classList.add('segment-sublabel');
          if (items[0].sublabel) {
            labelSpan.textContent = `${items[0].sublabel}: `;
            p.appendChild(labelSpan);
          }
          p.appendChild(createContentWithIntervalSpans(items[0].segment));
          outputTextContainer.appendChild(p);
          plainTextParts.push('- ' + p.textContent.trim());
        } else {
          const ul = document.createElement('ul');
          ul.className = 'finding-list';
          outputTextContainer.appendChild(ul);

          items.forEach((item) => {
            const li = document.createElement('li');
            const labelSpan = document.createElement('span');
            labelSpan.classList.add('segment-sublabel');
            if (item.sublabel) {
              labelSpan.textContent = `${item.sublabel}: `;
              li.appendChild(labelSpan);
            }
            li.appendChild(createContentWithIntervalSpans(item.segment));
            ul.appendChild(li);
            plainTextParts.push('• ' + li.textContent.trim());
          });
        }
      });
    }

    if (segmentsByType.suffix.length > 0) {
      appendSectionHeader('IMPRESSION:');
      plainTextParts.push('\nIMPRESSION:');

      segmentsByType.suffix.forEach((segment) => {
        outputTextContainer.appendChild(createSegmentElement(segment));
        plainTextParts.push(segment.content);
      });
    }

    // Store pre-computed plain text for efficient copying
    const plainText = plainTextParts
      .join('\n')
      .replace(/\n{3,}/g, '\n\n')
      .trim();
    const outputEl = document.getElementById('output-text');
    if (outputEl) {
      outputEl.dataset.copy = plainText;
    }
  }

  /**
   * Helper function to create section headers.
   * @param {string} text - The header text to display
   */
  function appendSectionHeader(text) {
    const header = document.createElement('div');
    header.className = 'section-header';
    header.textContent = text;
    outputTextContainer.appendChild(header);
  }

  /**
   * Creates a DOM element for a segment.
   * @param {Object} segment - The segment data object
   * @returns {HTMLElement} The created segment element
   */
  function createSegmentElement(segment) {
    const segmentDiv = document.createElement('div');
    segmentDiv.classList.add('segment', `segment-${segment.type}`);

    if (segment.type === 'body' && segment.label) {
      const labelSpan = document.createElement('span');
      labelSpan.classList.add('segment-label');
      labelSpan.textContent = `${segment.label}: `;
      segmentDiv.appendChild(labelSpan);
    }

    segmentDiv.appendChild(createContentWithIntervalSpans(segment));
    return segmentDiv;
  }

  /**
   * Creates content with interval spans for highlighting functionality.
   * @param {Object} segment - The content segment with intervals and metadata
   * @returns {DocumentFragment} Fragment containing the processed content
   */
  function createContentWithIntervalSpans(segment) {
    const fragment = document.createDocumentFragment();

    if (segment.intervals && segment.intervals.length > 0) {
      const contentSpan = createIntervalSpan(segment);
      addIntervalEventListeners(contentSpan);
      fragment.appendChild(contentSpan);
    } else {
      fragment.appendChild(createRegularSpan(segment));
    }

    return fragment;
  }

  /**
   * Creates a span element for content with intervals (highlighting capability).
   * @param {Object} segment - The content segment
   * @returns {HTMLSpanElement} The created span element
   */
  function createIntervalSpan(segment) {
    const interval = segment.intervals[0];
    const contentSpan = document.createElement('span');
    contentSpan.classList.add('text-span');

    // Set data attributes for position tracking
    contentSpan.dataset.startPos = interval.startPos;
    contentSpan.dataset.endPos = interval.endPos;
    contentSpan.dataset.type = segment.type;
    contentSpan.dataset.label = segment.label || '';

    // Handle label styling if present
    const labelInfo = extractLabelInfo(segment.content);
    if (labelInfo.hasLabel) {
      setupLabelSpan(contentSpan, labelInfo);
    } else {
      contentSpan.textContent = segment.content;
    }

    // Apply significance-based styling
    applySignificanceStyles(contentSpan, segment.significance);

    return contentSpan;
  }

  /**
   * Extracts label information from content.
   * @param {string} content - The content to analyze
   * @returns {Object} Label information object
   */
  function extractLabelInfo(content) {
    const colonIndex = content.indexOf(':');
    const hasLabel =
      colonIndex > 0 && colonIndex < GRID_CONFIG.MAX_LABEL_LENGTH;

    return {
      hasLabel,
      labelText: hasLabel ? content.slice(0, colonIndex) : '',
      restText: hasLabel ? content.slice(colonIndex) : content,
    };
  }

  /**
   * Sets up span with label and content parts for CSS styling.
   * @param {HTMLSpanElement} contentSpan - The span to configure
   * @param {Object} labelInfo - Label information object
   */
  function setupLabelSpan(contentSpan, labelInfo) {
    contentSpan.classList.add('has-label');

    const labelSpan = document.createElement('span');
    labelSpan.className = 'label-part';
    labelSpan.textContent = labelInfo.labelText;

    const contentPartSpan = document.createElement('span');
    contentPartSpan.className = 'content-part';
    contentPartSpan.textContent = labelInfo.restText;

    contentSpan.appendChild(labelSpan);
    contentSpan.appendChild(contentPartSpan);
  }

  /**
   * Applies significance-based CSS classes to content spans.
   * @param {HTMLSpanElement} span - The span to style
   * @param {string} significance - The significance level
   */
  function applySignificanceStyles(span, significance) {
    if (significance) {
      const significanceLevel = (significance || '').toLowerCase();
      if (
        significanceLevel === 'minor' ||
        significanceLevel === 'significant'
      ) {
        span.classList.add(`significance-${significanceLevel}`);
      }
    }
  }

  /**
   * Creates a regular span for content without intervals.
   * @param {Object} segment - The content segment
   * @returns {HTMLSpanElement} The created span element
   */
  function createRegularSpan(segment) {
    const regularSpan = document.createElement('span');
    regularSpan.textContent = segment.content;

    // Apply significance styling even for non-interval content
    applySignificanceStyles(regularSpan, segment.significance);

    return regularSpan;
  }

  /**
   * Adds event listeners for interval spans with distinct desktop/mobile interaction patterns.
   * Desktop: Hover to highlight/unhighlight instantly
   * Mobile: Tap to toggle highlight on/off
   * @param {HTMLSpanElement} contentSpan - The span to add listeners to
   */
  function addIntervalEventListeners(contentSpan) {
    const isDesktop = !isTouchDevice();

    if (isDesktop) {
      // Desktop: Hover-based highlighting
      contentSpan.addEventListener('mouseenter', function () {
        contentSpan.classList.add('highlight');
        const startPos = parseInt(contentSpan.dataset.startPos);
        const endPos = parseInt(contentSpan.dataset.endPos);
        if (!isNaN(startPos) && !isNaN(endPos)) {
          highlightInputText(startPos, endPos);
        }
      });

      contentSpan.addEventListener('mouseleave', function () {
        contentSpan.classList.remove('highlight');
        clearInputHighlight();
      });
    } else {
      // Mobile: Tap-based highlighting (toggle)
      contentSpan.addEventListener('touchstart', function (e) {
        e.preventDefault();
        handleMobileHighlight(contentSpan);
      });

      contentSpan.addEventListener('click', function (e) {
        e.preventDefault();
        handleMobileHighlight(contentSpan);
      });
    }
  }

  /**
   * Handles mobile highlighting toggle for touch devices.
   * Toggles highlight on/off when tapping the same span, or switches to new span.
   * @param {HTMLSpanElement} span - The span to highlight
   */
  function handleMobileHighlight(span) {
    const isCurrentlyHighlighted = span.classList.contains('highlight');

    // Clear all highlights first
    clearAllHighlights();

    // If this span wasn't highlighted before, highlight it now
    if (!isCurrentlyHighlighted) {
      span.classList.add('highlight');
      span.dataset.highlighted = 'true';

      const startPos = parseInt(span.dataset.startPos);
      const endPos = parseInt(span.dataset.endPos);
      if (!isNaN(startPos) && !isNaN(endPos)) {
        highlightInputText(startPos, endPos);
      }
    } else {
      // If it was highlighted, just clear (already done above)
      clearInputHighlight();
    }
  }

  /**
   * Highlights text in the input textarea based on character positions.
   * @param {number} startPos - Starting character position
   * @param {number} endPos - Ending character position
   */
  function highlightInputText(startPos, endPos) {
    // Enable focus for programmatic text selection
    if (isTouchDevice()) {
      allowInputFocus = true;
    }

    inputText.focus();
    if (typeof inputText.setSelectionRange === 'function') {
      inputText.setSelectionRange(startPos, endPos);
      scrollInputToRange(startPos, endPos); // Centre the selection in viewport
    }

    // Restore focus prevention
    if (isTouchDevice()) {
      allowInputFocus = false;
    }
  }

  /**
   * Scrolls the textarea so the selected range is vertically centered in the viewport.
   * Uses a temporary clone to calculate precise text measurements for accurate positioning.
   * @param {number} startPos - Start position of the selection
   * @param {number} endPos - End position of the selection
   */
  function scrollInputToRange(startPos, endPos) {
    const style = window.getComputedStyle(inputText);
    const clone = document.createElement('textarea');

    // Clone essential styles so scrollHeight matches the real textarea
    const ESSENTIAL_STYLES = [
      'width',
      'fontFamily',
      'fontSize',
      'fontWeight',
      'lineHeight',
      'letterSpacing',
      'padding',
      'border',
      'boxSizing',
    ];
    ESSENTIAL_STYLES.forEach((prop) => (clone.style[prop] = style[prop]));

    // Position clone off-screen for measurement
    Object.assign(clone.style, {
      position: 'absolute',
      top: '-9999px',
      height: 'auto',
    });

    document.body.appendChild(clone);

    try {
      // Calculate height before the selection
      clone.value = originalInputText.slice(0, startPos);
      const heightBefore = clone.scrollHeight;

      // Calculate height of the selection itself
      clone.value = originalInputText.slice(startPos, endPos);
      const heightSelection = clone.scrollHeight;

      // Calculate optimal scroll position to center the selection
      const viewportHeight = inputText.clientHeight;
      const targetScrollTop = Math.max(
        0,
        heightBefore - viewportHeight / 2 + heightSelection / 2,
      );

      inputText.scrollTo({
        top: targetScrollTop,
        behavior: UI_CONFIG.SCROLL_SMOOTH_BEHAVIOR,
      });
    } finally {
      // Always cleanup the clone element
      document.body.removeChild(clone);
    }
  }

  /**
   * Starts the GSAP loader pulse animation.
   */
  function startLoaderAnimation() {
    const message = document.querySelector('.loader-message');
    const spinner = document.querySelector('.spinner');

    if (!message || !spinner) return;

    gsap.killTweensOf([message, spinner]);
    gsap.set([message, spinner], { clearProps: 'all' });

    gsap.to(spinner, {
      rotation: 360,
      duration: 1.8,
      ease: 'none',
      repeat: -1,
    });

    gsap.fromTo(
      message,
      {
        opacity: 0.4,
        scale: 0.98,
      },
      {
        opacity: 1,
        scale: 1,
        duration: 1.2,
        ease: 'power2.inOut',
        yoyo: true,
        repeat: -1,
      },
    );

    gsap.to(message, {
      color: '#4285F4',
      duration: 2,
      ease: 'sine.inOut',
      yoyo: true,
      repeat: -1,
    });
  }

  /**
   * Clears any highlighting in the input textarea.
   */
  function clearInputHighlight() {
    if (document.activeElement === inputText) {
      inputText.blur();
    }
  }

  const rawOutput = document.getElementById('raw-output');
  const promptOutput = document.getElementById('prompt-output');

  /**
   * Shows or hides the prompt view panel.
   * @param {boolean} show - Whether to show the prompt view
   */
  function showPromptView(show) {
    if (!promptOutput) return;
    promptOutput.style.display = show ? 'block' : 'none';
    inputText.style.display = show ? 'none' : 'block';
  }

  if (rawToggle) {
    rawToggle.addEventListener('change', () => {
      const showRaw = rawToggle.checked;
      rawOutput.style.display = showRaw ? 'block' : 'none';
      outputTextContainer.style.display = showRaw ? 'none' : 'block';

      const mobileRawToggle = document.getElementById('raw-toggle-mobile');
      if (mobileRawToggle) {
        mobileRawToggle.checked = showRaw;
      }

      if (showRaw) {
        setTimeout(() => {
          const formatter = rawOutput._jsonFormatter;
          if (formatter && formatter.openAtDepth) {
            try {
              formatter.openAtDepth(3);
              return;
            } catch (e) {
              // Fall back to manual clicking
            }
          }

          // Fallback: manually click the root toggler if it's collapsed
          const rootToggler = rawOutput.querySelector(
            '.json-formatter-toggler',
          );
          if (rootToggler) {
            const arrow =
              rootToggler.querySelector('.json-formatter-toggler-link') ||
              rootToggler;
            const arrowText = arrow.textContent || arrow.innerText || '';

            if (arrowText.includes('►') || !arrowText.includes('▼')) {
              try {
                rootToggler.click();
              } catch (e) {
                console.error('Failed to expand JSON:', e);
              }
            }
          }
        }, 100);
      }
    });
  }

  if (promptToggle) {
    promptToggle.addEventListener('change', () => {
      const showPrompt = promptToggle.checked;
      showPromptView(showPrompt);
      // Synchronize with mobile toggle
      const mobilePromptToggle = document.getElementById(
        'prompt-toggle-mobile',
      );
      if (mobilePromptToggle) {
        mobilePromptToggle.checked = showPrompt;
      }
    });
  }

  // Mobile prompt toggle event handling
  const mobilePromptToggle = document.getElementById('prompt-toggle-mobile');
  if (mobilePromptToggle && promptToggle) {
    mobilePromptToggle.addEventListener('change', () => {
      const showPrompt = mobilePromptToggle.checked;
      promptToggle.checked = showPrompt;
      showPromptView(showPrompt);
    });
  }

  // Mobile raw toggle event handling
  const mobileRawToggle = document.getElementById('raw-toggle-mobile');
  if (mobileRawToggle && rawToggle) {
    mobileRawToggle.addEventListener('change', () => {
      const showRaw = mobileRawToggle.checked;
      rawToggle.checked = showRaw;
      rawToggle.dispatchEvent(new Event('change'));
    });
  }
});

/**
 * Scrolls to the output panel to direct user focus to the results area.
 * Provides improved navigation experience for sample report selection workflow.
 */
function scrollToOutput() {
  const outputContainer = document.getElementById('output-container');

  if (outputContainer) {
    // Smooth scroll to the output area
    outputContainer.scrollIntoView({
      behavior: 'smooth',
      block: 'center',
    });
  }
}

/**
 * Toggles the interface options panel between expanded and collapsed states.
 */
function toggleInterfaceOptions() {
  const content = document.getElementById('interface-options-content');
  const icon = document.getElementById('interface-expand-icon');

  if (content.style.display === 'none' || content.style.display === '') {
    content.style.display = 'block';
    icon.classList.add('expanded');
  } else {
    content.style.display = 'none';
    icon.classList.remove('expanded');
  }
}

// Set up event delegation for interface toggle
document.addEventListener('click', (e) => {
  if (e.target.closest('[data-action="toggle-interface"]')) {
    toggleInterfaceOptions();
  }
});
