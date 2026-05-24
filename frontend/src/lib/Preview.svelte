<script lang="ts">
  let { originalImage, enhancedImage } = $props<{
    originalImage: string | null
    enhancedImage: string | null
  }>()

  // slider position 0-100
  // 50 = show 50% original / 50% enhanced
  let sliderValue = $state(50)

  // auto-recalculates when sliderValue changes
  // inset(top right bottom left)
  // right value clips from the right side
  // so inset(0 40% 0 0) shows 60% of image from left
  const clipStyle = $derived(`inset(0 ${100 - sliderValue}% 0 0)`)
</script>

<div class="flex flex-col gap-4">

  <div class="rounded-xl overflow-hidden border border-slate-800 bg-[#0a1628]">

    <!-- TOP BAR -->
    <div class="px-4 py-2 border-b border-slate-800 flex items-center justify-between">
      <span class="text-slate-400 text-sm font-medium">Drag slider to compare</span>
      <span class="text-slate-600 text-xs">{sliderValue}%</span>
    </div>

    <!-- COMPARISON AREA -->
    {#if originalImage && enhancedImage}
    <div class="relative w-full aspect-video select-none">


      <!-- LAYER 1: enhanced image (bottom layer, always fully visible) -->
      <div class="absolute inset-0">
   
        <img src={enhancedImage} alt="Enhanced" class="w-full h-full object-cover" />
        <span class="absolute bottom-3 right-3 bg-cyan-900/80 text-cyan-300 text-xs px-2 py-1 rounded-full">
          Enhanced
        </span>
      </div>

      <!-- LAYER 2: original image (top layer, clipped by slider) -->
      <div class="absolute inset-0" style="clip-path: {clipStyle}">
    
        <img src={originalImage} alt="Original" class="w-full h-full object-cover" />
        <span class="absolute bottom-3 left-3 bg-slate-900/80 text-slate-300 text-xs px-2 py-1 rounded-full">
          Original
        </span>
      </div>

      <!-- DIVIDER LINE at slider position -->
      <div
        class="absolute top-0 bottom-0 w-0.5 bg-white pointer-events-none z-10"
        style="left: {sliderValue}%"
      >
    
        <div class="absolute top-1/2 -translate-x-1/2 -translate-y-1/2
                    w-8 h-8 bg-white rounded-full shadow-lg
                    flex items-center justify-center
                    text-slate-700 text-xs font-bold">
        
          ⇄
        </div>
      </div>

      <!-- INVISIBLE RANGE INPUT — captures all drag events -->
      <input
        type="range"
        min="0" max="100"
        bind:value={sliderValue}
        class="absolute inset-0 w-full h-full opacity-0 cursor-ew-resize z-20"

      />
    </div>
    {/if}
  </div>

  <!-- SIDE BY SIDE VIEW -->
  {#if originalImage && enhancedImage}
  <div class="grid grid-cols-2 gap-3">
 
    <div class="rounded-xl overflow-hidden border border-slate-800">
      <div class="bg-slate-800/50 px-3 py-1.5 text-xs text-slate-400 font-medium">
        Original
      </div>
      <img src={originalImage} alt="Original" class="w-full object-cover" />
    </div>
    <div class="rounded-xl overflow-hidden border border-cyan-900/50">
      <div class="bg-cyan-900/20 px-3 py-1.5 text-xs text-cyan-400 font-medium">
        Enhanced
      </div>
      <img src={enhancedImage} alt="Enhanced" class="w-full object-cover" />
    </div>
  </div>
  {/if}

</div>