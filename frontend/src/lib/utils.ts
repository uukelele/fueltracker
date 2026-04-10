const pad = (n: number) => n.toString().padStart(2, '0');

export function formatDate(isoString: string): string {
    const date = new Date(isoString);
    const now = new Date();

    const timeStr = `${pad(date.getHours())}:${pad(date.getMinutes())}`;

    if (date.toDateString() === now.toDateString()) {
        return `Today at ${timeStr}`;
    }

    const yesterday = new Date(now);
    yesterday.setDate(now.getDate() - 1);
    
    if (date.toDateString() === yesterday.toDateString()) {
        return `Yesterday at ${timeStr}`;
    }

    const sixDaysAgo = new Date(now);
    sixDaysAgo.setDate(now.getDate() - 6);

    sixDaysAgo.setHours(0, 0, 0, 0);

    if (date > sixDaysAgo) {
        const weekday = date.toLocaleDateString(undefined, { weekday: 'long' });
        return `${weekday} at ${timeStr}`;
    }

    const day = pad(date.getDate());
    const month = pad(date.getMonth() + 1);
    const year = date.getFullYear();

    return `${day}/${month}/${year} at ${timeStr}`;
}

export function getPriceColour(price: number | null, min: number, max: number) {
    if (!price) return '#616161';

    const clamped = Math.max(min, Math.min(max, price));

    const ratio = Math.pow((clamped - min) / (max - min), 1.2);

    const hue = (1 - ratio) * 120;

    return `hsl(${hue}, 70%, 45%)`;
}

export function createPriceIcon(petrol: number | null, diesel: number | null, color: string) {
    const svg = `
        <svg width="60" height="50" viewBox="0 0 60 50" xmlns="http://www.w3.org/2000/svg">
            <path d="M30 50 L10 35 H50 Z" fill="rgba(0,0,0,0.2)" transform="translate(2,2)" />
            <rect x="0" y="0" width="60" height="36" rx="6" fill="${color}" />
            <path d="M30 50 L20 35 H40 Z" fill="${color}" />
            <text x="5" y="15" fill="white" font-family="sans-serif" font-weight="bold" font-size="10">P</text>
            <text x="55" y="15" fill="white" font-family="sans-serif" font-weight="bold" font-size="11" text-anchor="end">${petrol ? petrol.toFixed(1) : '—'}</text>
            
            <rect x="5" y="19" width="50" height="1" fill="white" fill-opacity="0.3" />
            
            <text x="5" y="30" fill="white" font-family="sans-serif" font-weight="bold" font-size="10">D</text>
            <text x="55" y="30" fill="white" font-family="sans-serif" font-weight="bold" font-size="11" text-anchor="end">${diesel ? diesel.toFixed(1) : '—'}</text>
        </svg>
    `.trim();

    return `data:image/svg+xml;charset=UTF-8,${encodeURIComponent(svg)}`;
}