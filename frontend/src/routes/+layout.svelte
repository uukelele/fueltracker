<script lang="ts">
	import favicon from '$lib/assets/favicon.svg';

	import '$lib/styles/styles.css';

	let { children } = $props();
</script>

<svelte:head>
	<link rel="icon" href={favicon} />
	<title>FuelTracker</title>
</svelte:head>

{@render children()}
