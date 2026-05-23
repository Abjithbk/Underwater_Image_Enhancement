<script lang="ts">
  import type { MetricsData, QualityLevel } from './types'

  // $props() replaces export let
  let { metrics } = $props<{ metrics: MetricsData }>()

  // $derived() replaces $: for computed values
  const psnrLabel = $derived(getPsnrLabel(metrics.psnr))
  const ssimLabel = $derived(getSsimLabel(metrics.ssim))
  const psnrColor = $derived(
    metrics.psnr > 40 ? 'text-green-400' :
    metrics.psnr > 30 ? 'text-yellow-400' : 'text-red-400'
  )
  const ssimColor = $derived(
    metrics.ssim > 0.9 ? 'text-green-400' :
    metrics.ssim > 0.7 ? 'text-yellow-400' : 'text-red-400'
  )

  // Functions must be defined BEFORE $derived() uses them
  function getPsnrLabel(val: number): QualityLevel {
    if (val === 0) return 'Processing...'
    if (val > 40) return 'Excellent'
    if (val > 30) return 'Good'
    return 'Fair'
  }

  function getSsimLabel(val: number): QualityLevel {
    if (val === 0) return 'Processing...'
    if (val > 0.9) return 'Excellent'
    if (val > 0.7) return 'Good'
    return 'Fair'
  }
</script>

<div class="bg-[#0a1628] border border-slate-800 rounded-xl p-5">
  <h3 class="text-slate-400 text-sm font-medium mb-4">Quality Metrics</h3>

  <div class="grid grid-cols-2 gap-4">

    <!-- PSNR card -->
    <div class="bg-slate-900/60 rounded-xl p-4 border border-slate-800">
      <div class="flex items-start justify-between mb-1">
        <span class="text-slate-500 text-xs uppercase tracking-widest">PSNR</span>
        <span class="text-xs px-2 py-0.5 rounded-full bg-slate-800 {psnrColor}">
          {psnrLabel}
        </span>
      </div>
      <p class="text-2xl font-bold {psnrColor}">
        {metrics.psnr > 0 ? metrics.psnr.toFixed(1) : '—'}
        <span class="text-sm font-normal text-slate-500">dB</span>
      </p>
      <p class="text-slate-600 text-xs mt-2">
        Peak Signal-to-Noise Ratio · &gt;30 dB is acceptable
      </p>
    </div>

    <!-- SSIM card -->
    <div class="bg-slate-900/60 rounded-xl p-4 border border-slate-800">
      <div class="flex items-start justify-between mb-1">
        <span class="text-slate-500 text-xs uppercase tracking-widest">SSIM</span>
        <span class="text-xs px-2 py-0.5 rounded-full bg-slate-800 {ssimColor}">
          {ssimLabel}
        </span>
      </div>
      <p class="text-2xl font-bold {ssimColor}">
        {metrics.ssim > 0 ? metrics.ssim.toFixed(3) : '—'}
      </p>
      <p class="text-slate-600 text-xs mt-2">
        Structural Similarity · &gt;0.9 is high quality
      </p>
    </div>

  </div>

  <!-- Interpretation guide -->
  <div class="mt-4 pt-4 border-t border-slate-800 grid grid-cols-3 gap-2 text-xs text-center">
    <div>
      <span class="text-green-400 font-medium">Excellent</span>
      <p class="text-slate-600 mt-0.5">PSNR &gt;40 · SSIM &gt;0.9</p>
    </div>
    <div>
      <span class="text-yellow-400 font-medium">Good</span>
      <p class="text-slate-600 mt-0.5">PSNR &gt;30 · SSIM &gt;0.7</p>
    </div>
    <div>
      <span class="text-red-400 font-medium">Fair</span>
      <p class="text-slate-600 mt-0.5">PSNR &lt;30 · SSIM &lt;0.7</p>
    </div>
  </div>
</div>