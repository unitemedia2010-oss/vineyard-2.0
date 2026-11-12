export interface WineProduct {
  id: number;
  source_url: string;
  name: string;
  slug: string;
  sku?: string;
  brand?: string;
  category?: string;
  origin_country?: string;
  region?: string;
  producer?: string;
  vintage?: string;
  grape_variety?: string;
  volume?: string;
  abv?: string;
  original_price?: number;
  sale_price?: number;
  currency: string;
  stock_status: string;
  description?: string;
  tasting_notes?: string;
  specs: Record<string, string>;
  main_image_url?: string;
  gallery_image_urls: string[];
}

export interface Category {
  id: number;
  name: string;
  slug: string;
  description?: string;
  product_count?: number;
}

export interface CartItem {
  product: WineProduct;
  quantity: number;
}
