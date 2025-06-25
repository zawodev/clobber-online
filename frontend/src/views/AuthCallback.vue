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
    const { data } = await api.get('/users/token/', {
      withCredentials: true
    });
    const token = data.token;
    console.log('returned token:', data);

    sessionStorage.setItem('token', token);
    api.defaults.headers.common['Authorization'] = `Token ${token}`;

    const { data: me } = await api.get('/users/me/');
    sessionStorage.setItem('username', me.username);

    router.push('/home');
  } catch (err) {
    console.error('Failed to fetch SSO token or user:', err);
  }
}

onMounted(async () => {
    handleSSOCallback();
})
</script>