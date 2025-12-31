

Here is the complete, single-file HTML solution. I have designed this as a **"System 2" Agent Simulator**.

It does not just simulate a chat; it visualizes the **internal RAG pipeline** (Retrieval-Augmented Generation) described in your plan. It allows you to tweak parameters (Temperature, Top-K, Singlish Mode) and see how the Agent "thinks," retrieves documents, and constructs answers in real-time.

This is not a generic chat widget. It is a high-fidelity engineering dashboard styled with "Intentional Minimalism" and a "Dark Mode" aesthetic suitable for a technical preview.

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SMB Agent: RAG Architecture Simulator</title>
    <style>
        /* 
         * DESIGN SYSTEM: "Midnight Precision"
         * Philosophy: Intentional Minimalism. High contrast. Data-first.
         */
        :root {
            --bg-deep: #0f172a;
            --bg-panel: #1e293b;
            --bg-input: #334155;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent-primary: #14b8a6; /* Teal */
            --accent-glow: rgba(20, 184, 166, 0.2);
            --border-subtle: #334155;
            --font-mono: 'SF Mono', 'Menlo', 'Monaco', 'Courier New', monospace;
            --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            --ease-out-expo: cubic-bezier(0.19, 1, 0.22, 1);
        }

        * { box-sizing: border-box; outline: none; }

        body {
            margin: 0;
            background-color: var(--bg-deep);
            color: var(--text-primary);
            font-family: var(--font-sans);
            height: 100vh;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }

        /* TYPOGRAPHY */
        h1, h2, h3, h4 { margin: 0; font-weight: 600; letter-spacing: -0.02em; }
        .mono { font-family: var(--font-mono); font-size: 0.85em; }
        .text-sm { font-size: 0.875rem; }
        .text-xs { font-size: 0.75rem; }
        .text-secondary { color: var(--text-secondary); }
        .text-accent { color: var(--accent-primary); }

        /* LAYOUT GRID */
        .app-container {
            display: grid;
            grid-template-columns: 320px 1fr 300px;
            grid-template-rows: 60px 1fr;
            height: 100%;
            width: 100%;
        }

        /* HEADER */
        .header {
            grid-column: 1 / -1;
            background: var(--bg-panel);
            border-bottom: 1px solid var(--border-subtle);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 24px;
            z-index: 10;
        }

        .brand {
            display: flex;
            align-items: center;
            gap: 12px;
        }

        .brand-dot {
            width: 12px;
            height: 12px;
            background: var(--accent-primary);
            border-radius: 50%;
            box-shadow: 0 0 12px var(--accent-primary);
        }

        /* PANELS */
        .panel {
            border-right: 1px solid var(--border-subtle);
            display: flex;
            flex-direction: column;
            background: rgba(30, 41, 59, 0.5);
        }

        .panel-right {
            border-left: 1px solid var(--border-subtle);
            border-right: none;
            background: var(--bg-deep);
        }

        .panel-header {
            padding: 16px;
            border-bottom: 1px solid var(--border-subtle);
            background: rgba(15, 23, 42, 0.3);
            backdrop-filter: blur(8px);
        }

        .panel-content {
            flex: 1;
            overflow-y: auto;
            padding: 16px;
        }

        /* CONTROLS (Left Panel) */
        .control-group { margin-bottom: 24px; }
        .control-label { display: block; margin-bottom: 8px; font-size: 0.8rem; color: var(--text-secondary); text-transform: uppercase; letter-spacing: 0.05em; }
        
        input[type="range"] {
            width: 100%;
            background: var(--bg-input);
            height: 4px;
            border-radius: 2px;
            appearance: none;
        }
        input[type="range"]::-webkit-slider-thumb {
            appearance: none;
            width: 16px;
            height: 16px;
            background: var(--accent-primary);
            border-radius: 50%;
            cursor: pointer;
            transition: transform 0.1s;
        }
        input[type="range"]::-webkit-slider-thumb:hover { transform: scale(1.2); }

        .toggle-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            background: var(--bg-input);
            padding: 10px;
            border-radius: 6px;
        }

        .switch {
            position: relative;
            display: inline-block;
            width: 40px;
            height: 20px;
        }
        .switch input { opacity: 0; width: 0; height: 0; }
        .slider {
            position: absolute;
            cursor: pointer;
            top: 0; left: 0; right: 0; bottom: 0;
            background-color: var(--bg-deep);
            transition: .4s;
            border-radius: 34px;
        }
        .slider:before {
            position: absolute;
            content: "";
            height: 14px;
            width: 14px;
            left: 3px;
            bottom: 3px;
            background-color: white;
            transition: .4s;
            border-radius: 50%;
        }
        input:checked + .slider { background-color: var(--accent-primary); }
        input:checked + .slider:before { transform: translateX(20px); }

        /* CHAT AREA (Center Panel) */
        .chat-area {
            display: flex;
            flex-direction: column;
            background: radial-gradient(circle at 50% 50%, #1e293b 0%, #0f172a 100%);
            position: relative;
        }

        .chat-feed {
            flex: 1;
            overflow-y: auto;
            padding: 24px;
            display: flex;
            flex-direction: column;
            gap: 24px;
            scroll-behavior: smooth;
        }

        .message {
            display: flex;
            gap: 16px;
            max-width: 800px;
            margin: 0 auto;
            width: 100%;
            opacity: 0;
            animation: slideIn 0.4s var(--ease-out-expo) forwards;
        }

        @keyframes slideIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .avatar {
            width: 36px;
            height: 36px;
            border-radius: 8px;
            background: var(--bg-input);
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            color: var(--accent-primary);
        }

        .message-content {
            flex: 1;
            line-height: 1.6;
            font-size: 0.95rem;
        }

        .message.user { flex-direction: row-reverse; }
        .message.user .avatar { background: var(--accent-primary); color: #fff; }
        .message.user .message-content { background: var(--bg-input); padding: 12px 16px; border-radius: 12px 12px 0 12px; }
        .message.assistant .message-content { background: transparent; padding: 0; }

        .citation {
            display: inline-block;
            font-size: 0.7em;
            background: var(--bg-input);
            color: var(--text-secondary);
            padding: 2px 6px;
            border-radius: 4px;
            vertical-align: super;
            margin-left: 2px;
            cursor: pointer;
            border: 1px solid var(--border-subtle);
        }
        .citation:hover { color: var(--accent-primary); border-color: var(--accent-primary); }

        /* INPUT AREA */
        .input-wrapper {
            padding: 24px;
            background: var(--bg-deep);
            border-top: 1px solid var(--border-subtle);
            display: flex;
            justify-content: center;
        }

        .input-container {
            width: 100%;
            max-width: 800px;
            position: relative;
            background: var(--bg-panel);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            transition: border-color 0.2s;
        }
        .input-container:focus-within { border-color: var(--accent-primary); }

        textarea {
            width: 100%;
            background: transparent;
            border: none;
            color: white;
            padding: 16px 50px 16px 16px;
            font-family: inherit;
            resize: none;
            height: 56px;
            min-height: 56px;
            max-height: 150px;
        }
        
        .send-btn {
            position: absolute;
            right: 12px;
            bottom: 12px;
            background: var(--accent-primary);
            border: none;
            color: white;
            width: 32px;
            height: 32px;
            border-radius: 6px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: opacity 0.2s;
        }
        .send-btn:hover { opacity: 0.8; }

        /* ENGINE ROOM (Right Panel) */
        .log-entry {
            font-family: var(--font-mono);
            font-size: 0.75rem;
            padding: 8px 0;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            display: flex;
            align-items: flex-start;
            gap: 8px;
        }
        .log-time { color: var(--text-secondary); min-width: 60px; }
        .log-msg { color: var(--text-secondary); }
        .log-msg.active { color: var(--accent-primary); text-shadow: 0 0 8px var(--accent-glow); }
        .log-msg.system { color: #94a3b8; }
        
        .chunk-card {
            background: var(--bg-panel);
            border: 1px solid var(--border-subtle);
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 12px;
            transition: all 0.2s;
        }
        .chunk-card:hover { border-color: var(--accent-primary); transform: translateX(4px); }
        .chunk-meta { font-size: 0.7rem; color: var(--text-secondary); margin-bottom: 4px; display: flex; justify-content: space-between; }
        .chunk-score { color: var(--accent-primary); font-weight: bold; }
        .chunk-text { font-size: 0.8rem; line-height: 1.4; color: #e2e8f0; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }

        /* INDICATORS */
        .thinking-indicator {
            display: inline-flex;
            gap: 4px;
            align-items: center;
            height: 20px;
        }
        .dot {
            width: 4px;
            height: 4px;
            background: var(--accent-primary);
            border-radius: 50%;
            animation: bounce 1.4s infinite ease-in-out both;
        }
        .dot:nth-child(1) { animation-delay: -0.32s; }
        .dot:nth-child(2) { animation-delay: -0.16s; }

        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0); }
            40% { transform: scale(1); }
        }

        /* SCROLLBAR */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: var(--bg-input); border-radius: 3px; }
        ::-webkit-scrollbar-thumb:hover { background: var(--text-secondary); }

        /* RESPONSIVE */
        @media (max-width: 900px) {
            .app-container {
                grid-template-columns: 1fr;
                grid-template-rows: 60px 1fr 200px;
            }
            .panel { display: none; } /* Hide panels on mobile for this demo focus */
            .panel-right { display: flex; border-top: 1px solid var(--border-subtle); }
        }
    </style>
