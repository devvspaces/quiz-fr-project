<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-dark bg-primary">
      <div class="container">
        <RouterLink class="navbar-brand" to="/">Quiz App</RouterLink>
        <div class="navbar-nav ms-auto">
          <RouterLink class="nav-link" to="/">Home</RouterLink>
          <RouterLink class="nav-link" to="/admin">Admin</RouterLink>
        </div>
      </div>
    </nav>

    <main class="container mt-4">
      <RouterView />
    </main>
  </div>
</template>

<style scoped>
.router-link-active {
  font-weight: bold;
}
</style>