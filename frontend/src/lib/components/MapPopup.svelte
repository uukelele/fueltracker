<script lang="ts">
    import { getDivision, type BankHolidayRoot } from "$lib/holidays";
	import type { ForecourtRecord } from "$lib/schema";
    import { formatDate } from "$lib/utils";

	interface Props {
		record: ForecourtRecord;
        holidays: BankHolidayRoot | null;
        priceColour: string;
	}

	const { record, holidays, priceColour }: Props = $props();

	const f = record.forecourts;
	const prices = f.fuel_price;

	const formatPrice = (val: number | null) => (val ? val.toFixed(1) + "p" : "—");

	const isOpen24 =
		f.amenities.twenty_four_hour_fuel ||
		f.opening_times.usual_days.monday.is_24_hours;

    const isOpenNow = $derived.by<boolean>(() => {
        if (f.amenities.twenty_four_hour_fuel) return true;

        const now = new Date();
        const currentTimeStr = now.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' }); // HH:MM
        const todayISO = now.toISOString().split('T')[0]; // YYYY-MM-DD

        let sched = f.opening_times.usual_days[
            now.toLocaleDateString('en-GB', { weekday: 'long' }).toLowerCase() as keyof typeof f.opening_times.usual_days
        ];

        if (holidays) {
            const div = getDivision(f.location.country);
            const isBH = holidays[div].events.some(e => e.date === todayISO);

            if (isBH) {
                const bhSched = f.opening_times.bank_holiday.standard;
                if (bhSched.open_time || bhSched.is_24_hours) {
                    sched = bhSched as any;
                }
            }
        }

        if (sched.is_24_hours) return true;
        if (!sched.open_time || !sched.close_time) return true;

        return currentTimeStr >= sched.open_time && currentTimeStr <= sched.close_time;
    });
</script>

<div class="forecourt-popup">
	<header>
        <div class="status-bar">
            {#if isOpenNow}
                <span class="open">● OPEN NOW</span>
            {:else}
                <span class="closed">○ CLOSED</span>
            {/if}
        </div>
		<div class="brand-info">
			<span class="brand">{f.brand_name || f.trading_name || "Unknown Station"}</span>
			{#if isOpen24}
				<span class="badge-24h">24h</span>
			{/if}
		</div>
		<p class="address">{f.location.address_line_1}, {f.location.postcode}</p>
	</header>

	<div class="price-grid">
		<div class="fuel-group">
			<div class="label">PETROL</div>
			<div class="price-row">
				<span class="type">E10</span>
				<span class="value" style:color={priceColour}>{formatPrice(prices.E10)}</span>
			</div>
			{#if prices.E5}
				<div class="price-row premium">
					<span class="type">E5 (Prem)</span>
					<span class="value" style:color={priceColour}>{formatPrice(prices.E5)}</span>
				</div>
			{/if}
		</div>

		<div class="fuel-group">
			<div class="label">DIESEL</div>
			<div class="price-row">
				<span class="type">B7</span>
				<span class="value" style:color={priceColour}>{formatPrice(prices.B7S)}</span>
			</div>
			{#if prices.B7P}
				<div class="price-row premium">
					<span class="type">B7 (Prem)</span>
					<span class="value" style:color={priceColour}>{formatPrice(prices.B7P)}</span>
				</div>
			{/if}
		</div>
	</div>

	<footer>
		<div class="amenities">
			{#if f.amenities.fuel_and_energy_services.adblue_pumps}
				<span title="AdBlue at Pump">💧 AdBlue</span>
			{/if}
			{#if f.amenities.vehicle_services.car_wash}
				<span title="Car Wash">🚗 Wash</span>
			{/if}
            {#if f.amenities.customer_toilets}
                <span title="Customer Toilets">🚽 Toilets</span>
            {/if}
			{#if f.amenities.air_pump_or_screenwash}
				<span title="Air/Water">💨 Air</span>
			{/if}
            <a href={`https://www.google.com/maps/dir/?api=1&destination=${f.location.latitude},${f.location.longitude}`}>Get Directions</a>
		</div>
		{#if record.forecourt_update_timestamp}
			<div class="updated">
				Updated: {formatDate(record.forecourt_update_timestamp)}
			</div>
		{/if}
	</footer>
</div>

<style>
	.forecourt-popup {
		min-width: 220px;
		font-family:
			system-ui,
			-apple-system,
			sans-serif;
		color: #1a1a1a;
	}

	header {
		margin-bottom: 12px;
		border-bottom: 1px solid #eee;
		padding-bottom: 8px;
	}

	.brand-info {
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 8px;
	}

	.brand {
		font-weight: 800;
		font-size: 1.1rem;
		text-transform: uppercase;
		color: #2c3e50;
	}

    .open,
    .closed {
        font-family: 'ui-monospace', monospace;
    }

    .open {
        color: green;
    }

    .closed {
        color: red;
    }

	.badge-24h {
		background: #27ae60;
		color: white;
		font-size: 0.7rem;
		padding: 2px 6px;
		border-radius: 4px;
		font-weight: bold;
	}

	.address {
		margin: 2px 0 0 0;
		font-size: 0.75rem;
		color: #666;
	}

	.price-grid {
		display: grid;
		grid-template-columns: 1fr 1fr;
		gap: 12px;
		margin-bottom: 12px;
	}

	.fuel-group {
		display: flex;
		flex-direction: column;
	}

	.label {
		font-size: 0.65rem;
		font-weight: bold;
		color: #95a5a6;
		margin-bottom: 4px;
		letter-spacing: 0.05em;
	}

	.price-row {
		display: flex;
		justify-content: space-between;
		align-items: baseline;
		padding: 4px 0;
	}

	.type {
		font-size: 0.7rem;
		font-weight: 600;
	}

	.value {
		font-size: 1.1rem;
		font-weight: 800;
	}

	.premium .value {
        font-size: 1rem;
        font-weight: 600;
	}

	.premium .type {
		color: #7f8c8d;
		font-style: italic;
	}

	footer {
		border-top: 1px solid #eee;
		padding-top: 8px;
	}

	.amenities {
		display: flex;
		flex-wrap: wrap;
		gap: 6px;
		margin-bottom: 6px;
	}

	.amenities span {
		font-size: 0.65rem;
		background: #f8f9fa;
		padding: 2px 5px;
		border-radius: 3px;
		border: 1px solid #e9ecef;
	}

	.updated {
		font-size: 0.6rem;
		color: #bdc3c7;
		text-align: right;
	}
</style>