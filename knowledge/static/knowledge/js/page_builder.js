
document.addEventListener('DOMContentLoaded', function() {
    // Find the JSON textarea in the Django admin
    const textArea = document.querySelector('textarea[name="content_blocks"]');
    if (!textArea) return;

    // Hide the raw textarea
    textArea.style.display = 'none';

    // Create a container for our visual builder
    const builderContainer = document.createElement('div');
    builderContainer.className = 'custom-builder-wrap';
    textArea.parentNode.insertBefore(builderContainer, textArea);

    function renderBlocks() {
        builderContainer.innerHTML = '';
        let blocks = [];
        try {
            blocks = JSON.parse(textArea.value || '[]');
        } catch (e) { blocks = []; }

        blocks.forEach((block, index) => {
            const div = document.createElement('div');
            div.style = "background:#f9f9f9; border:1px solid #ddd; padding:15px; margin-bottom:10px; border-radius:8px; position:relative;";
            
            div.innerHTML = `
                <strong style="display:block; margin-bottom:5px; color:#009FE3;">${block.type.toUpperCase()} BLOCK</strong>
                <textarea style="width:100%; height:80px;">${block.value}</textarea>
                <button type="button" class="delete-block" data-index="${index}" style="color:red; cursor:pointer; margin-top:5px; border:none; background:none; text-decoration:underline;">Remove Block</button>
            `;

            div.querySelector('textarea').addEventListener('input', (e) => {
                blocks[index].value = e.target.value;
                textArea.value = JSON.stringify(blocks);
            });

            div.querySelector('.delete-block').addEventListener('click', () => {
                blocks.splice(index, 1);
                textArea.value = JSON.stringify(blocks);
                renderBlocks();
            });

            builderContainer.appendChild(div);
        });

        // Add Button Row
        const btnRow = document.createElement('div');
        btnRow.innerHTML = `
            <button type="button" class="add-blk" data-type="text" style="background:#009FE3; color:white; padding:5px 15px; border-radius:4px; border:none; margin-right:5px; cursor:pointer;">+ Add Text Box</button>
            <button type="button" class="add-blk" data-type="image" style="background:#009FE3; color:white; padding:5px 15px; border-radius:4px; border:none; margin-right:5px; cursor:pointer;">+ Add Image URL</button>
            <button type="button" class="add-blk" data-type="widget" style="background:#009FE3; color:white; padding:5px 15px; border-radius:4px; border:none; cursor:pointer;">+ Add HTML Widget</button>
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

    renderBlocks();
});
