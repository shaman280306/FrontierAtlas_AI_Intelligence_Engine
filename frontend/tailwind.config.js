/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0B1020",      // Midnight Navy
        surface: "#111A2E",         // Deep Slate
        elevated: "#17233A",        // Elevated Slate
        border: "#1E2D4A",          // Border Slate
        primary: {
          DEFAULT: "#4F8CFF",       // Electric Blue
          hover: "#3B7BE8",
          muted: "rgba(79, 140, 255, 0.15)"
        },
        cyan: {
          DEFAULT: "#36D6E7",       // Data & intelligence
          muted: "rgba(54, 214, 231, 0.15)"
        },
        violet: {
          DEFAULT: "#9275FF",       // AI & research
          muted: "rgba(146, 117, 255, 0.15)"
        },
        emerald: {
          DEFAULT: "#35C98A",       // Verified / success
          muted: "rgba(53, 201, 138, 0.15)"
        },
        amber: {
          DEFAULT: "#F3B84B",       // Freshness / warnings
          muted: "rgba(243, 184, 75, 0.15)"
        },
        text: {
          primary: "#F4F7FC",       // Soft White
          secondary: "#98A7BD",     // Muted Grey
          muted: "#60728F"
        }
      },
      fontFamily: {
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "Segoe UI", "Roboto", "sans-serif"],
        mono: ["JetBrains Mono", "Fira Code", "monospace"]
      }
    },
  },
  plugins: [],
};
