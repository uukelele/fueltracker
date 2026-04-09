export interface BankHolidayEvent {
    title: string;
    date: string; // YYYY-MM-DD
    notes: string;
    bunting: boolean;
}

export interface BankHolidayRoot {
    "england-and-wales": { division: string; events: BankHolidayEvent[] };
    "scotland": { division: string; events: BankHolidayEvent[] };
    "northern-ireland": { division: string; events: BankHolidayEvent[] };
}

export async function getBankHolidays(): Promise<BankHolidayRoot> {
    const res = await fetch("https://www.gov.uk/bank-holidays.json");
    return res.json();
}

export function getDivision(country: string | null): keyof BankHolidayRoot {
    const c = country?.toLowerCase() || "";
    if (c.includes("scotland")) return "scotland";
    if (c.includes("ireland")) return "northern-ireland";
    return "england-and-wales";
}