<template>
  <div>
    <h2>Logowanie</h2>
    <form @submit.prevent="submitLogin">
      <label>Login:</label>
      <input v-model="LoginInfo.username" type="text" required />

      <label>Hasło:</label>
      <input v-model="LoginInfo.password" type="password" required />

      <button class type="submit" @click="submitLogin" >Zaloguj</button>
    </form>
    <p>Nie masz konta? <router-link to="/register">Zarejestruj się</router-link></p>
  </div>
</template>

<script>
import api from '@/api'
export default {
  data() {
    return {
      LoginInfo:{
      username: '',
      password: ''
      }
    }
  },
  methods: {
    submitLogin() {
      api.post("/users/login/",this.LoginInfo)
        .then(response => {
          const data = response.data;
          localStorage.setItem("token", data.token);
          localStorage.setItem("username", this.LoginInfo.username);
          this.$router.push('/home');
        })
        .catch(error => {
          if (error.response && error.response.status === 400) {
            const data = error.response.data;
            if (data.error ) {
              alert(data.error[0]);
            } 
          }
        })
      console.log('Logowanie:', this.login, this.password)
    }
  }
}
</script>

<style scoped>
form {
  background-color: white;
  padding: 20px;
  margin: 50px auto;
  width: 300px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

h2 {
  text-align: center;
  margin-bottom: 20px;
}

label {
  display: block;
  margin-top: 10px;
  margin-bottom: 5px;
  font-weight: bold;
}

input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
  border-radius: 4px;
  border: 1px solid #ccc;
}

button {
  margin-top: 15px;
  width: 100%;
  padding: 10px;
  background-color: #3498db;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
}


button:hover {
  background-color: #2980b9;
}

p {
  text-align: center;
  margin-top: 15px;
}

a {
  color: #3498db;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>