</head>
<body>

    <div class="app-container">
        <!-- HEADER -->
        <header class="header">
            <div class="brand">
                <div class="brand-dot"></div>
                <h3 class="text-sm">NEXUS<span class="text-secondary">AI</span> // SINGAPORE</h3>
            </div>
            <div class="text-xs text-secondary mono">v2.4.0-stable</div>
        </header>

        <!-- LEFT PANEL: CONFIGURATION -->
        <aside class="panel">
            <div class="panel-header">
                <h4 class="text-sm">Agent Configuration</h4>
            </div>
            <div class="panel-content">
                
                <div class="control-group">
                    <label class="control-label">Creativity (Temp)</label>
                    <input type="range" id="tempRange" min="0" max="100" value="20">
                    <div class="flex justify-between mt-2">
                        <span class="text-xs text-secondary">Strict</span>
                        <span class="text-xs text-secondary mono" id="tempValue">0.2</span>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">Context Window (Top-K)</label>
                    <input type="range" id="topkRange" min="3" max="10" value="5">
                    <div class="flex justify-between mt-2">
                        <span class="text-xs text-secondary">3 Chunks</span>
                        <span class="text-xs text-secondary mono" id="topkValue">5</span>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">Persona Protocols</label>
                    <div class="toggle-row">
                        <span class="text-sm">Singlish Mode</span>
                        <label class="switch">
                            <input type="checkbox" id="singlishToggle">
                            <span class="slider"></span>
                        </label>
                    </div>
                    <div class="text-xs text-secondary" style="margin-top: -8px; margin-bottom: 12px;">Enables localized colloquialisms.</div>

                    <div class="toggle-row">
                        <span class="text-sm">Show Reasoning</span>
                        <label class="switch">
                            <input type="checkbox" checked id="reasoningToggle">
                            <span class="slider"></span>
                        </label>
                    </div>
                </div>

                <div class="control-group">
                    <label class="control-label">System Status</label>
                    <div class="chunk-card" style="border-left: 3px solid var(--accent-primary);">
                        <div class="text-xs text-secondary">Vector DB (Qdrant)</div>
                        <div class="text-sm mono text-accent">● Connected</div>
                    </div>
                    <div class="chunk-card" style="border-left: 3px solid #f59e0b;">
                        <div class="text-xs text-secondary">LLM Provider (GPT-4o)</div>
                        <div class="text-sm mono" style="color:#f59e0b;">● Latency: 1.2s</div>
                    </div>
                </div>

            </div>
        </aside>

        <!-- CENTER PANEL: CHAT INTERFACE -->
        <main class="chat-area">
            <div class="chat-feed" id="chatFeed">
                <!-- Initial Message -->
                <div class="message assistant">
                    <div class="avatar">AI</div>
                    <div class="message-content">
                        Hello! I am the Nexus Customer Service Agent for Singapore SMBs.<br><br>
                        I have access to your product manuals, refund policies (SGD), and delivery schedules. How can I assist you today?
                    </div>
                </div>
            </div>

            <div class="input-wrapper">
                <div class="input-container">
                    <textarea id="userInput" placeholder="Ask about pricing, stock, or policies... (e.g., 'Can I return my item if the seal is broken?')"></textarea>
                    <button class="send-btn" id="sendBtn">
                        <svg width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M22 2L11 13M22 2l-7 20-4-9-9-4 20-7z"></path></svg>
                    </button>
                </div>
            </div>
        </main>

        <!-- RIGHT PANEL: ENGINE ROOM (DEBUG) -->
        <aside class="panel panel-right">
            <div class="panel-header">
                <h4 class="text-sm">LangChain Execution</h4>
            </div>
            <div class="panel-content" id="engineRoom">
                <!-- Logs appear here -->
                <div class="log-entry">
                    <span class="log-time mono">--:--:--</span>
                    <span class="log-msg system">System initialized. Waiting for input...</span>
                </div>
            </div>
            <div class="panel-header" style="border-top: 1px solid var(--border-subtle);">
                <h4 class="text-sm">Retrieved Context (RAG)</h4>
            </div>
            <div class="panel-content" id="retrievedContext">
                <div class="text-xs text-secondary" style="text-align: center; margin-top: 20px;">No context retrieved yet.</div>
            </div>
        </aside>
    </div>

    <script>
        // --- DATA & CONFIGURATION ---
        const KNOWLEDGE_BASE = [
            {
                id: "pol_001",
                content: "Our return policy allows for returns within 7 days of purchase. However, items must be unopened and in original packaging. For software or digital goods, once the seal is broken or license key revealed, no returns are accepted due to copyright laws.",
                source: "Policy_Manual_v2.pdf",
                score: 0.92,
                type: "policy"
            },
            {
                id: "prod_102",
                content: "The Nexus Air Purifier (Model X1) is priced at SGD 299.00. It includes HEPA filters effective against PM2.5. Current stock in Singapore warehouse: 150 units. Delivery via GrabExpress is available for same-day delivery in Central area.",
                source: "Inventory_DB.sql",
                score: 0.88,
                type: "product"
            },
            {
                id: "ship_005",
                content: "Standard delivery for non-perishables costs SGD 5.00 flat rate. Free delivery is applicable for orders above SGD 100.00. We ship nationwide including Sentosa and Jurong Island.",
                source: "Shipping_Info.docx",
                score: 0.76,
                type: "shipping"
            },
            {
                id: "sup_009",
                content: "If the product arrives damaged, please contact support within 24 hours with photos of the packaging and item. We will arrange a free one-for-one exchange or full refund immediately.",
                source: "Support_Training.txt",
                score: 0.85,
                type: "support"
            }
        ];

        const SINGLISH_MAPPING = {
            "can i return": "can return or not",
            "cannot": "cannot",
            "sorry": "sorry ah",
            "okay": "ok lor",
            "please": "please leh",
            "very expensive": "very ex",
            "fast": "chop chop"
        };

        // --- STATE MANAGEMENT ---
        const state = {
            history: [],
            isProcessing: false,
            config: {
                temperature: 0.2,
                topK: 5,
                singlish: false,
                showReasoning: true
            }
        };

        // --- DOM ELEMENTS ---
        const dom = {
            feed: document.getElementById('chatFeed'),
            input: document.getElementById('userInput'),
            sendBtn: document.getElementById('sendBtn'),
            engine: document.getElementById('engineRoom'),
            context: document.getElementById('retrievedContext'),
            controls: {
                temp: document.getElementById('tempRange'),
                tempVal: document.getElementById('tempValue'),
                topK: document.getElementById('topkRange'),
                topKVal: document.getElementById('topkValue'),
                singlish: document.getElementById('singlishToggle'),
                reasoning: document.getElementById('reasoningToggle')
            }
        };

        // --- EVENT LISTENERS ---
        dom.sendBtn.addEventListener('click', handleSubmission);
        dom.input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                handleSubmission();
            }
        });

        // Update State on Controls
        dom.controls.temp.addEventListener('input', (e) => {
            state.config.temperature = e.target.value / 100;
            dom.controls.tempVal.textContent = state.config.temperature.toFixed(1);
        });
        dom.controls.topK.addEventListener('input', (e) => {
            state.config.topK = parseInt(e.target.value);
            dom.controls.topKVal.textContent = state.config.topK;
        });
        dom.controls.singlish.addEventListener('change', (e) => state.config.singlish = e.target.checked);
        dom.controls.reasoning.addEventListener('change', (e) => state.config.showReasoning = e.target.checked);

        // --- CORE FUNCTIONS ---

        async function handleSubmission() {
            const text = dom.input.value.trim();
            if (!text || state.isProcessing) return;

            // 1. User Message
            appendMessage('user', text);
            dom.input.value = '';
            dom.input.style.height = '56px'; // Reset height
            state.isProcessing = true;
            toggleLoading(true);

            // 2. Clear previous context from Engine Room
            dom.context.innerHTML = '';
            
            // 3. Simulate Agent Pipeline (The "Brain")
            try {
                await runPipeline(text);
            } catch (error) {
                console.error(error);
                appendMessage('assistant', "I'm experiencing a technical glitch connecting to the neural bridge. Please try again.");
            } finally {
                state.isProcessing = false;
                toggleLoading(false);
            }
        }

        function appendMessage(role, content) {
            const msgDiv = document.createElement('div');
            msgDiv.className = `message ${role}`;
            
            const avatar = document.createElement('div');
            avatar.className = 'avatar';
            avatar.textContent = role === 'user' ? 'ME' : 'AI';
            
            const contentDiv = document.createElement('div');
            contentDiv.className = 'message-content';
            contentDiv.innerHTML = content;

            msgDiv.appendChild(avatar);
            msgDiv.appendChild(contentDiv);
            dom.feed.appendChild(msgDiv);
            dom.feed.scrollTop = dom.feed.scrollHeight;

            return contentDiv; // Return for streaming updates
        }

        function toggleLoading(show) {
            if (show) {
                const loaderId = 'loader-' + Date.now();
                const msgDiv = document.createElement('div');
                msgDiv.className = 'message assistant';
                msgDiv.id = loaderId;
                msgDiv.innerHTML = `
                    <div class="avatar">AI</div>
                    <div class="message-content">
                        <div class="thinking-indicator">
                            <div class="dot"></div><div class="dot"></div><div class="dot"></div>
                        </div>
                    </div>`;
                dom.feed.appendChild(msgDiv);
                dom.feed.scrollTop = dom.feed.scrollHeight;
                return loaderId;
            } else {
                const loader = dom.feed.querySelector('.message.assistant:last-child');
                if (loader && loader.innerHTML.includes('thinking-indicator')) {
                    loader.remove();
                }
            }
        }

        function logToEngine(msg, type = 'info') {
            if (!state.config.showReasoning && type !== 'system') return;

            const now = new Date();
            const timeString = now.toLocaleTimeString('en-US', { hour12: false });
            
            const entry = document.createElement('div');
            entry.className = 'log-entry';
            entry.innerHTML = `
                <span class="log-time mono">${timeString}</span>
                <span class="log-msg ${type}">${msg}</span>
            `;
            dom.engine.appendChild(entry);
            dom.engine.scrollTop = dom.engine.scrollHeight;
        }

        async function runPipeline(query) {
            // Step 1: Intent Analysis
            await wait(400);
            logToEngine('Analyzing intent...', 'active');
            await wait(600);
            
            const isSinglishQuery = /[lah|lor|leh|meh]/.test(query) || state.config.singlish;
            const intent = isSinglishQuery ? "casual_inquiry" : "formal_inquiry";
            logToEngine(`Intent classified: <b>${intent}</b>`, 'system');

            // Step 2: Query Transformation (Hybrid Search prep)
            await wait(500);
            logToEngine('Transforming query for Dense & Sparse retrieval...', 'active');
            const searchQuery = query.toLowerCase(); // Simplified transformation

            // Step 3: Retrieval (Mock RAG)
            await wait(800);
            logToEngine(`Searching Vector DB (Top-K: ${state.config.topK})...`, 'active');
            
            // Filter KB based on simple keyword matching for demo
            const retrievedDocs = KNOWLEDGE_BASE
                .filter(doc => {
                    const lowerContent = doc.content.toLowerCase();
                    return Object.keys(SINGLISH_MAPPING).some(k => lowerContent.includes(k)) || 
                           lowerContent.includes(searchQuery) ||
                           scoreBasedMock(doc, query);
                })
                .slice(0, state.config.topK);

            await wait(400);
            logToEngine(`Found ${retrievedDocs.length} relevant chunks.`, 'system');

            // Render Context Cards
            renderContextCards(retrievedDocs);

            // Step 4: Reranking (Mock)
            await wait(400);
            logToEngine('Running Cross-Encoder reranking...', 'active');
            await wait(500);

            // Step 5: Response Generation
            logToEngine('Generating response via LLM...', 'active');
            
            // Generate Response Text
            const responseText = generateResponseText(query, retrievedDocs, state.config.singlish);
            
            // Remove loader
            toggleLoading(false);

            // Stream Response
            const msgContentDiv = appendMessage('assistant', '');
            await streamText(msgContentDiv, responseText);

            logToEngine('Response successfully delivered.', 'system');
        }

        function scoreBasedMock(doc, query) {
            // Simple mock scoring for demo visualization purposes
            // In real app, this is dot product similarity
            const terms = query.split(' ');
            let score = 0;
            terms.forEach(term => {
                if (doc.content.toLowerCase().includes(term)) score += 0.2;
            });
            return score > 0.2; // Threshold
        }

        function renderContextCards(docs) {
            dom.context.innerHTML = '';
            if(docs.length === 0) {
                dom.context.innerHTML = '<div class="text-xs text-secondary">No relevant documents found in Vector DB.</div>';
                return;
            }

            docs.forEach(doc => {
                const card = document.createElement('div');
                card.className = 'chunk-card';
                card.innerHTML = `
                    <div class="chunk-meta">
                        <span>${doc.source}</span>
                        <span class="chunk-score">${(doc.score * 100).toFixed(0)}% Match</span>
                    </div>
                    <div class="chunk-text">${doc.content}</div>
                `;
                dom.context.appendChild(card);
            });
        }

        function generateResponseText(query, docs, isSinglish) {
            // Naive template-based generation to ensure the demo works intelligently without a backend
            const hasPolicy = docs.some(d => d.type === 'policy');
            const hasProduct = docs.some(d => d.type === 'product');
            const hasShipping = docs.some(d => d.type === 'shipping');

            let response = "";
            const citations = docs.map((d, i) => `<sup class="citation" title="${d.source}">${i+1}</sup>`).join('');

            if (query.toLowerCase().includes("return") || query.toLowerCase().includes("refund")) {
                if (isSinglish) {
                    response = "Wah, you want return ah? <br>According to our policy, you got 7 days to return items one${citations}. But hor, must make sure the thing never open or use before. If it's software or digital goods, once the seal break, sorry ah, cannot return already${citations}.";
                } else {
                    response = "Regarding your return request: Our standard policy allows returns within 7 days of purchase, provided the item is unopened and in its original packaging${citations}. <br><br>Please note that for software or digital goods, once the seal is broken or the license is revealed, we cannot accept returns due to copyright restrictions${citations}.";
                }
            } else if (query.toLowerCase().includes("price") || query.toLowerCase().includes("cost")) {
                if (isSinglish) {
                    response = "The price is not bad leh. For the Air Purifier Model X1, it's selling at SGD 299${citations}. If you order above SGD 100, delivery is free one${citations}!";
                } else {
                    response = "I can help with pricing. The Nexus Air Purifier (Model X1) is currently listed at SGD 299.00${citations}. <br><br>Also, we offer free standard delivery for all orders exceeding SGD 100.00${citations}.";
                }
            } else {
                if (isSinglish) {
                    response = "I heard you, but can you be more specific? I checked our knowledge base but I'm not sure what you want exactly${citations}. You want to know about shipping or product specs?";
                } else {
                    response = "I've retrieved some relevant information based on your query${citations}, but I'm not entirely sure which aspect you are focusing on. Could you clarify if you are asking about pricing, shipping, or product specifications?";
                }
            }
            
            return response;
        }

        async function streamText(element, text) {
            // Create a temporary div to parse HTML tags separately
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = text;
            
            // Simple streaming: For this demo, we'll just fade it in to avoid 
            // complex HTML tag parsing logic in vanilla JS which might break tags.
            // Ideally, we'd stream text nodes only.
            
            element.innerHTML = '';
            element.style.opacity = 0;
            element.innerHTML = text;
            
            // Fade in effect
            let op = 0;
            const timer = setInterval(() => {
                if (op >= 1) clearInterval(timer);
                element.style.opacity = op;
                op += 0.1;
            }, 30);
        }

        function wait(ms) {
            return new Promise(resolve => setTimeout(resolve, ms));
        }

    </script>
