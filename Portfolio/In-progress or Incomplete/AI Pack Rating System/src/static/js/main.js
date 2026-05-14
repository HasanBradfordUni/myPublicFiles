// Popular packs array - hardcoded for quick access
const popularPacks = [
    '85+ x10 Players Pack',
    '10 Coins Energizer Pack', 
    '100 Players Pack',
    '77+ X5 Rare Gold Players Pack',
    '80+ X5 Players Pack',
    '81+ X11 Players Pack',
    '81+ X2 Rare Gold Players Pack',
    '82+ X10 Rare Gold Players Pack', 
    '82+ x100 Rare Gold Players Pack', 
    '82+ x11 EFIGS Pack',
    '82+ X2 Rare Gold Players Pack',
    '83+ x10 Rare Gold Players Pack', 
    '83+ x100 Pack',
    '83+ X2 Rare Gold Players Pack',
    '84+ X7 Rare Gold Players Pack',
    '84+ x10 Rare Gold Players Pack',
    '84+ X2 Rare Gold Players Pack',
    '84+ X5 Rare Gold Players Pack',
    '83+ X3 Rare Gold Players Pack',
    '85+ X2 Rare Gold Players Pack',
    '85+ X5 Rare Gold Players Pack',
    '86+ X2 Rare Gold Players Pack',
    '87+ X2 Rare Gold Players Pack',
    '85+ X3 Rare Gold Players Pack',
    '86+ X3 Rare Gold Players Pack',
    '88+ X2 Rare Gold Players Pack',
    '86+ X5 Rare Gold Players Pack',
    '87+ X3 Rare Gold Players Pack',
    '85+ X7 Rare Gold Players Pack',
    'Premium Gold Pack',
    'Ultimate Pack',
    'Rare Mega Pack', 
    'Mega Pack',
    'Jumbo Premium Gold Pack',
    'Prime Gold Players Pack',
    'Rare Gold Pack',
];

// Function to fetch and populate pack types
async function populatePackTypes() {
    try {
        const response = await fetch('/static/packNames.txt');
        const text = await response.text();
        const packNames = text.split(',').map(name => name.trim()).filter(name => name);
        
        // Group pack names by first character
        const groupedPacks = {};
        packNames.forEach(pack => {
            const firstChar = pack.charAt(0).toUpperCase();
            if (!groupedPacks[firstChar]) {
                groupedPacks[firstChar] = [];
            }
            groupedPacks[firstChar].push(pack);
        });
        
        // Sort groups alphabetically
        const sortedKeys = Object.keys(groupedPacks).sort();
        
        const selectElement = document.getElementById('pack-type');
        
        // Clear existing options except the first placeholder
        selectElement.innerHTML = '<option value="">--Select Pack Type--</option>';
        
        // Add popular packs section first
        if (popularPacks.length > 0) {
            const popularOptgroup = document.createElement('optgroup');
            popularOptgroup.label = '🔥 Popular Packs';
            
            popularPacks.forEach(pack => {
                const option = document.createElement('option');
                option.value = pack.toLowerCase().replace(/\s+/g, '-');
                option.textContent = pack;
                popularOptgroup.appendChild(option);
            });
            
            selectElement.appendChild(popularOptgroup);
        }
        
        // Add separator or "All Packs" section
        const allPacksOptgroup = document.createElement('optgroup');
        allPacksOptgroup.label = '📦 All Packs';
        selectElement.appendChild(allPacksOptgroup);
        
        // Add options grouped by first character
        sortedKeys.forEach(key => {
            // Create optgroup for each letter/number
            const optgroup = document.createElement('optgroup');
            optgroup.label = key;
            
            // Sort packs within each group
            groupedPacks[key].sort().forEach(pack => {
                const option = document.createElement('option');
                option.value = pack.toLowerCase().replace(/\s+/g, '-');
                option.textContent = pack;
                optgroup.appendChild(option);
            });
            
            selectElement.appendChild(optgroup);
        });
        
    } catch (error) {
        console.error('Error loading pack names:', error);
        // Fallback to basic options if file loading fails
        const fallbackPacks = ['Standard Pack', 'Rare Pack', 'Mega Pack', 'Ultimate Pack'];
        const selectElement = document.getElementById('pack-type');
        
        // Add popular packs even in fallback
        if (popularPacks.length > 0) {
            const popularOptgroup = document.createElement('optgroup');
            popularOptgroup.label = '🔥 Popular Packs';
            
            popularPacks.forEach(pack => {
                const option = document.createElement('option');
                option.value = pack.toLowerCase().replace(/\s+/g, '-');
                option.textContent = pack;
                popularOptgroup.appendChild(option);
            });
            
            selectElement.appendChild(popularOptgroup);
        }
        
        // Add fallback packs
        const fallbackOptgroup = document.createElement('optgroup');
        fallbackOptgroup.label = 'Basic Packs';
        
        fallbackPacks.forEach(pack => {
            const option = document.createElement('option');
            option.value = pack.toLowerCase().replace(/\s+/g, '-');
            option.textContent = pack;
            fallbackOptgroup.appendChild(option);
        });
        
        selectElement.appendChild(fallbackOptgroup);
    }
}

