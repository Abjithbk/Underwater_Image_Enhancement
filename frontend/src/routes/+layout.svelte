<script lang="ts">
  import '../app.css'
</script>

<div class="min-h-screen bg-[#050d1a] text-slate-200 flex flex-col">


  <header class="bg-[#0a1628] border-b border-slate-800 px-6 py-4 flex items-center justify-between">

    <div class="flex items-center gap-3">
      <div class="w-8 h-8 rounded-lg bg-cyan-500/20 flex items-center justify-center text-xl">
        🌊
      </div>
      <span class="text-cyan-400 font-bold text-lg tracking-tight">
        Underwater Enhancer
      </span>
    </div>

    <span class="text-slate-500 text-sm hidden sm:block">
   
      AI-powered image clarity restoration
    </span>
  </header>

  <main class="flex-1 max-w-5xl w-full mx-auto px-4 py-8">
    <slot />
    <!-- SvelteKit puts +page.svelte content here -->
  </main>

  <footer class="border-t border-slate-800 py-4 text-center text-slate-600 text-xs">
    Powered by U-Net · FastAPI · SvelteKit
  </footer>

</div>