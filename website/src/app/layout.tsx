import type { Metadata } from "next";
import "@/app/globals.css";

export const metadata: Metadata = {
  title: "VINEYARD 2.0 - Hầm Rượu Vang Thượng Hạng Nhập Khẩu Chính Hãng",
  description: "Tuyển chọn các dòng rượu vang Grand Cru, DOCG từ Ý, Pháp, Chile, Úc được bảo quản tại hầm nhiệt độ tiêu chuẩn.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="vi" className="dark bg-cellar-950 text-alabaster antialiased">
      <body className="min-h-screen flex flex-col font-sans selection:bg-bordeaux selection:text-champagne-light">
        {children}
      </body>
    </html>
  );
}
