(function() {
    // 1. Inject External TinyMCE JS
    const tScript = document.createElement('script');
    tScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/tinymce/6.8.3/tinymce.min.js';
    document.head.appendChild(tScript);

    function startEditor() {
        const targetField = document.getElementById('id_content');
        if (!targetField) return;

        // Initialize TinyMCE directly onto Django's textarea
        tinymce.init({
            selector: '#id_content',
            height: '75vh',
            menubar: true,
            plugins: [
                'advlist', 'autolink', 'lists', 'link', 'image', 'charmap', 'preview',
                'anchor', 'searchreplace', 'visualblocks', 'code', 'fullscreen',
                'insertdatetime', 'media', 'table', 'wordcount', 'codesample'
            ],
            toolbar: 'undo redo | blocks | ' +
            'bold italic underline | alignleft aligncenter ' +
            'alignright alignjustify | bullist numlist | ' +
            'image media codesample code | fullscreen',
            
            // Advanced Image Options
            image_advtab: true,
            
            // CRITICAL: Tell the editor NOT to strip out iframes or script tags
            extended_valid_elements: 'iframe[src|width|height|name|align|frameborder|scrolling|allowfullscreen|allow],script[src|async|defer|type|charset]',
            
            content_style: 'body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 16px; }',
            
            // Ensure data syncs back to Django before saving
            setup: function (editor) {
                editor.on('change', function () {
                    editor.save();
                });
            }
        });
    }

    tScript.onload = () => {
        if (document.readyState === 'complete' || document.readyState === 'interactive') {
            startEditor();
        } else {
            window.addEventListener('load', startEditor);
        }
    };
})();
