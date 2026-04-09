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
    
    import type { Map } from "leaflet";
    import { type BankHolidayRoot, getBankHolidays } from "$lib/holidays";


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

        forecourts.forEach(item => {
            const loc = item.forecourts.location;
            if (loc.latitude && loc.longitude) {
                const marker = L.marker([loc.latitude, loc.longitude]);

                marker.bindPopup(() => {
                    const container = document.createElement('div');

                    mount(MapPopup, {
                        target: container,
                        props: { record: item, holidays }
                    });

                    return container;
                });

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