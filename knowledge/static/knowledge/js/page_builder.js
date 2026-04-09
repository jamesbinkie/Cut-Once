(function() {
    // 1. Load Quill.js resources
    const quillCss = document.createElement('link');
    quillCss.rel = 'stylesheet';
    quillCss.href = 'https://cdn.quilljs.com/1.3.6/quill.snow.css';
    document.head.appendChild(quillCss);

    const quillJs = document.createElement('script');
    quillJs.src = 'https://cdn.quilljs.com/1.3.6/quill.js';
    document.head.appendChild(quillJs);

    function initFullEditor() {
        // Targets the standard 'content' textarea
        const textArea = document.querySelector('textarea[name="content"]');
        if (!textArea) return;

        textArea.style.display = 'none';

        // Create the Google Docs style container
        const editorContainer = document.createElement('div');
        editorContainer.style = "background: white; margin-bottom: 20px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.1);";
        editorContainer.innerHTML = `<div id="quill-document-editor" style="height: 600px; font-size: 16px;">${textArea.value}</div>`;
        textArea.parentNode.insertBefore(editorContainer, textArea);

        // Initialize Quill with full toolbar (Headers, Colors, Align, Media)
        const quill = new Quill('#quill-document-editor', {
            theme: 'snow',
            modules: {
                toolbar: [
                    [{ 'header': [1, 2, 3, false] }],
                    ['bold', 'italic', 'underline', 'strike'],
                    [{ 'color': [] }, { 'background': [] }], // Text & Highlight colors
                    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                    [{ 'align': [] }],
                    ['link', 'image', 'video'],
                    ['clean']
                ]
            }
        });

        // Sync Quill back to the hidden textarea for Django to save
        quill.on('text-change', function() {
            textArea.value = quill.root.innerHTML;
        });
    }

    quillJs.onload = initFullEditor;
})();
