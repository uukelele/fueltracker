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