</body>
</html>
```

---



Here is the **Project Architecture Document (PAD)**. This document is the definitive source of truth, designed to be fed directly into an AI coding agent (like Cursor, GitHub Copilot Workspace, or Devin) or used by a human senior developer to scaffold the entire system.

It adheres to the **Meticulous Approach**, focusing on Singapore-specific optimizations, strict compliance, and the "Anti-Generic" aesthetic philosophy.

---

# PROJECT ARCHITECTURE DOCUMENT (PAD)
**Project Name:** NexusAI SMB (Singapore Edition)
**Version:** 1.0.0-RC
**Status:** Ready for Implementation
**Architecture Style:** Event-Driven Microservices (Monolith-First Deployment)

---

## 1. EXECUTIVE SUMMARY & VISION

### 1.1 Core Objective
Build a **context-aware, multilingual Customer Service AI Agent** specifically architected for Singapore SMBs. The system must move beyond simple Q&A to handle complex, multi-turn conversations while maintaining strict PDPA compliance and cultural fluency (Singlish/Standard English).

### 1.2 Success KPIs
*   **Resolution Rate:** >85% without human escalation.
*   **Cultural Accuracy:** Singlish detection and response accuracy >90%.
*   **Compliance:** 100% PDPA adherence (automated PII masking).
*   **Latency:** <1.5s Time to First Token (TTFT).
*   **ROI:** Enable PSD Grant qualification (80% cost recovery potential).

---

## 2. SINGAPORE CONTEXT & COMPLIANCE LAYER

This section is non-negotiable. All code must pass these filters.

### 2.1 Cultural Intelligence Module
*   **Singlish Handling:**
    *   **Detection:** Use a keyword classifier (e.g., `lah`, `lor`, `leh`, `meh`, `shiok`, `kiasu`) or a small BERT model fine-tuned on Singlish datasets.
    *   **Translation:** Internal logic translates Singlish -> Standard English for RAG retrieval.
    *   **Response:** Post-processing re-applies Singlish tone if user initiated it (Configurable `persona_mode`).
*   **Currency & Formats:**
    *   All currency: `SGD` (Format: `$1,234.56`).
    *   Dates: `DD/MM/YYYY` (Singapore Standard).
*   **Channel Strategy:**
    *   **Primary:** WhatsApp Business API (Cloud API).
    *   **Secondary:** Web Widget (React).

### 2.2 Regulatory Compliance (PDPA & IMDA)
*   **Data Minimization:** Only collect conversation history and metadata strictly necessary for support.
*   **Right to be Forgotten:** Implement `/api/v1/user/{id}/forget` endpoint to trigger cascading deletion across PostgreSQL, Redis, and Vector DB.
*   **PII Masking:**
    *   **Tool:** Microsoft Presidio (`presidio-analyzer`, `presidio-anonymizer`).
    *   **Action:** Redact NRIC, Mobile Numbers, and Email addresses *before* sending to LLM context window.
*   **Data Sovereignty:** All data hosted in AWS `ap-southeast-1` (Singapore) region only.

---

## 3. TECHNOLOGY STACK

The stack is chosen for performance, developer velocity, and local ecosystem support in Singapore.

| Layer | Technology | Justification |
|-------|------------|---------------|
| **Frontend** | Next.js 14 (App Router) | Server-side rendering (SEO), API routes, React Server Components. |
| **UI Library** | Shadcn/UI + Tailwind CSS 4 | "Anti-Generic" foundation. Highly customizable, accessible primitives. |
| **Backend** | Python 3.11+ (FastAPI) | Async performance, native WebSocket support, automatic OpenAPI docs. |
| **Orchestration** | LangGraph | Stateful, cyclical agent workflows (better than simple chains). |
| **LLM** | OpenAI GPT-4o-mini (Primary) <br> Llama-3-8B (Local Fallback) | Cost-efficiency (GPT-4o-mini) + Privacy fallback (Local LLM for sensitive data). |
| **Vector DB** | Qdrant (Hybrid Search) | Best-in-class filtering, performs well on affordable instances. |
| **Cache/Session** | Redis (ElastiCache) | Fast state management for conversation history. |
| **Relational DB** | PostgreSQL (RDS) | Structured data (Users, Analytics, Tickets). |
| **Infrastructure** | AWS ECS (Fargate) | Serverless containers, auto-scaling for Singapore traffic spikes. |
| **Observability** | LangSmith + Datadog | LLM tracing + Infrastructure monitoring. |

---

## 4. SYSTEM ARCHITECTURE

### 4.1 High-Level Diagram
```
┌──────────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  WhatsApp    │  │  Web Widget  │  │  Admin Dashboard         │
│  │  (Meta API)  │  │  (Next.js)   │  │  (Next.js)   │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
└─────────┼──────────────────┼──────────────────┼─────────────────┘
          │                  │                  │
          │ Webhook/HTTPS    │ WebSocket/HTTP   │ HTTPS
          ▼                  ▼                  ▼
