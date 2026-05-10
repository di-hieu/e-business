TÀI LIỆU ĐẶC TẢ YÊU CẦU PHẦN MỀM -SC Chatbot 

Tên dự án: Trợ lý Chatbot AI cho Thương mại Xã hội (Social Commerce). 

1. TỔNG QUAN DỰ ÁN (PROJECT OVERVIEW) 

    Mục tiêu: Xây dựng hệ thống chatbot tích hợp AI để tự động hóa dịch vụ khách hàng và mua sắm trên các nền tảng mạng xã hội và e-commerce. Giải pháp này được xây dựng dưới dạng phần mềm dịch vụ (SaaS) nhằm cung cấp cho các doanh nghiệp nhỏ lẻ (SME), các công ty e-commerce (như Haravan) ở đa dạng lĩnh vực như làm đẹp, điện tử, tiêu dùng, du lịch. 

    Vấn đề giải quyết: Khắc phục tình trạng thiếu nhân sự trực 24/7 của các SME, giảm thiểu việc bỏ lỡ đơn hàng tiềm năng, đồng thời giảm chi phí nhân sự và tạo trải nghiệm khách hàng nhất quán. 

    Kỳ vọng: Giảm thời gian phản hồi trung bình xuống dưới 1 phút, tăng tỷ lệ chuyển đổi từ 10 - 20%, nâng cao sự hài lòng của khách hàng và tự động hóa quy trình chăm sóc khách hàng. 

2. YÊU CẦU CHỨC NĂNG (FUNCTIONAL REQUIREMENTS) 

    Tích hợp trên kênh mạng xã hội: Chatbot phải có khả năng tiếp nhận và phản hồi tin nhắn từ nền tảng Zalo. 

    Tư vấn và giải đáp tự động (FAQ & Consultation):  

    Hệ thống phải tự động trả lời các câu hỏi thường gặp (FAQ) của người dùng. 

    Chatbot có khả năng truy xuất thông tin chi tiết của từng sản phẩm (ví dụ: công dụng, chống chỉ định, hàm lượng) để tư vấn chuyên sâu cho khách hàng. 

    Gợi ý sản phẩm: Chatbot cần có thuật toán để gợi ý sản phẩm phù hợp dựa trên yêu cầu từ khóa của người dùng hoặc lịch sử mua hàng. 

    Xử lý đơn hàng: Chatbot hỗ trợ bán hàng, nhận đơn hàng đơn giản, tạo đơn và đồng bộ dữ liệu trực tiếp lên hệ thống quản lý đơn hàng của doanh nghiệp, cũng như cho phép tra cứu đơn hàng. 

    Thu thập thông tin động và Gọi API:  

    Hệ thống sử dụng cơ chế Function Calling để yêu cầu AI tự động hỏi và thu thập đủ các thông tin cần thiết từ người dùng (ví dụ: thông tin đặt vé tour, khu vực giao hàng). 

    Sau khi thu thập đủ thông tin, chatbot tự động gọi API của doanh nghiệp để thực hiện các nghiệp vụ như: kiểm tra tình trạng đặt chỗ (còn/hết vé), kiểm tra tồn kho theo khu vực và báo giá chính xác. 

    Phân tích dữ liệu (Analytics): Tích hợp tính năng theo dõi tương tác, lịch sử hội thoại để cung cấp báo cáo cơ bản phục vụ đánh giá mức độ hài lòng và tỷ lệ chuyển đổi. 

3. YÊU CẦU PHI CHỨC NĂNG (NON-FUNCTIONAL REQUIREMENTS) 

    Kiến trúc Hệ thống & Nền tảng Cloud: Hệ thống được thiết kế theo dạng Multi-tenant để phục vụ nhiều doanh nghiệp cùng lúc. Phải được triển khai trên các nền tảng đám mây -AWS để đảm bảo tính mở rộng và dễ dàng tích hợp. 

    Công nghệ :  

    Ngôn ngữ lập trình: Python. 

    AI & Logic: đùng LLM, kết hợp với thư viện Langchain để điều phối và thực thi Function Calling. 

    Database:  

    Sử dụng Cơ sở dữ liệu NoSQL để lưu trữ lịch sử hội thoại. 

    Sử dụng Vector Database (FAISS hoặc Qdrant) để lưu trữ kho tri thức. Kho tri thức này được tạo ra bằng cách thu thập (crawl) dữ liệu từ website doanh nghiệp hoặc từ các kịch bản mẫu từ khách hàng. Dữ liệu được nhúng (embedding) thành các chunk để AI truy xuất và trả lời theo ngữ cảnh. 

    Hiệu suất & Khả dụng: Hệ thống phải hoạt động ổn định 24/7 và đảm bảo tốc độ phản hồi truy vấn nhanh. 

4. KẾ HOẠCH TRIỂN KHAI VÀ BẢO TRÌ (DEPLOYMENT PLAN) 

Dự án được lên kế hoạch triển khai trong vòng 3 tháng: 

    Tháng 1 - Nghiên cứu & Thiết lập: Xác định nền tảng (ChatGPT API, Node.js/Python), kịch bản hội thoại. Thiết lập hạ tầng đám mây, môi trường phát triển, và đăng ký các API mạng xã hội Zalo. 

    Tháng 2 - Phát triển & Kiểm thử: Xây dựng tính năng cốt lõi (Langchain, Vector DB, Function calling). Tích hợp vào Zalo mẫu, thực hiện kiểm thử nội bộ để tinh chỉnh kịch bản. 

    Tháng 3 - Triển khai & Tối ưu: Triển khai thử nghiệm cho một doanh nghiệp SME. Theo dõi các chỉ số KPI, thu thập dữ liệu thực tế để tối ưu hóa câu trả lời và đánh giá hiệu quả báo cáo. 

5. CHỈ SỐ ĐÁNH GIÁ THÀNH CÔNG (KPIs) 

    Tốc độ phản hồi trung bình tính bằng giây. 

    Tỷ lệ chuyển đổi từ việc hỏi đáp thành đơn hàng thành công. 

    Số lượng câu hỏi chatbot xử lý thành công mỗi ngày. 

    Điểm đánh giá mức độ hài lòng của khách hàng sau tương tác. 

    Chi phí nhân sự tiết kiệm được hoặc phần doanh thu gia tăng thêm. Việc triển khai hệ thống này còn đóng góp vào quá trình chuyển đổi số và quản lý tri thức của doanh nghiệp (tái sử dụng FAQ làm thư viện kiến thức). 

 