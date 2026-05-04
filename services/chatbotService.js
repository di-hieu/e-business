// services/chatbotService.js
const axios = require('axios');
require('dotenv').config();
const knowledgeBase = require('../config/knowledgeBase');

// --- Configuration ---
const OLLAMA_API_URL = 'http://localhost:11434/api/chat';
const OLLAMA_MODEL = process.env.OLLAMA_MODEL || 'llama2';
const FB_PAGE_ID = process.env.FB_PAGE_ID;
// Knowledge base is loaded from config/knowledgeBase.js
// const knowledgeBase = require('../config/knowledgeBase'); 


/**
 * Searches the local knowledge base for relevant FAQs or products.
 * @param {string} messageText - The user's input.
 * @returns {string} Contextual information found.
 */
function retrieveKnowledge(messageText) {
    const lowerCaseMessage = messageText.toLowerCase();
    let context = [];
    
    // Search FAQs
    const faqMatch = knowledgeBase.faqs.find(faq => 
        faq.keywords.some(keyword => lowerCaseMessage.includes(keyword))
    );
    if (faqMatch) {
        context.push(`[FAQ]: ${faqMatch.answer}`);
    }

    // Search Products
    const productMatch = knowledgeBase.products.find(product => 
        product.keywords.some(keyword => lowerCaseMessage.includes(keyword))
    );
    if (productMatch) {
        context.push(`[PRODUCT]: ${product.name} (SKU: ${product.sku}) - ${product.description} | Giá: ${product.price}`);
    }
    
    if (context.length > 0) {
        return `[Knowledge Context Found]: ${context.join('\n---\n')}`;
    }
    return "Không tìm thấy thông tin cụ thể trong cơ sở dữ liệu nội bộ. Hãy hỏi về các chủ đề chung để tôi tra cứu thêm.";
}

/**
 * Main function to process a user's message through the AI core.
 * @param {string} messageText - The incoming text message from the user.
 * @param {string} senderId - ID of the sender.
 * @param {string} platform - Platform of the message (Facebook, Zalo, etc.).
 * @returns {Promise<string>} The AI-generated, formatted response text.
 */
async function processChatRequest(messageText, senderId, platform) {
    // 1. Retrieve and inject context/knowledge base
    const knowledgeContext = retrieveKnowledge(messageText);
    
    if (!OLLAMA_API_URL) {
        console.warn("OLLAMA_API_URL not set. Cannot connect to AI service.");
        return `Xin chào! Tôi là trợ lý AI của cửa hàng. Hiện tại tôi đang gặp sự cố kỹ thuật và không thể trả lời bạn. Vui lòng thử lại sau. (Platform: ${platform})`;
    }

    console.log(`--- Running AI processing for ${platform} ---`);

    // 2. Construct the system prompt using the retrieved knowledge
    const systemPrompt = `Bạn là một trợ lý AI bán hàng chuyên nghiệp, thân thiện, và hiểu rõ về thương mại xã hội tại Việt Nam. Nhiệm vụ của bạn là sử dụng thông tin CUNG CẤP TRONG TRUYỀN THÔNG BỐI CẢNH bên dưới để trả lời câu hỏi của khách hàng một cách chính xác, đầy đủ, và mang tính chuyển đổi cao.
    
    ---
    **BỐI CẢNH TRI THỨC:**
    ${knowledgeContext}
    ---
    
    Các bước trả lời cần tuân theo:
    1. Phân tích ý định của khách hàng.
    2. Nếu thông tin có trong BỐI CẢNH, hãy sử dụng nó để trả lời.
    3. Nếu không có thông tin, hãy trả lời một cách tự nhiên và lịch sự, đồng thời gợi ý khách hàng cung cấp thêm chi tiết.
    4. Luôn kết thúc bằng lời kêu gọi hành động (CTA) như "Vui lòng để lại SĐT/Địa chỉ để được tư vấn chi tiết hơn."`;

    // 3. Construct the request payload for the LLM API
    const payload = {
        model: OPENAI_MODEL,
        messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: messageText }
        ],
        temperature: 0.7,
    };

    try {
        // 4. Call the Ollama API
        const response = await axios.post(
            OLLAMA_API_URL, 
            payload, 
            { 
                headers: { 
                    'Content-Type': 'application/json'
                }
            }
        );

        const aiResponse = response.data.choices[0].message.content;
        
        // 5. Further process/format response
        return formatAiResponse(aiResponse, platform);

    } catch (error) {
        console.error("Error calling OpenAI API:", error.response ? error.response.data : error.message);
        return `Xin lỗi, tôi đã gặp lỗi khi kết nối với hệ thống AI. Vui lòng liên hệ trực tiếp với nhân viên hỗ trợ hoặc kiểm tra lại thông tin.`;
    }
}

