// config/knowledgeBase.js

/**
 * Simulated knowledge base for FAQs and product catalog.
 * In a real system, this data would come from a PostgreSQL/MongoDB database.
 */
const knowledgeBase = {
    // --- FAQs ---
    faqs: [
        { 
            keywords: ["giờ mở cửa", "mở cửa khi nào"], 
            answer: "Cửa hàng của chúng tôi mở cửa từ 9:00 AM đến 9:00 PM, 7 ngày/tuần. Chúng tôi phục vụ 24/7 qua Chatbot AI!" 
        },
        { 
            keywords: ["giao hàng", "giao hàng mất bao lâu"], 
            answer: "Chúng tôi giao hàng toàn quốc. Thời gian giao hàng dự kiến từ 1-3 ngày làm việc, tùy thuộc vào khu vực của bạn. Bạn có thể để lại địa chỉ để chúng tôi báo giá chính xác hơn." 
        },
        { 
            keywords: ["chính sách đổi trả", "bảo hành"], 
            answer: "Chúng tôi cam kết đổi trả sản phẩm trong vòng 7 ngày kể từ ngày nhận hàng, nếu sản phẩm bị lỗi do nhà sản xuất. Vui lòng giữ lại biên nhận mua hàng." 
        }
    ],

    // --- Products ---
    products: [
        { 
            sku: "S-2024-001", 
            name: "Áo Thun Cotton Basic", 
            description: "Áo thun cơ bản, chất liệu cotton thoáng mát, phù hợp với nhiều dịp.",
            price: "199,000 VND",
            keywords: ["áo thun", "cotton", "basic"]
        },
        { 
            sku: "S-2024-002", 
            name: "Quần Jeans Slim Fit", 
            description: "Quần jeans nam dáng slim fit, chất liệu denim cao cấp, độ co giãn tốt.",
            price: "350,000 VND",
            keywords: ["quần jeans", "nam", "denim"]
        }
    ]
};

module.exports = knowledgeBase;