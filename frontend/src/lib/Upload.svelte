<script lang="ts">
  import { enhanceImage } from './api'
  import type { EnhanceResult } from './types'

  let {
    originalImage = $bindable<string | null>(null),
    loading = $bindable(false),
    onresult,          // callback prop — parent passes handleResult function
    onerror            // callback prop — parent passes handleError function
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
      onresult(result)           // call the callback directly — no dispatch needed
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

  function onDragLeave() { dragOver = false }

  function onDrop(event: DragEvent) {
    event.preventDefault()
    dragOver = false
    processFile(event.dataTransfer?.files[0])
  }
</script>