<template>
  <div>
    <h2>Rejestracja</h2>
    <form @submit.prevent="submitRegister">
      <label>Login:</label>
      <input v-model="userForm.username" type="text" required />

      <label>Hasło:</label>
      <input v-model="userForm.password" type="password" required />

      <label>Email:</label>
      <input v-model="userForm.email" type="email" required />

      <button type="submit">Zarejestruj się</button>
    </form>
    <p>Masz już konto? <router-link to="/">Zaloguj się</router-link></p>
  </div>
</template>

<script>
import api from "@/api"
export default {
  data() {
    return {
      userForm: {
        username: '',
        email: '',
        password: ''
      }
    }
  },
  methods: {
    submitRegister() {
      api.post("/users/register/", this.userForm)
        .then(response => {
          const data = response.data;

          localStorage.setItem("username", data.username);

          alert("Rejestracja zakończona pomyślnie!");
          this.$router.push("/");

        })
        .catch(error => {
          if (error.response && error.response.status === 400) {
            const data = error.response.data;

            // Obsługa znanych błędów walidacyjnych
            if (data.username ) {
              alert(data.username[0]);
            } else if (data.email) {
              alert(data.email[0]);
            } else if (data.password) {
              alert(data.password[0]);
            } else {
              alert("Nieprawidłowe dane rejestracyjne.");
            }
          } else {
            alert("Błąd połączenia z serwerem.");
            console.error(error);
          }
        });
      console.log('Rejestracja:', this.userForm.username, this.userForm.password, this.userForm.email)
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
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
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