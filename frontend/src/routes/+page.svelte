<script lang="ts">
  import Upload from '$lib/Upload.svelte'
  import Preview from '$lib/Preview.svelte'
  import Metrics from '$lib/Metrics.svelte'
  import type { EnhanceResult, MetricsData } from '$lib/types'

  // $state() = reactive variable
  // when these change, any part of UI using them re-renders automatically
  let originalImage = $state<string | null>(null)
  let enhancedImage = $state<string | null>(null)
  let metrics = $state<MetricsData>({ psnr: 0, ssim: 0 })
  let loading = $state(false)
  let error = $state<string | null>(null)

  // called by Upload when backend responds with enhanced image
  function handleResult(data: EnhanceResult) {
    enhancedImage = data.enhanced_image  // base64 image string
    metrics = { psnr: data.psnr, ssim: data.ssim }
    error = null
  }

  // called by Upload when backend call fails
  function handleError(data: { message: string }) {
    error = data.message
    loading = false
  }

  // reset everything for a fresh upload
  function reset() {
    originalImage = null
    enhancedImage = null
    metrics = { psnr: 0, ssim: 0 }
    error = null
    loading = false
  }
</script>

<div class="flex flex-col gap-8">


  <!-- HERO SECTION -->
  <div class="text-center py-4">
    <h1 class="text-3xl font-extrabold text-cyan-400 mb-2">

      Restore Underwater Clarity
    </h1>
    <p class="text-slate-400 text-sm max-w-md mx-auto">

      Upload an underwater image — AI removes haze, fixes color distortion, and reduces noise.
    </p>
  </div>

  <!-- UPLOAD COMPONENT — always visible -->
  <Upload
    bind:originalImage
    bind:loading
    onresult={handleResult}
    onerror={handleError}
  />

  <!-- ERROR BANNER — only shows when error has a value -->
  {#if error}
    <div class="bg-red-950 border border-red-700 text-red-300 px-4 py-3 rounded-xl text-sm flex items-center gap-2">

      <span class="text-red-400 font-bold">Error:</span>
      {error}
    </div>
  {/if}

  <!-- LOADING SPINNER — only shows when loading is true -->
  {#if loading}
    <div class="flex items-center gap-4 bg-[#0a1628] border border-slate-800 rounded-xl px-5 py-4">
      <div class="w-6 h-6 border-2 border-slate-700 border-t-cyan-400 rounded-full animate-spin">

      </div>
      <div>
        <p class="text-slate-300 text-sm font-medium">Enhancing your image with AI...</p>
        <p class="text-slate-500 text-xs mt-0.5">Running U-Net inference</p>
      </div>
    </div>
  {/if}

  
  {#if enhancedImage}
    <div class="flex flex-col gap-6">
      <div class="flex items-center justify-between">
        <h2 class="text-slate-300 font-semibold text-lg">Enhancement Results</h2>
        <button
          onclick={reset}
          class="text-sm text-slate-400 border border-slate-700 px-4 py-1.5 rounded-lg
                 hover:border-cyan-500 hover:text-cyan-400 transition-colors"
        >
   
          Try another image
        </button>
      </div>

      <Preview {originalImage} {enhancedImage} />
      <Metrics {metrics} />
    </div>
  {/if}

</div>