document.addEventListener("DOMContentLoaded", function () {
    console.log("Zabbix AI Agent: Initializing...");

    if (document.getElementById("zabbix-ai-agent-overlay")) return;

    // Create overlay iframe
    var iframe = document.createElement("iframe");
    iframe.id = "zabbix-ai-agent-overlay";
    iframe.src = "/ai-backend/app/index.html";
    iframe.style.position = "fixed";
    iframe.style.width = "100px";
    iframe.style.height = "100px";
    iframe.style.bottom = "0";
    iframe.style.right = "0";
    iframe.style.border = "none";
    iframe.style.zIndex = "99999";
    iframe.allow = "microphone";

    document.body.appendChild(iframe);

    // Listen for resize requests
    window.addEventListener("message", function (e) {
        if (e.data && e.data.type === "zabbix-agent-resize") {
            if (e.data.expanded) {
                iframe.style.width = "450px";
                iframe.style.height = "700px";
            } else {
                iframe.style.width = "100px";
                iframe.style.height = "100px";
            }
        }
    });

    // === CONTEXTUAL MENU INTEGRATION ===

    // Create AI context menu
    var aiContextMenu = document.createElement("div");
    aiContextMenu.id = "ai-context-menu";
    aiContextMenu.style.cssText = `
        position: fixed;
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 8px;
        padding: 8px 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        z-index: 100000;
        display: none;
        min-width: 200px;
    `;

    var menuItem = document.createElement("div");
    menuItem.style.cssText = `
        padding: 10px 16px;
        cursor: pointer;
        color: #cbd5e1;
        font-size: 14px;
        transition: background 0.2s;
        display: flex;
        align-items: center;
        gap: 8px;
    `;
    menuItem.innerHTML = '<span style="font-size: 18px;">🤖</span> Analizar con IA';

    menuItem.addEventListener('mouseenter', function () {
        this.style.background = '#334155';
    });

    menuItem.addEventListener('mouseleave', function () {
        this.style.background = 'transparent';
    });

    aiContextMenu.appendChild(menuItem);
    document.body.appendChild(aiContextMenu);

    console.log("Zabbix AI Agent: Context menu created");

    // Track what element was right-clicked
    var contextData = null;

    // Detect right-clicks ANYWHERE - simplified approach
    document.addEventListener('contextmenu', function (e) {
        console.log("Right click detected at:", e.target);

        // Find the closest table row
        var row = e.target.closest('tr');

        if (row) {
            console.log("Row found:", row);

            // Get all text from the row for context
            var rowText = row.innerText || row.textContent;
            console.log("Row text:", rowText);

            // Check if this looks like a Zabbix data row (has multiple cells)
            var cells = row.querySelectorAll('td');
            if (cells.length > 1) {
                // This is likely a data row, show our menu
                e.preventDefault();
                e.stopPropagation();

                contextData = {
                    text: rowText,
                    html: row.innerHTML
                };

                // Position menu at cursor
                aiContextMenu.style.left = e.pageX + 'px';
                aiContextMenu.style.top = e.pageY + 'px';
                aiContextMenu.style.display = 'block';

                console.log("Showing AI menu with data:", contextData);
                return false;
            }
        }

        // Hide menu if  click is not on a valid row
        aiContextMenu.style.display = 'none';
    }, true); // Use capture phase

    // Hide menu on regular click
    document.addEventListener('click', function () {
        aiContextMenu.style.display = 'none';
    });

    // Handle AI analysis
    menuItem.addEventListener('click', function (e) {
        e.stopPropagation();

        if (!contextData) {
            console.log("No context data available");
            return;
        }

        console.log("Analyzing context:", contextData);

        var message = "Analiza esta información de Zabbix: " + contextData.text;

        // Send message to AI iframe
        iframe.contentWindow.postMessage({
            type: 'analyze-context',
            contextType: 'generic',
            data: { name: contextData.text, type: 'zabbix_row' }
        }, '*');

        // Open the chat
        window.postMessage({ type: 'zabbix-agent-resize', expanded: true }, '*');

        aiContextMenu.style.display = 'none';
        contextData = null;
    });

    console.log("Zabbix AI Agent: Fully initialized");
});
