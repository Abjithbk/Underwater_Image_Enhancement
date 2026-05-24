<script lang="ts">
  import { enhanceImage } from './api'
  import type { EnhanceResult } from './types'

  let {
    originalImage = $bindable<string | null>(null),
    loading = $bindable(false),
    onresult,
    onerror
  } = $props<{
    originalImage: string | null
    loading: boolean
    onresult: (data: EnhanceResult) => void
    onerror: (data: { message: string }) => void
  }>()

  let dragOver = $state(false)

  async function processFile(file: File | null | undefined) {
    if (!file) return
    if (!file.type.startsWith('image/')) {
      onerror({ message: 'Please upload an image file' })
      return
    }
    originalImage = URL.createObjectURL(file)
    loading = true
    try {
      const result = await enhanceImage(file)
      onresult(result)
    } catch (err) {
      onerror({ message: err instanceof Error ? err.message : 'Unknown error' })
      originalImage = null
    } finally {
      loading = false
    }
  }

  function onFileInput(event: Event) {
    const input = event.target as HTMLInputElement
    processFile(input.files?.[0])
    input.value = ''
  }

  function onDragOver(event: DragEvent) {
    event.preventDefault()
    dragOver = true
  }

  function onDragLeave() {
    dragOver = false
  }

  function onDrop(event: DragEvent) {
    event.preventDefault()
    dragOver = false
    processFile(event.dataTransfer?.files[0])
  }
</script>

<div
  class="relative rounded-2xl border-2 border-dashed transition-all duration-200
         overflow-hidden min-h-[200px] flex items-center justify-center cursor-pointer
         {dragOver ? 'border-cyan-400 bg-cyan-950/20' : 'border-slate-700 bg-[#0a1628]'}
         {originalImage ? 'border-solid border-slate-700 p-0' : 'p-10'}"
  ondragover={onDragOver}
  ondragleave={onDragLeave}
  ondrop={onDrop}
  role="button"
  tabindex="0"
>

  {#if originalImage}
    <img
      src={originalImage}
      alt="Original underwater"
      class="w-full max-h-72 object-cover"
    />
    <div class="absolute bottom-3 right-3">
      <label class="bg-slate-900/80 border border-slate-600 text-slate-300
                    text-xs px-3 py-1.5 rounded-lg cursor-pointer
                    hover:border-cyan-500 hover:text-cyan-400
                    transition-colors backdrop-blur-sm">
        Change image
        <input type="file" accept="image/*" class="hidden" onchange={onFileInput} />
      </label>
    </div>

  {:else}
    <div class="flex flex-col items-center gap-3 text-center">
      <div class="w-14 h-14 rounded-full bg-slate-800 flex items-center justify-center text-2xl">
        📁
      </div>
      <div>
        <p class="text-slate-300 font-medium">Drag & drop an underwater image</p>
        <p class="text-slate-500 text-sm mt-1">or click to browse your files</p>
      </div>
      <label class="mt-2 bg-cyan-600 hover:bg-cyan-500 text-white
                    text-sm font-medium px-5 py-2 rounded-lg
                    cursor-pointer transition-colors">
        Browse files
        <input type="file" accept="image/*" class="hidden" onchange={onFileInput} />
      </label>
      <p class="text-slate-600 text-xs">Supports JPG, PNG, WEBP</p>
    </div>
  {/if}

</div>