<script lang="ts">
  let { originalImage, enhancedImage } = $props<{
    originalImage: string | null
    enhancedImage: string | null
  }>()

  let sliderValue = $state(50)   // reactive local state in Svelte 5

  // $derived() replaces $: reactive statements
  const clipStyle = $derived(`inset(0 ${100 - sliderValue}% 0 0)`)
</script>