┌──────────────────────────────────────────────────────────────────┐
│                     API GATEWAY (AWS ALB)                         │
└──────────────────────────────┬───────────────────────────────────┘
                               │
┌──────────────────────────────▼───────────────────────────────────┐
│                    APPLICATION LAYER (FastAPI)                   │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  AGENT ORCHESTRATOR (LangGraph)                             │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐     │ │
│  │  │ Intent   │  │  RAG     │  │  Tools   │  │  Safety  │     │ │
│  │  │ Analysis │  │  Search  │  │ (API/DB) │  │  Guard   │     │ │
│  │  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘     │ │
│  └───────┼─────────────┼─────────────┼─────────────┼───────────┘ │
└──────────┼─────────────┼─────────────┼─────────────┼─────────────┘
           │             │             │             │
    ┌──────▼──────┐ ┌────▼──────┐ ┌───▼────┐ ┌────▼──────┐
    │  Redis      │ │  Qdrant   │ │ Postgres│   Presidio │
    │  (Sessions) │ │ (Vectors) │ │ (Users) │  (PII Mask)│
    └─────────────┘ └───────────┘ └────────┘ └───────────┘
```

### 4.2 Data Flow (Request Lifecycle)
1.  **Ingest:** User sends message via WhatsApp.
2.  **Normalization:** FastAPI receives webhook. Meta payload normalized to internal `Message` schema.
3.  **PII Scan:** `Presidio` scans text. If PII found, mask with placeholders (e.g., `<PHONE_NUMBER>`). Store hash of real value in Redis for unmasking *only* if necessary for execution (e.g., booking a cab).
4.  **Agent Execution:** LangGraph receives state.
    *   *Node 1:* Detect Singlish/Intent.
    *   *Node 2:* Search Vector DB (Hybrid: Keyword + Semantic).
    *   *Node 3:* LLM Synthesis (GPT-4o-mini).
5.  **Safety Check:** Output checked for prohibited content/controversial topics.
6.  **Response:** Send back to WhatsApp API.

---

## 5. DATA ARCHITECTURE

### 5.1 PostgreSQL Schema (Key Tables)
```sql
-- Users (GDPR compliant)
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone_number VARCHAR(20) UNIQUE, -- WhatsApp ID
    language_preference VARCHAR(10) DEFAULT 'en_SG',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    is_anonymized BOOLEAN DEFAULT FALSE
);

