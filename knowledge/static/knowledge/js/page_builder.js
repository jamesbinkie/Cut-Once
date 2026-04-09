(function() {
    // 1. Inject Quill.js resources directly into the head
    const qCss = document.createElement('link');
    qCss.rel = 'stylesheet'; 
    qCss.href = 'https://cdn.quilljs.com/1.3.6/quill.snow.css';
    document.head.appendChild(qCss);

    const qJs = document.createElement('script');
    qJs.src = 'https://cdn.quilljs.com/1.3.6/quill.js';
    document.head.appendChild(qJs);

    function startEditor() {
        // Target the 'content' field shown in your HTML file
        const targetField = document.querySelector('textarea[name="content"]');
        if (!targetField) return;

        // Hide standard box and create editor surface
        targetField.style.display = 'none';
        const container = document.createElement('div');
        // Styling the container for a clean "Doc" look
        container.style = "background: white; border: 1px solid #ccc; border-radius: 4px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px;";
        container.innerHTML = `<div id="google-doc-editor" style="height: 500px; font-size: 16px;">${targetField.value}</div>`;
        targetField.parentNode.insertBefore(container, targetField);

        // Professional formatting toolbar configuration (Google Docs style)
        const quill = new Quill('#google-doc-editor', {
            theme: 'snow',
            modules: {
                toolbar: [
                    [{ 'header': [1, 2, 3, false] }],
                    ['bold', 'italic', 'underline', 'strike'],
                    [{ 'color': [] }, { 'background': [] }], // Text & Highlight colors
                    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                    [{ 'align': [] }],
                    ['link', 'image', 'video'],
                    ['clean'] // Button to remove formatting
                ]
            }
        });

        // Keep the hidden Django field in sync for saving
        quill.on('text-change', () => {
            targetField.value = quill.root.innerHTML;
        });
    }

    // Wait for the library to load, then fire the editor
    qJs.onload = () => {
        if (document.readyState === 'complete') { 
            startEditor(); 
        } else { 
            window.addEventListener('load', startEditor); 
        }
    };
})();
