import type { EnhanceResult } from "./types";

const BASE_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

/*
In this, this function takes the image given by the user and
sends it to the backend . Backend will return the enhanced image
otherwise throw an error
*/

export async function enhanceImage(file:File)  :Promise<EnhanceResult> {

  const formData = new FormData();
  formData.append('file',file);

  const response = await fetch(`${BASE_URL}/api/enhance`,{
    method:'POST',
    body:formData,
  })

  if(!response.ok) {
    const err = await response.json().catch(() => ({}));//return an empty object if error comes

    throw new Error(
      (err as {detail? : string}).detail??`Server error ${response.status}`
    )
  }

  return response.json() as Promise<EnhanceResult>;

  
}