-- Conversations
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    status VARCHAR(20) DEFAULT 'active', -- active, closed, escalated
    sentiment_score DECIMAL(3,2), -- -1.0 to 1.0
    started_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Messages
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id),
    role VARCHAR(10) NOT NULL, -- user, assistant, system
    content TEXT NOT NULL,
    is_pii_masked BOOLEAN DEFAULT FALSE,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Audit Log (Crucial for Grants/Compliance)
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id UUID,
    action VARCHAR(50),
    details JSONB,
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

### 5.2 Qdrant (Vector DB) Collection Schema
*   **Collection Name:** `smb_knowledge_base`
*   **Vector Size:** 1024 (BGE-Large-EN-V1.5)
*   **Distance:** Cosine
*   **Payload Structure:**
    ```json
    {
      "content": "Text chunk...",
      "source": "policy_manual.pdf",
      "page_number": 12,
      "category": "returns",
      "language": "en",
      "access_level": "public", // vs 'internal_staff'
      "last_updated": "2024-05-20"
    }
    ```

---

## 6. AI AGENT ARCHITECTURE (LangGraph)

### 6.1 State Graph Definition
The agent is not a simple prompt/response. It is a graph of state.

```python
class AgentState(TypedDict):
    messages: list[BaseMessage]
    user_intent: str  # e.g., "return_request", "singlish_complaint"
    retrieved_docs: list[Document]
    singlish_mode: bool
    session_id: str
```