// Add form submission handler
document.getElementById('upload-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const formData = new FormData();
    const packType = document.getElementById('pack-type').value;
    const files = document.getElementById('image-upload').files;
    
    if (!packType || files.length === 0) {
        alert('Please select a pack type and upload at least one image.');
        return;
    }
    
    // Add pack type to form data
    formData.append('pack-type', packType);
    
    // Add all selected files
    for (let file of files) {
        formData.append('image-upload', file);
    }
    
    // Show loading message
    const resultDiv = document.getElementById('result');
    resultDiv.innerHTML = '<p>Analyzing your pack... This may take a few moments.</p>';
    
    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.error) {
            resultDiv.innerHTML = `<p style="color: red;">Error: ${data.error}</p>`;
            return;
        }
        
        // Display results
        let html = `
            <h3>Pack Analysis Results</h3>
            <div class="results-summary">
                <p><strong>Pack Type:</strong> ${data.pack_type || 'Unknown'}</p>
                <p><strong>Players Found:</strong> ${data.total_players || 0}</p>
                <p><strong>Average Rating:</strong> ${data.average_rating || 'N/A'}</p>
                <p><strong>Pack Value:</strong> ${(data.pack_value || 0).toLocaleString()} coins</p>
                <p><strong>Pack Rating:</strong> ${data.pack_rating || 0}/100</p>
            </div>
            <h4>Players Detected:</h4>
        `;
        
        if (data.players && data.players.length > 0) {
            html += '<div class="players-list">';
            data.players.forEach(player => {
                const playerName = player.name || 'Unknown Player';
                const playerRating = player.rating || 'N/A';
                const cardType = player.card_type || 'Unknown';
                const playerPrice = player.price ? player.price.toLocaleString() + ' coins' : 'Price unavailable';
                const priceSource = player.price_source === 'futbin' ? '📊' : '📈';
                
                html += `
                    <div class="player-card">
                        <div class="player-info">
                            <span class="player-name">${playerName}</span>
                            <span class="player-rating">${playerRating} OVR</span>
                            <span class="card-type">(${cardType})</span>
                        </div>
                        <div class="player-price">
                            <span class="price">${playerPrice}</span>
                            <span class="price-source">${priceSource}</span>
                        </div>
                    </div>
                `;
            });
            html += '</div>';
        } else {
            html += '<p>No players detected in the uploaded images.</p>';
        }
        
        resultDiv.innerHTML = html;
        
    } catch (error) {
        resultDiv.innerHTML = `<p style="color: red;">Error: ${error.message}</p>`;
    }
});

// Call the function when the page loads
document.addEventListener('DOMContentLoaded', populatePackTypes);