(function() {
    // 1. Load Quill Editor Resources
    const qCss = document.createElement('link');
    qCss.rel = 'stylesheet'; qCss.href = 'https://cdn.quilljs.com/1.3.6/quill.snow.css';
    document.head.appendChild(qCss);

    const qJs = document.createElement('script');
    qJs.src = 'https://cdn.quilljs.com/1.3.6/quill.js';
    document.head.appendChild(qJs);

    function startEditor() {
        // Matches the ID labled 'id_content' in your admin HTML
        const targetField = document.getElementById('id_content');
        if (!targetField) return;

        targetField.style.display = 'none';
        const container = document.createElement('div');
        container.style = "background: white; border: 1px solid #ccc; border-radius: 4px; margin-bottom: 20px; color: black !important;";
        container.innerHTML = `<div id="google-doc-editor" style="height: 500px; font-size: 16px;">${targetField.value}</div>`;
        targetField.parentNode.insertBefore(container, targetField);

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

        quill.on('text-change', () => {
            targetField.value = quill.root.innerHTML;
        });
    }

    qJs.onload = () => {
        if (document.readyState === 'complete' || document.readyState === 'interactive') {
            startEditor();
        } else {
            window.addEventListener('load', startEditor);
        }
    };
})();
