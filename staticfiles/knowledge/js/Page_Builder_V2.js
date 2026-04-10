(function() {
    // 1. Load the Editor Script
    const tScript = document.createElement('script');
    tScript.src = 'https://cdnjs.cloudflare.com/ajax/libs/tinymce/6.8.3/tinymce.min.js';
    document.head.appendChild(tScript);

    function startEditor() {
        const targetField = document.getElementById('id_content');
        if (!targetField) return;

        // Initialize the simple Google Docs style editor
        tinymce.init({
            selector: '#id_content',
            height: '80vh',
            menubar: false, // Hide complex top menus
            plugins: 'lists link image media table code wordcount',
            
            // Clean, straightforward toolbar
            toolbar: 'blocks | bold italic | alignleft aligncenter alignright | bullist numlist | table image media link | removeformat | code',
            
            // Style the editor area to look exactly like a Google Doc (white paper, gray background)
            content_style: `
                html { 
                    background-color: #f3f4f6 !important; 
                }
                body { 
                    font-family: 'Open Sans', Arial, sans-serif; 
                    font-size: 16px; 
                    color: #333;
                    max-width: 850px; 
                    margin: 20px auto !important; 
                    padding: 40px !important; 
                    box-shadow: 0 1px 3px rgba(0,0,0,0.12), 0 1px 2px rgba(0,0,0,0.24); 
                    background-color: white !important;
                    min-height: 800px;
                }
                img { max-width: 100%; height: auto; }
                table { border-collapse: collapse; width: 100%; }
                table, th, td { border: 1px solid #ccc; padding: 8px; }
            `,
            // Sync content back to Django before saving
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
