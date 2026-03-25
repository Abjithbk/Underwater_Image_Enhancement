<script lang="ts">
    let file = $state<File | null>(null);

    let previewUrl = $state<string|null>(null);

    function handleFile(e : Event) {
        const input = e.target as HTMLInputElement;
        const selectedFile = input.files?.[0];

        if(selectedFile) {
            file = selectedFile;
            previewUrl = URL.createObjectURL(selectedFile);
        }
    }

</script>

<div class="flex flex-col items-center justify-center min-h-screen gap-6">
  <h1 class="text-2xl font-bold">Image Upload</h1>

  <!-- File Input -->
  <input 
    type="file" 
    accept="image/*"
    class="border p-2 rounded"
    onchange={handleFile}
  />

  <!-- Preview -->
  {#if previewUrl}
    <div class="mt-4">
      <p class="text-lg mb-2">Preview:</p>
      <img 
        src={previewUrl} 
        alt="Preview" 
        class="w-64 h-auto rounded shadow"
      />
    </div>
  {/if}
</div>
