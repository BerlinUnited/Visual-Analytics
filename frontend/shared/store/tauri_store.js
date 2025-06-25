import { load } from '@tauri-apps/plugin-store';

const store = await load('store.json', { autoSave: true });

export async function saveToken(token){
  await store.set('api-token', { value: token });
  await store.save();
}

export async function loadToken(){
    const token = await store.get('api-token');

    return token?.value || null;
}

export async function saveLogRoot(log_root){
  await store.set('log_root', { value: log_root });
  await store.save();
}

export async function loadLogRoot(){
    const token = await store.get('log_root');

    return token?.value || null;
}