### 6.2 Graph Nodes (Execution Steps)
1.  **`classify_language`**:
    *   Input: User Message.
    *   Logic: Check for Singlish markers. Set `singlish_mode` flag.
2.  **`retrieve_context`**:
    *   Logic: Query Qdrant using Hybrid Search (Sparse BM25 + Dense Vector).
    *   Filter: Apply `access_level` and `last_updated` filters.
3.  **`rag_generate`**:
    *   Input: `retrieved_docs` + `user_intent`.
    *   Logic: Construct prompt. If `singlish_mode` is true, append "Instructions: Use casual Singaporean English (Singlish) where appropriate." to system prompt.
    *   Model: `gpt-4o-mini`.
4.  **`human_escalation_check`**:
    *   Logic: If confidence < 0.6 or sentiment is very negative (`<-0.8`), route to `human_handoff`.

### 6.3 Prompt Engineering Strategy
*   **System Prompt Template:**
    ```text
    You are a helpful customer support agent for {company_name} in Singapore.
    You answer strictly based on the provided context. If you don't know, say "I'm not sure, I'll check with my team."
    
    CONTEXT: {retrieved_context}
    
    INSTRUCTIONS:
    - Be concise and polite.
    - Use SGD for currency.
    - <USE_SINGLISH> Use light Singlish (lah, lor) to build rapport. </USE_SINGLISH>
    ```

