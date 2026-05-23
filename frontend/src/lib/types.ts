// This file defines all shared data types for the project.
// Using types means TypeScript will warn you if you pass wrong data anywhere.

export interface EnhanceResult {
  enhanced_image: string   // base64 data URL: "data:image/png;base64,..."
  psnr: number             // Peak Signal-to-Noise Ratio (higher = better, >30 is good)
  ssim: number             // Structural Similarity Index (0-1, >0.9 is good)
}

export interface MetricsData {
  psnr: number
  ssim: number
}

// Quality label helper type
export type QualityLevel = 'Excellent' | 'Good' | 'Fair' | 'Processing...'