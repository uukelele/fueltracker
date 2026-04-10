<script lang="ts">
    import { client } from "$lib/ephaptic";

    import iconUrl from 'leaflet/dist/images/marker-icon.png';
    import iconRetinaUrl from 'leaflet/dist/images/marker-icon-2x.png';
    import shadowUrl from 'leaflet/dist/images/marker-shadow.png';
    import 'leaflet/dist/leaflet.css';
    import 'leaflet.markercluster/dist/MarkerCluster.css';
    import 'leaflet.markercluster/dist/MarkerCluster.Default.css';

    import { mount, onMount } from "svelte";
    import type { ForecourtRecord } from "$lib/schema";
    import MapPopup from "$lib/components/MapPopup.svelte";
    
    import { type Map } from "leaflet";
    import { type BankHolidayRoot, getBankHolidays } from "$lib/holidays";
    import { createPriceIcon, getPriceColour } from "$lib/utils";


    let forecourts = $state<ForecourtRecord[]>([]);
    let holidays = $state<BankHolidayRoot | null>(null);
    let mapElement = $state<HTMLDivElement>();
    let map = $state<Map>();

    let userLocation = $state<GeolocationCoordinates | null>(null);

    onMount(async () => {
        if (!client || !mapElement) return;

        const L = await import('leaflet');
        (window as any).L = L;
        await import('leaflet.markercluster');

        // delete L.Icon.Default.prototype._getIconUrl;
        const DefaultIcon = L.icon({
            iconUrl,
            iconRetinaUrl,
            shadowUrl,
            iconSize: [25, 41],
            iconAnchor: [12, 41],
            popupAnchor: [1, -34],
            shadowSize: [41, 41]
        });
        
        L.Marker.prototype.options.icon = DefaultIcon;

        map = L.map(mapElement).setView([54.5, -3], 6);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);

        if ('geolocation' in navigator) {
            navigator.geolocation.getCurrentPosition(
                position => { userLocation = position.coords },
                error => console.error,
                { enableHighAccuracy: true, timeout: 5000 }
            )
        }

        const markers = L.markerClusterGroup();

        forecourts = await client.records();
        holidays = await getBankHolidays();

        const allValues = forecourts
            .map(f => {
                const p = f.forecourts.fuel_price.E10;
                const d = f.forecourts.fuel_price.B7S;
                if (p && d) return (p + d) / 2;
                return p || d || null;
            })
            .filter((p): p is number => p !== null && p > 0)
            .sort((a, b) => a - b);
        
        const minPrice = allValues[Math.floor(allValues.length * 0.1)] || allValues[0];
        const maxPrice = allValues[Math.floor(allValues.length * 0.9)] || allValues[allValues.length - 1];

        forecourts.forEach(item => {
            const loc = item.forecourts.location;
            if (loc.latitude && loc.longitude) {
                const marker = L.marker([loc.latitude, loc.longitude]);

                const petrol = item.forecourts.fuel_price.E10;
                const diesel = item.forecourts.fuel_price.B7S;

                let avgPrice: number | null = null;
                if (petrol && diesel) avgPrice = (petrol + diesel) / 2;
                else avgPrice = petrol || diesel || null;

                const colour = getPriceColour(avgPrice, minPrice, maxPrice);

                marker.bindPopup(() => {
                    const container = document.createElement('div');

                    mount(MapPopup, {
                        target: container,
                        props: {
                            record: item,
                            holidays,
                            priceColour: colour,
                        }
                    });

                    return container;
                });

                marker.setIcon(L.icon({
                    iconUrl: createPriceIcon(item.forecourts.fuel_price.E10, item.forecourts.fuel_price.B7S, colour),
                    iconSize: [60, 50],
                    iconAnchor: [30, 50],
                    popupAnchor: [0, -50],
                }));

                // marker.on('mouseover', e => { e.target.openPopup(); });
                // marker.on('mouseout', e => { e.target.closePopup(); });

                markers.addLayer(marker);
            }
        });

        map.addLayer(markers);

        return map.remove;
    });

    $effect(() => {
        if (!userLocation || !map) return;

        const { latitude, longitude } = userLocation;

        map.flyTo([latitude, longitude], 13, {
            animate: true,
            duration: 1.5
        });
    });
</script>

<div
    id="map"
    bind:this={mapElement}
></div>