---

## 7. API CONTRACT (FastAPI)

### 7.1 Core Endpoints

#### `POST /api/v1/webhook/whatsapp`
*   **Purpose:** Receive incoming messages from Meta.
*   **Auth:** Verify Token (Header `X-Hub-Signature-256`).
*   **Body:** Standard WhatsApp Webhook JSON.
*   **Response:** 200 OK (Must be fast, <200ms, then process async).

#### `POST /api/v1/chat/completions`
*   **Purpose:** Standard chat for Web Widget.
*   **Body:**
    ```json
    {
      "message": "How to return item?",
      "session_id": "uuid",
      "user_meta": { "timezone": "Asia/Singapore" }
    }
    ```
*   **Response (Streaming):** Server-Sent Events (SSE) or Chunked Transfer Encoding.

#### `GET /api/v1/analytics/dashboard`
*   **Purpose:** Business Owner Dashboard.
*   **Returns:** JSON with resolution rate, top topics, cost savings (in SGD).

---

## 8. FRONTEND ARCHITECTURE (Next.js)

### 8.1 UI Philosophy (Anti-Generic)
*   **Do Not Use:** Default Bootstrap colors, standard purple AI gradients, generic card layouts.
*   **Do Use:**
    *   **Typography:** Inter (UI) + JetBrains Mono (Code/Data).
    *   **Palette:** Deep Slate (`#0f172a`), Electric Teal (`#14b8a6`), Warm White (`#f8fafc`).
    *   **Layout:** Asymmetrical grids for the dashboard. Chat bubbles with distinct "thinking" states.

