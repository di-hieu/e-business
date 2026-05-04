// routes/chatRoutes.js
const express = require('express');
const router = express.Router();
const { processChatRequest } = require('../services/chatbotService');

// Endpoint to handle all chat messages from various platforms
router.post('/', async (req, res) => {
    const { senderId, messageText, platform = 'unknown' } = req.body;

    if (!senderId || !messageText) {
        return res.status(400).json({ error: 'Missing senderId or messageText.' });
    }

    console.log(`[${platform}] Received message from ${senderId}: ${messageText}`);

    try {
        // 1. Process the chat request through the core service
        const responseText = await processChatRequest(messageText, senderId, platform);

        // 2. Simulate saving conversation history (placeholder)
        // saveConversationHistory(senderId, messageText, responseText); 

        // 3. Send response back (implementation depends on platform API)
        res.json({ 
            success: true, 
            response: responseText,
            message: `Successfully processed request for ${senderId}`
        });
    } catch (error) {
        console.error('Error processing chat request:', error.message);
        res.status(500).json({ error: 'Failed to process chat request.' });
    }
});

module.exports = router;