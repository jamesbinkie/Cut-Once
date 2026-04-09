// Load Quill CSS and JS dynamically
const quillCss = document.createElement('link');
quillCss.rel = 'stylesheet';
quillCss.href = 'https://cdn.quilljs.com/1.3.6/quill.snow.css';
document.head.appendChild(quillCss);

const quillJs = document.createElement('script');
quillJs.src = 'https://cdn.quilljs.com/1.3.6/quill.js';
document.head.appendChild(quillJs);

document.addEventListener('DOMContentLoaded', function() {
    const textArea = document.querySelector('textarea[name="content_blocks"]');
    if (!textArea) return;

    textArea.style.display = 'none';
    const builderContainer = document.createElement('div');
    builderContainer.className = 'custom-builder-wrap';
    textArea.parentNode.insertBefore(builderContainer, textArea);

    function renderBlocks() {
        builderContainer.innerHTML = '';
        let blocks = JSON.parse(textArea.value || '[]');

        blocks.forEach((block, index) => {
            const wrapper = document.createElement('div');
            wrapper.className = 'block-editor-container';
            wrapper.style = "padding:15px; border:1px solid #ddd; margin-bottom:20px; border-radius:8px;";

            if (block.type === 'text') {
                wrapper.innerHTML = `
                    <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                        <strong style="color:#009FE3;">TEXT BOX (Rich Editor)</strong>
                        <button type="button" class="delete-block" data-index="${index}" style="color:red; border:none; background:none; cursor:pointer;">Remove</button>
                    </div>
                    <div id="editor-${index}" style="height: 200px;">${block.value}</div>
                `;
                
                builderContainer.appendChild(wrapper);

                // Initialize Quill for this block
                const quill = new Quill(`#editor-${index}`, {
                    theme: 'snow',
                    modules: {
                        toolbar: [
                            ['bold', 'italic', 'underline'],
                            [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                            ['link', 'clean']
                        ]
                    }
                });

                quill.on('text-change', function() {
                    blocks[index].value = quill.root.innerHTML;
                    textArea.value = JSON.stringify(blocks);
                });

            } else {
                // Image or Widget (Standard Input)
                wrapper.innerHTML = `
                    <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
                        <strong style="color:#009FE3;">${block.type.toUpperCase()} URL/CODE</strong>
                        <button type="button" class="delete-block" data-index="${index}" style="color:red; border:none; background:none; cursor:pointer;">Remove</button>
                    </div>
                    <input type="text" value="${block.value}" style="width:100%; padding:8px; border:1px solid #ccc; border-radius:4px;">
                `;
                builderContainer.appendChild(wrapper);

                wrapper.querySelector('input').addEventListener('input', (e) => {
                    blocks[index].value = e.target.value;
                    textArea.value = JSON.stringify(blocks);
                });
            }

            wrapper.querySelector('.delete-block').addEventListener('click', () => {
                blocks.splice(index, 1);
                textArea.value = JSON.stringify(blocks);
                renderBlocks();
            });
        });

        // "Add" Buttons
        const btnRow = document.createElement('div');
        btnRow.style = "margin-top:20px; display:flex; gap:10px;";
        btnRow.innerHTML = `
            <button type="button" class="add-blk" data-type="text" style="background:#009FE3; color:white; padding:10px 20px; border-radius:6px; border:none; cursor:pointer; font-weight:bold;">+ Add Rich Text</button>
            <button type="button" class="add-blk" data-type="image" style="background:#666; color:white; padding:10px 20px; border-radius:6px; border:none; cursor:pointer;">+ Add Image</button>
        `;

        btnRow.querySelectorAll('.add-blk').forEach(btn => {
            btn.addEventListener('click', () => {
                blocks.push({ type: btn.dataset.type, value: "" });
                textArea.value = JSON.stringify(blocks);
                renderBlocks();
            });
        });
        builderContainer.appendChild(btnRow);
    }

    // Wait for Quill to load from CDN before rendering
    quillJs.onload = renderBlocks;
});
