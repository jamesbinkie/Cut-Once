(function() {
    // 1. Inject Quill.js resources directly
    const qCss = document.createElement('link');
    qCss.rel = 'stylesheet'; 
    qCss.href = 'https://cdn.quilljs.com/1.3.6/quill.snow.css';
    document.head.appendChild(qCss);

    const qJs = document.createElement('script');
    qJs.src = 'https://cdn.quilljs.com/1.3.6/quill.js';
    document.head.appendChild(qJs);

    function startEditor() {
        // Critical: Look for the textarea specifically by ID and Name
        const targetField = document.getElementById('id_content') || document.querySelector('textarea[name="content"]');
        if (!targetField) {
            console.error("Editor Error: Could not find the 'content' field.");
            return;
        }

        // Hide the standard box
        targetField.style.display = 'none';

        // Create the editor container
        const container = document.createElement('div');
        container.style = "background: white; border: 1px solid #ccc; border-radius: 4px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px; color: black !important;";
        container.innerHTML = `<div id="google-doc-editor" style="height: 500px; font-size: 16px;">${targetField.value}</div>`;
        targetField.parentNode.insertBefore(container, targetField);

        // Initialize Quill
        const quill = new Quill('#google-doc-editor', {
            theme: 'snow',
            modules: {
                toolbar: [
                    [{ 'header': [1, 2, 3, false] }],
                    ['bold', 'italic', 'underline', 'strike'],
                    [{ 'color': [] }, { 'background': [] }],
                    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                    [{ 'align': [] }],
                    ['link', 'image', 'video'],
                    ['clean']
                ]
            }
        });

        // Sync contents for saving
        quill.on('text-change', () => {
            targetField.value = quill.root.innerHTML;
        });
    }

    // Force wait for Quill to load and the DOM to be ready
    qJs.onload = () => {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', startEditor);
        } else {
            startEditor();
        }
    };
})();