### 8.2 Component Structure
*   `components/ui/` (Shadcn primitives: Button, Dialog, ScrollArea).
*   `components/chat/`
    *   `ChatInterface.tsx`: Main container.
    *   `MessageBubble.tsx`: Handles user/assistant/styles.
    *   `FeedbackWidget.tsx`: Thumbs up/down logic.
*   `components/dashboard/`
    *   `ConversationMap.tsx`: Visual representation of chat flows.
    *   `SentimentChart.tsx`: Recharts integration.

### 8.3 State Management
*   **Zustand**: For global client state (Theme, User Session).
*   **React Query (TanStack Query)**: For fetching server-side data (Analytics, History).

---

## 9. SECURITY & INFRASTRUCTURE

### 9.1 Security
*   **Secrets Management:** AWS Secrets Manager (never `.env` in git).
*   **Rate Limiting:** Slow down abusive users (Redis-based token bucket).
*   **Input Sanitization:** Strip all HTML tags from user inputs before LLM processing.

### 9.2 Infrastructure as Code (Terraform)
*   **VPC:** Isolated within `ap-southeast-1`.
*   **ECS:** Two services - `api-service` (FastAPI) and `frontend-service` (Next.js).
*   **RDS:** Postgres 15 Multi-AZ.
*   **Qdrant:** EC2 instance or Docker container in ECS with EBS volume.

---

## 10. IMPLEMENTATION ROADMAP (For AI Agents)

If you are an AI coding agent, execute the following sequence strictly:

1.  **Phase 1: Scaffold**
    *   Initialize Monorepo (Nx or Turbo).
    *   Set up `frontend` (Next.js) and `backend` (FastAPI) apps.
    *   Configure Tailwind and Shadcn.

2.  **Phase 2: Data & Database**
    *   Write Docker Compose for local dev (Postgres, Redis, Qdrant).
    *   Write SQL Schema in `backend/prisma/schema.prisma` or raw SQL files.
    *   Create Alembic migrations.

3.  **Phase 3: Backend Core**
    *   Implement FastAPI app structure.
    *   Create `/health` endpoint.
    *   Implement `PresidioService` for PII masking (Unit test this first).

4.  **Phase 4: RAG Pipeline**
    *   Implement `VectorStoreService` (Qdrant client).
    *   Create dummy data loader script.
    *   Implement `HybridRetriever` (BM25 + Vector).

5.  **Phase 5: The Agent**
    *   Install `langgraph`.
    *   Define `AgentState`.
    *   Implement the graph nodes (`classify`, `retrieve`, `generate`).
    *   Connect to FastAPI endpoints.

6.  **Phase 6: Frontend Integration**
    *   Build Chat UI (using Shadcn components).
    *   Connect to backend WebSocket/SSE.
    *   Implement streaming text display.

7.  **Phase 7: WhatsApp Integration**
    *   Set up Meta Developer App.
    *   Implement webhook verification and message reception.

8.  **Phase 8: Testing & Audit**
    *   Add `pytest` for backend (target >80% coverage).
    *   Verify PDPA "Forget Me" functionality.

---

**End of Document.**

This Architecture Document provides the structural integrity required to build a robust, compliant, and culturally resonant AI system. Proceed with implementation.
