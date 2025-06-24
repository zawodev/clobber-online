<template>
    <div>
        <p>Authenticating…</p>
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import api from '@/api'
import router from '@/router'
async function handleSSOCallback() {
  try {
    // 1) Exchange session cookie for token
    const { data } = await api.get('/users/token/', {
      withCredentials: true
    });
    const token = data.token;
    console.log('returned token:', data);

    // 2) Persist token & configure axios
    sessionStorage.setItem('token', token);
    api.defaults.headers.common['Authorization'] = `Token ${token}`;

    // 3) Fetch current user
    const { data: me } = await api.get('/users/me/');
    sessionStorage.setItem('username', me.username);

    // 4) Redirect
    router.push('/home');
  } catch (err) {
    console.error('Failed to fetch SSO token or user:', err);
  }
}

onMounted(async () => {
    handleSSOCallback();
})
</script>