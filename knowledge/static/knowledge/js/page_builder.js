(function() {
    // 1. Inject External Quill CSS
    const qCss = document.createElement('link');
    qCss.rel = 'stylesheet'; qCss.href = 'https://cdn.quilljs.com/1.3.6/quill.snow.css';
    document.head.appendChild(qCss);

    // 2. Inject External Quill JS
    const qJs = document.createElement('script');
    qJs.src = 'https://cdn.quilljs.com/1.3.6/quill.js';
    document.head.appendChild(qJs);

    // 3. Inject Image Formatter Module (Allows dragging, resizing, and aligning)
    const qFormatJs = document.createElement('script');
    qFormatJs.src = 'https://unpkg.com/quill-blot-formatter@1.0.5/dist/quill-blot-formatter.min.js';
    document.head.appendChild(qFormatJs);

    function startEditor() {
        const targetField = document.getElementById('id_content');
        if (!targetField) return;

        targetField.style.display = 'none';
        if (document.getElementById('google-doc-editor')) return;

        const container = document.createElement('div');
        // INCREASED HEIGHT: Now 75vh (75% of window height) with a min-height fallback
        container.style = "background: white; border: 1px solid #ccc; border-radius: 4px; margin-bottom: 20px; color: black !important;";
        container.innerHTML = `<div id="google-doc-editor" style="height: 75vh; min-height: 600px; font-size: 16px;">${targetField.value}</div>`;
        targetField.parentNode.insertBefore(container, targetField);

        // Register the new image moving/resizing module
        Quill.register('modules/blotFormatter', QuillBlotFormatter.default);

        const quill = new Quill('#google-doc-editor', {
            theme: 'snow',
            modules: {
                // Activate the image formatter
                blotFormatter: {},
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

        quill.on('text-change', () => {
            targetField.value = quill.root.innerHTML;
        });
    }

    // Ensure both scripts load before trying to build the editor
    let scriptsLoaded = 0;
    function checkLoad() {
        scriptsLoaded++;
        if (scriptsLoaded === 2) { // Wait for both Quill and Formatter to load
            if (document.readyState === 'complete' || document.readyState === 'interactive') {
                startEditor();
            } else {
                window.addEventListener('load', startEditor);
            }
        }
    }

    qJs.onload = checkLoad;
    qFormatJs.onload = checkLoad;
})();
