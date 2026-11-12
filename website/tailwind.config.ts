import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        cellar: {
          950: "#0A0708",
          900: "#140D0F",
          850: "#1C1417",
          800: "#271B20",
          700: "#3D2B32",
        },
        bordeaux: {
          DEFAULT: "#4A0E17",
          hover: "#661320",
          light: "#821929",
          muted: "rgba(74, 14, 23, 0.4)",
        },
        champagne: {
          DEFAULT: "#D4AF37",
          light: "#F3E5AB",
          dark: "#AA8C2C",
        },
        alabaster: {
          DEFAULT: "#FBF9F5",
          muted: "#A8A19F",
          dark: "#6B6567",
        }
      },
      fontFamily: {
        serif: ["Cinzel", "Playfair Display", "Georgia", "serif"],
        sans: ["Plus Jakarta Sans", "Inter", "sans-serif"],
      },
    },
  },
  plugins: [],
};
export default config;
