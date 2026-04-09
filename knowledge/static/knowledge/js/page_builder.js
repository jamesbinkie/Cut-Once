(function() {
    // 1. Load external Quill resources
    const quillCss = document.createElement('link');
    quillCss.rel = 'stylesheet';
    quillCss.href = 'https://cdn.quilljs.com/1.3.6/quill.snow.css';
    document.head.appendChild(quillCss);

    const quillJs = document.createElement('script');
    quillJs.src = 'https://cdn.quilljs.com/1.3.6/quill.js';
    document.head.appendChild(quillJs);

    function initFullEditor() {
        // Find the standard Django content textarea
        const textArea = document.querySelector('textarea[name="content"]');
        if (!textArea) return;

        // Hide the original textarea
        textArea.style.display = 'none';

        // Create a container for the Google Docs style editor
        const editorContainer = document.createElement('div');
        editorContainer.style = "background: white; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);";
        editorContainer.innerHTML = `<div id="quill-document-editor" style="height: 600px; font-size: 16px;">${textArea.value}</div>`;
        textArea.parentNode.insertBefore(editorContainer, textArea);

        // Initialize Quill with a full-featured toolbar
        const quill = new Quill('#quill-document-editor', {
            theme: 'snow',
            modules: {
                toolbar: [
                    [{ 'header': [1, 2, 3, false] }],
                    ['bold', 'italic', 'underline', 'strike'],
                    [{ 'color': [] }, { 'background': [] }], // Text color & highlight
                    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                    [{ 'align': [] }],
                    ['link', 'image', 'video'], // Media embedding
                    ['clean'] // Clear formatting button
                ]
            }
        });

        // Sync Quill content back to the hidden Django textarea for saving
        quill.on('text-change', function() {
            textArea.value = quill.root.innerHTML;
        });
    }

    // Fire the editor once the script is loaded
    quillJs.onload = initFullEditor;
})();
