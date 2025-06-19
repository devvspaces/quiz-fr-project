<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import participationStorageService from "@/services/ParticipationStorageService";

const router = useRouter();
const username = ref('');

function launchNewQuiz() {
  if (!username.value.trim()) {
    alert('Please enter your name');
    return;
  }
  
  participationStorageService.savePlayerName(username.value);
  router.push('/questions');
}
</script>

<template>
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card">
        <div class="card-header">
          <h2 class="card-title mb-0">Start Your Quiz</h2>
        </div>
        <div class="card-body">
          <form @submit.prevent="launchNewQuiz">
            <div class="mb-3">
              <label for="playerName" class="form-label">Enter your name:</label>
              <input 
                type="text" 
                id="playerName"
                v-model="username" 
                class="form-control"
                placeholder="Your name here..."
                required
              />
            </div>
            
            <div class="d-grid">
              <button type="submit" class="btn btn-success btn-lg">
                Start Quiz
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>