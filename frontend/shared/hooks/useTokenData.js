/*
import { useQuery } from '@tanstack/react-query';
import { invoke } from '@tauri-apps/api/core';
import { loadToken } from '@/store/tauri_store';

export async function fetchWithToken(url) {
  const token = await loadToken();
  if (!token) throw new Error('No token available');
  return invoke('fetch_data', { url, token });
}

export async function fetchWithTokenFrontend(url) {
  const token = await loadToken();
  if (!token) throw new Error('No token available');
  
  const response = await fetch(url, {
    headers: {
      'Authorization': `Token ${token}`
    }
  });
  
  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }
  
  return await response.json();
}

export function useTokenData(url) {
  console.log('useTokenData hook called for:', url);
  const normalizedUrl = new URL(url).toString(); // Removes potential variations
  return useQuery({
    queryKey: ['api-data', normalizedUrl], // Unique key for caching
    queryFn: () => fetchWithToken(url),
    staleTime: 5 * 60 * 1000, // Cache data for 5 minutes
  });
}
  */