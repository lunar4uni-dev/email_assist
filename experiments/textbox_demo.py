import gradio as gr


class RichTextbox(gr.HTML):
    """A rich text editor component built on gr.HTML with a formatting toolbar."""

    def __init__(
        self,
        value="",
        label="Rich Textbox",
        placeholder="Type here...",
        **kwargs,
    ):
        html_template = """
<div class="rte-container">
    <div class="rte-toolbar">
        <div class="rte-btn-group">
            <button class="rte-btn" data-cmd="bold" title="Bold (Ctrl+B)"><b>B</b></button>
            <button class="rte-btn" data-cmd="italic" title="Italic (Ctrl+I)"><i>I</i></button>
            <button class="rte-btn" data-cmd="underline" title="Underline (Ctrl+U)"><u>U</u></button>
            <button class="rte-btn" data-cmd="strikeThrough" title="Strikethrough"><s>S</s></button>
        </div>
        <div class="rte-sep"></div>
        <div class="rte-btn-group">
            <button class="rte-btn rte-color-btn" data-action="foreColor" title="Text Color">
                <span class="rte-color-label">A</span>
                <span class="rte-color-bar" id="rte-fg-bar"></span>
            </button>
            <button class="rte-btn rte-color-btn" data-action="hiliteColor" title="Highlight">
                <span class="rte-hl-label">A</span>
                <span class="rte-color-bar" id="rte-bg-bar"></span>
            </button>
        </div>
        <div class="rte-sep"></div>
        <div class="rte-btn-group">
            <button class="rte-btn" data-cmd="insertOrderedList" title="Ordered List">OL</button>
            <button class="rte-btn" data-cmd="insertUnorderedList" title="Unordered List">UL</button>
            <button class="rte-btn" data-action="blockquote" title="Blockquote">&gt;</button>
        </div>
        <div class="rte-sep"></div>
        <div class="rte-btn-group">
            <button class="rte-btn" data-action="inlineCode" title="Inline Code">&lt;/&gt;</button>
            <button class="rte-btn" data-action="codeBlock" title="Code Block">{ }</button>
        </div>
        <div class="rte-sep"></div>
        <div class="rte-btn-group">
            <button class="rte-btn" data-action="link" title="Insert Link">&#128279;</button>
            <button class="rte-btn" data-action="emoji" title="Insert Emoji">&#128578;</button>
        </div>
    </div>
    <div class="rte-popup rte-color-popup" id="rte-color-popup" style="display:none;"></div>
    <div class="rte-popup rte-link-popup" id="rte-link-popup" style="display:none;">
        <input type="text" class="rte-link-input" placeholder="https://example.com" />
        <div class="rte-link-actions">
            <button class="rte-link-cancel">Cancel</button>
            <button class="rte-link-ok">OK</button>
        </div>
    </div>
    <div class="rte-popup rte-emoji-popup" id="rte-emoji-popup" style="display:none;"></div>
    <div class="rte-editor" contenteditable="true"></div>
</div>
"""

        css_template = """
.rte-container {
    border: 1px solid var(--border-color-primary, #d1d5db);
    border-radius: var(--radius-lg, 8px);
    overflow: visible;
    font-family: var(--font, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif);
    position: relative;
    background: var(--background-fill-primary, #ffffff);
}
.rte-toolbar {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 2px;
    padding: 6px 8px;
    background: var(--background-fill-secondary, #f9fafb);
    border-bottom: 1px solid var(--border-color-primary, #d1d5db);
    border-radius: var(--radius-lg, 8px) var(--radius-lg, 8px) 0 0;
}
.rte-btn-group {
    display: flex;
    gap: 2px;
}
.rte-btn {
    width: 32px;
    height: 32px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border: 1px solid transparent;
    border-radius: 4px;
    background: transparent;
    cursor: pointer;
    font-size: 14px;
    color: var(--body-text-color, #374151);
    transition: background 0.15s, border-color 0.15s;
    padding: 0;
    line-height: 1;
}
.rte-btn:hover {
    background: var(--background-fill-primary, #e5e7eb);
    border-color: var(--border-color-primary, #d1d5db);
}
.rte-btn.active {
    background: #dbeafe;
    border-color: #3b82f6;
    color: #3b82f6;
}
.rte-sep {
    width: 1px;
    height: 24px;
    background: var(--border-color-primary, #d1d5db);
    margin: 0 4px;
    flex-shrink: 0;
}
.rte-color-btn {
    gap: 1px;
}
.rte-color-label {
    font-weight: 700;
    font-size: 15px;
    line-height: 1;
}
.rte-hl-label {
    font-weight: 700;
    font-size: 15px;
    line-height: 1;
    background: #ffff00;
    padding: 0 3px;
    border-radius: 2px;
}
.rte-color-bar {
    display: block;
    height: 3px;
    width: 18px;
    border-radius: 1px;
}
#rte-fg-bar { background: #e53e3e; }
#rte-bg-bar { background: #ffff00; }

/* Popups */
.rte-popup {
    position: absolute;
    z-index: 1000;
    background: var(--background-fill-primary, #ffffff);
    border: 1px solid var(--border-color-primary, #d1d5db);
    border-radius: 8px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.12);
    padding: 8px;
}
.rte-color-popup { left: 50px; top: 46px; }
.rte-color-grid {
    display: grid;
    grid-template-columns: repeat(6, 1fr);
    gap: 4px;
}
.rte-color-swatch {
    width: 26px;
    height: 26px;
    border-radius: 4px;
    border: 2px solid transparent;
    cursor: pointer;
    transition: transform 0.1s, border-color 0.15s;
    padding: 0;
}
.rte-color-swatch:hover {
    transform: scale(1.15);
    border-color: #3b82f6;
}
.rte-link-popup {
    left: 50%;
    top: 46px;
    transform: translateX(-50%);
    width: 300px;
    padding: 12px;
}
.rte-link-input {
    width: 100%;
    padding: 8px 10px;
    border: 1px solid var(--border-color-primary, #d1d5db);
    border-radius: 6px;
    font-size: 13px;
    box-sizing: border-box;
    margin-bottom: 8px;
    outline: none;
}
.rte-link-input:focus {
    border-color: #3b82f6;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.15);
}
.rte-link-actions {
    display: flex;
    justify-content: flex-end;
    gap: 6px;
}
.rte-link-actions button {
    padding: 5px 14px;
    border-radius: 6px;
    border: 1px solid var(--border-color-primary, #d1d5db);
    cursor: pointer;
    font-size: 13px;
    background: var(--background-fill-primary, #fff);
}
.rte-link-ok {
    background: #3b82f6 !important;
    color: #fff !important;
    border-color: #3b82f6 !important;
}
.rte-link-ok:hover { background: #2563eb !important; }
.rte-emoji-popup {
    right: 8px;
    top: 46px;
    width: 270px;
    max-height: 220px;
    overflow-y: auto;
}
.rte-emoji-grid {
    display: grid;
    grid-template-columns: repeat(8, 1fr);
    gap: 2px;
}
.rte-emoji-item {
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    border-radius: 4px;
    font-size: 18px;
    border: none;
    background: transparent;
    padding: 0;
}
.rte-emoji-item:hover {
    background: var(--background-fill-secondary, #f3f4f6);
}

/* Editor */
.rte-editor {
    min-height: 200px;
    max-height: 500px;
    padding: 12px 16px;
    outline: none;
    font-size: 15px;
    line-height: 1.7;
    color: var(--body-text-color, #1f2937);
    overflow-y: auto;
}
.rte-editor:empty:before {
    content: attr(data-placeholder);
    color: var(--body-text-color-subdued, #9ca3af);
    pointer-events: none;
}
.rte-editor blockquote {
    border-left: 4px solid #3b82f6;
    margin: 8px 0;
    padding: 6px 14px;
    color: #4b5563;
    background: #f0f5ff;
    border-radius: 0 6px 6px 0;
}
.rte-editor code {
    background: #f3f4f6;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: 'SFMono-Regular', Consolas, 'Liberation Mono', Menlo, monospace;
    font-size: 0.88em;
    color: #e11d48;
}
.rte-editor pre {
    background: #1e293b;
    color: #e2e8f0;
    padding: 14px 18px;
    border-radius: 8px;
    overflow-x: auto;
    margin: 10px 0;
    line-height: 1.5;
}
.rte-editor pre code {
    background: transparent;
    color: inherit;
    padding: 0;
    font-size: 0.9em;
}
.rte-editor a {
    color: #3b82f6;
    text-decoration: underline;
}
.rte-editor ul, .rte-editor ol {
    padding-left: 24px;
    margin: 6px 0;
}
.rte-editor li {
    margin: 2px 0;
}
"""

        js_on_load = """
(function() {
    var editor = element.querySelector('.rte-editor');
    var colorPopup = element.querySelector('#rte-color-popup');
    var linkPopup = element.querySelector('#rte-link-popup');
    var emojiPopup = element.querySelector('#rte-emoji-popup');
    var fgBar = element.querySelector('#rte-fg-bar');
    var bgBar = element.querySelector('#rte-bg-bar');
    var linkInput = element.querySelector('.rte-link-input');

    var activeColorAction = null;
    var savedRange = null;

    /* Placeholder */
    if (props.placeholder) {
        editor.setAttribute('data-placeholder', props.placeholder);
    }

    /* Initial content */
    if (props.value) {
        editor.innerHTML = props.value;
    }

    /* Use CSS-based styling for foreColor so it generates <span style="color:..."> instead of <font> */
    try { document.execCommand('styleWithCSS', false, true); } catch(e) {}

    /* --- Helpers --- */
    function saveSelection() {
        var sel = window.getSelection();
        if (sel && sel.rangeCount > 0) {
            savedRange = sel.getRangeAt(0).cloneRange();
        }
    }
    function restoreSelection() {
        if (savedRange) {
            var sel = window.getSelection();
            sel.removeAllRanges();
            sel.addRange(savedRange);
        }
    }
    function closeAllPopups() {
        colorPopup.style.display = 'none';
        linkPopup.style.display = 'none';
        emojiPopup.style.display = 'none';
    }
    function syncValue() {
        var html = editor.innerHTML;
        if (html !== props.value) {
            props.value = html;
        }
    }
    function updateToolbarState() {
        element.querySelectorAll('.rte-btn[data-cmd]').forEach(function(btn) {
            try {
                if (document.queryCommandState(btn.dataset.cmd)) {
                    btn.classList.add('active');
                } else {
                    btn.classList.remove('active');
                }
            } catch(e) {}
        });
    }

    /* --- Color Palette --- */
    var COLORS = [
        '#000000','#434343','#666666','#999999','#b7b7b7','#ffffff',
        '#e53e3e','#dd6b20','#d69e2e','#38a169','#3182ce','#805ad5',
        '#ff0000','#ff9900','#ffff00','#00ff00','#00bfff','#0000ff',
        '#f56565','#ed8936','#ecc94b','#48bb78','#4299e1','#9f7aea'
    ];
    var colorGrid = document.createElement('div');
    colorGrid.className = 'rte-color-grid';
    COLORS.forEach(function(color) {
        var swatch = document.createElement('button');
        swatch.className = 'rte-color-swatch';
        swatch.style.background = color;
        if (color === '#ffffff') {
            swatch.style.borderColor = '#d1d5db';
        }
        swatch.setAttribute('data-color', color);
        swatch.addEventListener('mousedown', function(e) { e.preventDefault(); });
        swatch.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            restoreSelection();
            editor.focus();
            document.execCommand(activeColorAction, false, color);
            if (activeColorAction === 'foreColor') {
                fgBar.style.background = color;
            } else {
                bgBar.style.background = color;
            }
            closeAllPopups();
            syncValue();
        });
        colorGrid.appendChild(swatch);
    });
    colorPopup.appendChild(colorGrid);

    /* --- Emoji Grid --- */
    var EMOJIS = [
        '\\u{1F600}','\\u{1F602}','\\u{1F60A}','\\u{1F60D}','\\u{1F970}','\\u{1F60E}','\\u{1F914}','\\u{1F622}',
        '\\u{1F621}','\\u{1F973}','\\u{1F631}','\\u{1F917}','\\u{1F634}','\\u{1F92E}','\\u{1F910}','\\u{1F607}',
        '\\u{1F44D}','\\u{1F44E}','\\u{1F44F}','\\u{1F64C}','\\u{1F4AA}','\\u{1F91D}','\\u270C\\uFE0F','\\u{1F44B}',
        '\\u2764\\uFE0F','\\u{1F525}','\\u2B50','\\u{1F4AF}','\\u2705','\\u274C','\\u26A1','\\u{1F389}',
        '\\u{1F4CC}','\\u{1F4A1}','\\u{1F4CE}','\\u{1F517}','\\u{1F4DD}','\\u{1F4AC}','\\u{1F440}','\\u{1F3AF}'
    ];
    var emojiGrid = document.createElement('div');
    emojiGrid.className = 'rte-emoji-grid';
    EMOJIS.forEach(function(emoji) {
        var btn = document.createElement('button');
        btn.className = 'rte-emoji-item';
        btn.textContent = emoji;
        btn.addEventListener('mousedown', function(e) { e.preventDefault(); });
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            restoreSelection();
            editor.focus();
            document.execCommand('insertText', false, emoji);
            closeAllPopups();
            syncValue();
        });
        emojiGrid.appendChild(btn);
    });
    emojiPopup.appendChild(emojiGrid);

    /* --- Close popups on outside click --- */
    document.addEventListener('mousedown', function(e) {
        if (!element.contains(e.target)) {
            closeAllPopups();
        }
    });

    /* --- Editor input sync --- */
    editor.addEventListener('input', function() {
        syncValue();
    });

    /* --- Toolbar: execCommand buttons --- */
    element.querySelectorAll('.rte-btn[data-cmd]').forEach(function(btn) {
        btn.addEventListener('mousedown', function(e) { e.preventDefault(); });
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            editor.focus();
            document.execCommand(btn.dataset.cmd, false, null);
            syncValue();
            updateToolbarState();
        });
    });

    /* --- Toolbar: custom action buttons --- */
    element.querySelectorAll('.rte-btn[data-action]').forEach(function(btn) {
        btn.addEventListener('mousedown', function(e) { e.preventDefault(); });
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            var action = btn.dataset.action;

            if (action === 'foreColor' || action === 'hiliteColor') {
                saveSelection();
                activeColorAction = action;
                closeAllPopups();
                colorPopup.style.display = colorPopup.style.display === 'none' ? 'block' : 'none';
            } else if (action === 'link') {
                saveSelection();
                closeAllPopups();
                linkInput.value = '';
                linkPopup.style.display = 'block';
                linkInput.focus();
            } else if (action === 'emoji') {
                saveSelection();
                closeAllPopups();
                emojiPopup.style.display = emojiPopup.style.display === 'none' ? 'block' : 'none';
            } else if (action === 'inlineCode') {
                var sel = window.getSelection();
                if (sel && sel.rangeCount > 0 && !sel.isCollapsed) {
                    var range = sel.getRangeAt(0);
                    var code = document.createElement('code');
                    try {
                        range.surroundContents(code);
                    } catch(err) {
                        code.textContent = range.toString();
                        range.deleteContents();
                        range.insertNode(code);
                    }
                    sel.removeAllRanges();
                }
                syncValue();
            } else if (action === 'codeBlock') {
                var sel = window.getSelection();
                if (sel && sel.rangeCount > 0) {
                    var range = sel.getRangeAt(0);
                    var pre = document.createElement('pre');
                    var codeEl = document.createElement('code');
                    if (sel.isCollapsed) {
                        codeEl.textContent = '\\n';
                    } else {
                        codeEl.textContent = range.toString();
                        range.deleteContents();
                    }
                    pre.appendChild(codeEl);
                    range.insertNode(pre);
                    var newRange = document.createRange();
                    newRange.selectNodeContents(codeEl);
                    newRange.collapse(false);
                    sel.removeAllRanges();
                    sel.addRange(newRange);
                }
                syncValue();
            } else if (action === 'blockquote') {
                editor.focus();
                document.execCommand('formatBlock', false, 'blockquote');
                syncValue();
            }
        });
    });

    /* --- Link popup handlers --- */
    element.querySelector('.rte-link-ok').addEventListener('mousedown', function(e) { e.preventDefault(); });
    element.querySelector('.rte-link-ok').addEventListener('click', function(e) {
        e.preventDefault();
        var url = linkInput.value.trim();
        if (url) {
            restoreSelection();
            editor.focus();
            document.execCommand('createLink', false, url);
        }
        closeAllPopups();
        syncValue();
    });
    element.querySelector('.rte-link-cancel').addEventListener('mousedown', function(e) { e.preventDefault(); });
    element.querySelector('.rte-link-cancel').addEventListener('click', function(e) {
        e.preventDefault();
        closeAllPopups();
    });
    linkInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            element.querySelector('.rte-link-ok').click();
        } else if (e.key === 'Escape') {
            closeAllPopups();
        }
    });

    /* --- Active state tracking --- */
    editor.addEventListener('keyup', updateToolbarState);
    editor.addEventListener('mouseup', updateToolbarState);

    /* --- Keyboard shortcut sync --- */
    editor.addEventListener('keydown', function(e) {
        if ((e.ctrlKey || e.metaKey) && ['b','i','u'].indexOf(e.key.toLowerCase()) !== -1) {
            setTimeout(function() {
                syncValue();
                updateToolbarState();
            }, 0);
        }
    });

    /* --- Helper: check if cursor is at the end of a node --- */
    function isAtEndOf(node) {
        var sel = window.getSelection();
        if (!sel || sel.rangeCount === 0) return false;
        var range = sel.getRangeAt(0);
        var testRange = document.createRange();
        testRange.selectNodeContents(node);
        testRange.setStart(range.endContainer, range.endOffset);
        return testRange.toString().length === 0;
    }

    /* --- Helper: insert a clean paragraph after a node and move cursor there --- */
    function insertParagraphAfter(refNode) {
        var sel = window.getSelection();
        var p = document.createElement('p');
        p.innerHTML = '<br>';
        refNode.parentNode.insertBefore(p, refNode.nextSibling);
        var newR = document.createRange();
        newR.setStart(p, 0);
        newR.collapse(true);
        sel.removeAllRanges();
        sel.addRange(newR);
    }

    /* --- Helper: find ancestor matching condition, up to (but not including) stopAt --- */
    function findAncestor(node, testFn, stopAt) {
        var cur = node && node.nodeType === 3 ? node.parentNode : node;
        while (cur && cur !== stopAt) {
            if (testFn(cur)) return cur;
            cur = cur.parentNode;
        }
        return null;
    }

    function isHighlightSpan(el) {
        return el.nodeName === 'SPAN' && el.style && (el.style.backgroundColor || el.style.color);
    }
    function isInlineCode(el) {
        return el.nodeName === 'CODE' && (!el.parentNode || el.parentNode.nodeName !== 'PRE');
    }

    /* ======================================================
       ENTER key: escape inline elements (highlight, code)
       and block elements (blockquote, pre)
       ====================================================== */
    editor.addEventListener('keydown', function(e) {
        if (e.key !== 'Enter' || e.shiftKey) return;
        var sel = window.getSelection();
        if (!sel || sel.rangeCount === 0) return;
        var range = sel.getRangeAt(0);
        var node = range.startContainer;

        /* --- 1. Inline: <span style="background-color/color"> or <code> (not inside <pre>) --- */
        var inlineEl = findAncestor(node, function(el) {
            return isHighlightSpan(el) || isInlineCode(el);
        }, editor);

        if (inlineEl && isAtEndOf(inlineEl)) {
            e.preventDefault();
            /* Split: move cursor out after the inline element, then let the browser do a normal line break */
            /* Insert a zero-width space after the inline element to anchor the cursor */
            var textNode = document.createTextNode('\\u200B');
            if (inlineEl.nextSibling) {
                inlineEl.parentNode.insertBefore(textNode, inlineEl.nextSibling);
            } else {
                inlineEl.parentNode.appendChild(textNode);
            }
            var newR = document.createRange();
            newR.setStartAfter(textNode);
            newR.collapse(true);
            sel.removeAllRanges();
            sel.addRange(newR);
            /* Now insert a line break at the new position outside the inline element */
            document.execCommand('insertParagraph', false, null);
            syncValue();
            return;
        }

        /* --- 2. Block: <pre> (double-Enter escape) --- */
        var preEl = findAncestor(node, function(el) { return el.nodeName === 'PRE'; }, editor);
        if (preEl) {
            var codeChild = preEl.querySelector('code') || preEl;
            var text = codeChild.textContent;
            if (isAtEndOf(preEl) && (text.endsWith('\\n') || text.endsWith('\\n\\n'))) {
                e.preventDefault();
                codeChild.textContent = text.replace(/\\n+$/, '');
                insertParagraphAfter(preEl);
                syncValue();
                return;
            }
            return; /* Normal Enter inside pre — don't interfere */
        }

        /* --- 3. Block: <blockquote> (Enter on empty line escapes) --- */
        var bqEl = findAncestor(node, function(el) { return el.nodeName === 'BLOCKQUOTE'; }, editor);
        if (bqEl) {
            var lastEl = bqEl.lastElementChild || bqEl.lastChild;
            var isEmpty = false;
            if (lastEl && lastEl.nodeName === 'BR') isEmpty = true;
            else if (lastEl && (lastEl.nodeName === 'DIV' || lastEl.nodeName === 'P') &&
                     (lastEl.innerHTML === '<br>' || lastEl.innerHTML === '' || lastEl.textContent.trim() === '')) isEmpty = true;
            if (isEmpty && isAtEndOf(bqEl)) {
                e.preventDefault();
                lastEl.remove();
                insertParagraphAfter(bqEl);
                syncValue();
                return;
            }
        }
    });

    /* ======================================================
       ESCAPE key: break out of current block/inline formatting
       ====================================================== */
    editor.addEventListener('keydown', function(e) {
        if (e.key !== 'Escape') return;
        var sel = window.getSelection();
        if (!sel || sel.rangeCount === 0) return;
        var node = sel.anchorNode;

        /* Inline: highlight span or inline code */
        var inlineEl = findAncestor(node, function(el) {
            return isHighlightSpan(el) || isInlineCode(el);
        }, editor);
        if (inlineEl) {
            e.preventDefault();
            /* Move cursor to right after the inline element */
            var textNode = document.createTextNode('\\u200B');
            if (inlineEl.nextSibling) {
                inlineEl.parentNode.insertBefore(textNode, inlineEl.nextSibling);
            } else {
                inlineEl.parentNode.appendChild(textNode);
            }
            var newR = document.createRange();
            newR.setStartAfter(textNode);
            newR.collapse(true);
            sel.removeAllRanges();
            sel.addRange(newR);
            syncValue();
            return;
        }

        /* Block: blockquote */
        var bqEl = findAncestor(node, function(el) { return el.nodeName === 'BLOCKQUOTE'; }, editor);
        if (bqEl) {
            e.preventDefault();
            document.execCommand('formatBlock', false, 'p');
            syncValue();
            return;
        }

        /* Block: pre/code block */
        var preEl = findAncestor(node, function(el) { return el.nodeName === 'PRE'; }, editor);
        if (preEl) {
            e.preventDefault();
            var text = preEl.textContent;
            var p = document.createElement('p');
            p.textContent = text;
            preEl.parentNode.replaceChild(p, preEl);
            var newR = document.createRange();
            newR.selectNodeContents(p);
            newR.collapse(false);
            sel.removeAllRanges();
            sel.addRange(newR);
            syncValue();
            return;
        }
    });
})();
"""

        super().__init__(
            value=value,
            label=label,
            html_template=html_template,
            css_template=css_template,
            js_on_load=js_on_load,
            apply_default_css=False,
            placeholder=placeholder,
            container=False,
            padding=False,
            **kwargs,
        )

    def api_info(self):
        return {"type": "string", "description": "HTML content of the rich text editor"}


if __name__ == "__main__":
    with gr.Blocks(title="Rich Text Editor Demo") as demo:
        gr.Markdown("# Rich Text Editor Demo")
        gr.Markdown(
            "A rich text editor built as a custom Gradio 6 `gr.HTML` component. "
            "Supports bold, italic, underline, strikethrough, text/highlight colors, "
            "emojis, links, lists, blockquotes, and code blocks."
        )

        editor = RichTextbox(
            value="<p>Welcome to the <b>Rich Text Editor</b>! Try out the toolbar above.</p>",
            label="Editor",
        )

        with gr.Row():
            get_html_btn = gr.Button("Get HTML", variant="primary")
            clear_btn = gr.Button("Clear", variant="secondary")

        html_output = gr.Code(label="HTML Output", language="html")

        get_html_btn.click(fn=lambda x: x, inputs=editor, outputs=html_output)
        clear_btn.click(fn=lambda: "", outputs=editor)
        editor.change(fn=lambda x: x, inputs=editor, outputs=html_output)

    demo.launch()