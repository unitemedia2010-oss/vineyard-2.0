with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace hardcoded shades with variables
html = html.replace(
    '.niche{position:relative;aspect-ratio:3/5;border-radius:50% 50% 5px 5px/26% 26% 5px 5px;background:radial-gradient(120% 85% at 50% 32%,#f3eadb 0%,#e3d3b7 55%,#c7b08d 100%);box-shadow:inset 0 14px 26px rgba(70,40,22,.38),inset 0 -8px 14px rgba(70,40,22,.22);overflow:hidden;display:block}',
    '.niche{position:relative;aspect-ratio:3/5;border-radius:50% 50% 5px 5px/26% 26% 5px 5px;background:var(--niche-bg);box-shadow:var(--niche-shadow);overflow:hidden;display:block}'
)

html = html.replace(
    '.shade{position:absolute;inset:0;z-index:1;pointer-events:none;background:radial-gradient(circle var(--r) at var(--x) var(--y),rgba(20,12,11,0) 0%,rgba(20,12,11,.28) 34%,rgba(20,12,11,.88) 70%,rgba(20,12,11,.975) 100%)}',
    '.shade{position:absolute;inset:0;z-index:1;pointer-events:none;background:radial-gradient(circle var(--r) at var(--x) var(--y),var(--shade-0) 0%,var(--shade-34) 34%,var(--shade-70) 70%,var(--shade-100) 100%)}'
)

html = html.replace(
    '.warm{position:absolute;inset:0;z-index:1;pointer-events:none;mix-blend-mode:soft-light;background:radial-gradient(circle calc(var(--r)*.75) at var(--x) var(--y),rgba(255,168,76,.7),rgba(255,168,76,0) 72%)}',
    '.warm{position:absolute;inset:0;z-index:1;pointer-events:none;mix-blend-mode:soft-light;background:radial-gradient(circle calc(var(--r)*.75) at var(--x) var(--y),var(--warm-glow),rgba(255,168,76,0) 72%)}'
)

html = html.replace(
    '.veil{position:absolute;inset:0;z-index:1;pointer-events:none;background:linear-gradient(90deg,rgba(20,12,11,.97) 0%,rgba(20,12,11,.86) 28%,rgba(20,12,11,0) 56%),linear-gradient(0deg,rgba(20,12,11,.92),rgba(20,12,11,0) 24%),linear-gradient(180deg,rgba(20,12,11,.85),rgba(20,12,11,0) 18%)}',
    '.veil{position:absolute;inset:0;z-index:1;pointer-events:none;background:linear-gradient(90deg,var(--veil-1) 0%,var(--veil-2) 28%,transparent 56%),linear-gradient(0deg,var(--veil-1),transparent 24%),linear-gradient(180deg,var(--veil-1),transparent 18%)}'
)

html = html.replace(
    '.hdr.solid{background:rgba(20,12,11,.88);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);border-bottom-color:var(--line)}',
    '.hdr.solid{background:var(--hdr-bg);-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);border-bottom-color:var(--line)}'
)

html = html.replace(
    '.ftr{border-top:1px solid var(--line);padding:64px 0 120px;background:#100908}',
    '.ftr{border-top:1px solid var(--line);padding:64px 0 120px;background:var(--ftr-bg)}'
)

html = html.replace(
    '.plinth{position:relative;aspect-ratio:4/5;border-radius:50% 50% 4px 4px/24% 24% 4px 4px;background:radial-gradient(circle at var(--mx,50%) var(--my,30%),#fdf7ec 0%,#ece0c9 42%,#d3bf9d 100%);overflow:hidden;box-shadow:inset 0 10px 22px rgba(70,40,22,.22)}',
    '.plinth{position:relative;aspect-ratio:4/5;border-radius:50% 50% 4px 4px/24% 24% 4px 4px;background:var(--card-plinth);overflow:hidden;box-shadow:inset 0 10px 22px rgba(70,40,22,.22)}'
)

# Smooth transition for theme toggle
html = html.replace(
    'body{margin:0;background:var(--cellar);color:var(--label);font:400 16px/1.65 var(--sans);-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility}',
    'body{margin:0;background:var(--cellar);color:var(--label);font:400 16px/1.65 var(--sans);-webkit-font-smoothing:antialiased;text-rendering:optimizeLegibility;transition:background-color .35s var(--ease),color .35s var(--ease)}'
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Linked CSS theme variables to cellar wall, plinths, and header!")
