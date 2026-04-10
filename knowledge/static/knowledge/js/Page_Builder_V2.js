(function() {
    // 1. Load GrapesJS Styles
    const gCss = document.createElement('link');
    gCss.rel = 'stylesheet'; 
    gCss.href = 'https://unpkg.com/grapesjs/dist/css/grapes.min.css';
    document.head.appendChild(gCss);

    // 2. Load GrapesJS Core
    const gJs = document.createElement('script');
    gJs.src = 'https://unpkg.com/grapesjs';
    document.head.appendChild(gJs);
    
    // 3. Load the Drag-and-Drop Webpage Blocks
    const gPreset = document.createElement('script');
    gPreset.src = 'https://unpkg.com/grapesjs-preset-webpage@1.0.2';
    document.head.appendChild(gPreset);

    function startBuilder() {
        const targetField = document.getElementById('id_content');
        if (!targetField) return;

        // Hide Django's default text area
        targetField.style.display = 'none';

        if (document.getElementById('gjs')) return;

        // Create the canvas for the drag-and-drop builder
        const container = document.createElement('div');
        container.id = 'gjs';
        container.style.border = '1px solid #444';
        
        // Load any existing article content into the canvas
        container.innerHTML = targetField.value;
        targetField.parentNode.insertBefore(container, targetField);

        // Initialize GrapesJS
        const editor = grapesjs.init({
            container: '#gjs',
            fromElement: true,     // Convert existing HTML into draggable blocks
            height: '75vh',
            width: '100%',
            plugins: ['gjs-preset-webpage'],
            storageManager: false, // We will use Django's database to save, not local storage
        });

        // Every time you drag, drop, or type, sync the code back to Django
        editor.on('change:changesCount', () => {
            const html = editor.getHtml();
            const css = editor.getCss();
            // Combine the styling and the structure so Django saves both!
            targetField.value = `<style>${css}</style>\n${html}`;
        });
    }

    // Wait for the heavy builder scripts to load before starting
    let scriptsLoaded = 0;
    function checkLoad() {
        scriptsLoaded++;
        if (scriptsLoaded === 2) { 
            if (document.readyState === 'complete' || document.readyState === 'interactive') {
                startBuilder();
            } else {
                window.addEventListener('load', startBuilder);
            }
        }
    }

    gJs.onload = checkLoad;
    gPreset.onload = checkLoad;
})();
