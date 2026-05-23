import type { EnhanceResult } from './types'

// VITE_ prefix is required for SvelteKit to expose env vars to the browser
const BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8000'

/**
 * Sends an image file to FastAPI and returns the enhancement result.
 * Throws a typed Error if the request fails.
 */
export async function enhanceImage(file: File): Promise<EnhanceResult> {
  // FormData is how browsers send files over HTTP (multipart/form-data)
  // Never set Content-Type manually — browser sets it with the boundary string
  const formData = new FormData()
  formData.append('file', file)

  const response = await fetch(`${BASE_URL}/api/enhance`, {
    method: 'POST',
    body: formData
  })

  if (!response.ok) {
    // FastAPI sends errors as { detail: "..." }
    const err = await response.json().catch(() => ({}))
    throw new Error((err as { detail?: string }).detail ?? `Server error ${response.status}`)
  }

  return response.json() as Promise<EnhanceResult>
}