/**
 * Formats the raw AI response to ensure consistency and actionability.
 * (Placeholder for advanced response parsing/enrichment)
 */
function formatAiResponse(rawResponse, platform) {
    // Example: Extracting Product Names or SKUs from the response.
    let formatted = rawResponse.trim();

    // Simple check for a follow-up action
    if (formatted.toLowerCase().includes("hàng") && !formatted.includes("Xin lỗi")) {
        formatted = "\n\n⭐ **Gợi ý hành động:** Vui lòng phản hồi bằng [Mã Sản Phẩm] và [Số Lượng] để chúng tôi kiểm tra tồn kho và báo giá chính xác nhất cho bạn.\n";
    }

    return formatted;
}


module.exports = {
    processChatRequest
};


/**
 * Main function to process a user's message through the AI core.
 * @param {string} messageText - The incoming text message from the user.
 * @param {string} senderId - ID of the sender.
 * @param {string} platform - Platform of the message (Facebook, Zalo, etc.).
 * @returns {Promise<string>} The AI-generated, formatted response text.
 */
async function processChatRequest(messageText, senderId, platform) {
    if (!OLLAMA_API_URL) {
        console.warn("OLLAMA_API_URL not set. Cannot connect to AI service.");
        return `Xin chào! Tôi là trợ lý AI của cửa hàng. Hiện tại tôi đang gặp sự cố kỹ thuật và không thể trả lời bạn. Vui lòng thử lại sau. (Platform: ${platform})`;
    }

    console.log(`--- Running AI processing for ${platform} ---`);

    // 1. Retrieve and inject context/knowledge base (Simulated Step)
    // In a real system, we would query a DB or a dedicated knowledge service here.
    const systemPrompt = `You are a helpful, polite, and professional AI Chatbot assistant for a social commerce SME in Vietnam. Your goal is to help users with product inquiries, provide FAQs, and facilitate simple order placement based on the company's knowledge base. Keep responses friendly and actionable. The user is messaging from a ${platform} platform.`;

    // 2. Construct the request payload for the LLM API
    const payload = {
        model: OLLAMA_MODEL,
        messages: [
            { role: "system", content: systemPrompt },
            { role: "user", content: messageText }
        ],
        temperature: 0.7,
    };

    try {
        // 3. Call the Ollama API
        const response = await axios.post(
            OLLAMA_API_URL, 
            payload, 
            { 
                headers: { 
                    'Content-Type': 'application/json'
                }
            }
        );

        const aiResponse = response.data.choices[0].message.content;
        
        // 4. Further process/format response (e.g., checking for order confirmation keywords)
        return formatAiResponse(aiResponse, platform);

    } catch (error) {
        console.error("Error calling OpenAI API:", error.response ? error.response.data : error.message);
        return `Xin lỗi, tôi đã gặp lỗi khi kết nối với hệ thống AI. Vui lòng liên hệ trực tiếp với nhân viên hỗ trợ hoặc kiểm tra lại thông tin.`;
    }
}

/**
 * Formats the raw AI response to ensure consistency and actionability.
 * (Placeholder for advanced response parsing/enrichment)
 */
function formatAiResponse(rawResponse, platform) {
    // Example: Extracting Product Names or SKUs from the response.
    let formatted = rawResponse.trim();

    // Simple check for a follow-up action
    if (formatted.toLowerCase().includes("hàng")) {
        formatted = "\n🛒 **Gợi ý sản phẩm:** Bạn có thể xem qua các sản phẩm X và Y, chúng phù hợp với yêu cầu của bạn.\n";
    }

    return formatted;
}


module.exports = {
    processChatRequest
};