(function () {
  function exec(editor, command, value) {
    editor.focus();
    document.execCommand(command, false, value || null);
    sync(editor);
  }

  function sync(editor) {
    const textarea = editor.closest(".rich-text-editor-shell").querySelector("textarea.rich-text-source");
    textarea.value = editor.innerHTML;
  }

  function init(textarea) {
    if (textarea.dataset.richTextInitialized === "1") return;
    textarea.dataset.richTextInitialized = "1";

    const shell = document.createElement("div");
    shell.className = "rich-text-editor-shell";

    const toolbar = document.createElement("div");
    toolbar.className = "rich-text-editor-toolbar";

    const editor = document.createElement("div");
    editor.className = "rich-text-editor-surface";
    editor.contentEditable = "true";
    editor.setAttribute("role", "textbox");
    editor.setAttribute("aria-multiline", "true");
    editor.innerHTML = textarea.value || "";

    const buttons = [
      { label: "B", command: "bold", title: "Bold" },
      { label: "I", command: "italic", title: "Italic" },
      { label: "U", command: "underline", title: "Underline" },
      { label: "UL", command: "insertUnorderedList", title: "Bullet list" },
      { label: "OL", command: "insertOrderedList", title: "Numbered list" },
      { label: "Clear", command: "removeFormat", title: "Clear formatting" },
    ];

    buttons.forEach(function (buttonDef) {
      const button = document.createElement("button");
      button.type = "button";
      button.className = "rich-text-editor-button";
      button.textContent = buttonDef.label;
      button.title = buttonDef.title;
      button.addEventListener("click", function () {
        exec(editor, buttonDef.command);
      });
      toolbar.appendChild(button);
    });

    editor.addEventListener("input", function () {
      sync(editor);
    });

    textarea.insertAdjacentElement("beforebegin", shell);
    shell.appendChild(toolbar);
    shell.appendChild(editor);
    shell.appendChild(textarea);
    textarea.hidden = true;
  }

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("textarea.rich-text-source").forEach(init);
  });
})();
