import { WineProduct } from "@/types/wine";
import fs from "fs";
import path from "path";

export async function getAllProducts(): Promise<WineProduct[]> {
  try {
    const jsonPath = path.resolve(process.cwd(), "../data/normalized/products.json");
    if (fs.existsSync(jsonPath)) {
      const content = fs.readFileSync(jsonPath, "utf-8");
      return JSON.parse(content) as WineProduct[];
    }
  } catch (e) {
    console.warn("Could not read local normalized products JSON, using fallback data:", e);
  }

  // Fallback sample wine for preview
  return [
    {
      id: 1,
      source_url: "https://vineyard.vn/san-pham/r9-primitivo-icono",
      name: "R9 Primitivo & Syrah Passito Salento IGP",
      slug: "r9-primitivo-icono",
      sku: "B06.GRATI.06",
      brand: "Reputazione",
      category: "Vang Đỏ > Vang Ý",
      origin_country: "Italy",
      region: "Puglia",
      producer: "Reputazione",
      vintage: "2019",
      grape_variety: "Primitivo & Syrah",
      volume: "0.75L",
      abv: "19,0%",
      original_price: undefined,
      sale_price: undefined,
      currency: "VND",
      stock_status: "Còn trong kho",
      description: "Dòng vang thượng hạng phiên bản giới hạn với nồng độ 19 độ đậm sâu từ phương pháp nho phơi khô Passito cổ truyền vùng Puglia nước Ý.",
      tasting_notes: "Màu: Đỏ Ruby đậm ánh tím quý phái.\nVị: Cấu trúc dầy dặn, tannin mềm mại như nhung hòa cùng vị mận chín, quả anh đào đen, sô-cô-la đen và gia vị phương Đông.",
      specs: {
        "Quốc gia": "Italy",
        "Vùng": "Puglia",
        "Nồng độ": "19,0%",
        "Dung tích": "0.75L",
        "Phân hạng": "Icon wine/DOC",
        "Loại nút": "Bần"
      },
      main_image_url: "https://vineyard.vn/userfiles/images/SanPham/RuouVangCaoCap/VangY/R9-limited-edition.png",
      gallery_image_urls: []
    }
  ];
}

export async function getProductBySlug(slug: string): Promise<WineProduct | null> {
  const products = await getAllProducts();
  return products.find(p => p.slug === slug) || null;
}
