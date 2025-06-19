<script setup>
import { ref, onMounted } from 'vue';
import quizApiService from "@/services/QuizApiService";

const registeredScores = ref([]);

onMounted(async () => {
  try {
    const response = await quizApiService.getQuizInfo();
    registeredScores.value = response.data.scores;
  } catch (error) {
    console.error("Failed to load quiz info:", error);
  }
});
</script>

<template>
  <div class="row">
    <div class="col-md-8">
      <h1>Welcome to the Quiz!</h1>
      <p class="lead">Test your knowledge with our interactive quiz.</p>
      
      <div class="text-center">
        <router-link to="/new-quiz" class="btn btn-primary btn-lg">
          Start the Quiz!
        </router-link>
      </div>
    </div>
    
    <div class="col-md-4">
      <h3>Best Scores</h3>
      <div v-if="registeredScores.length === 0" class="text-muted">
        No scores yet. Be the first to take the quiz!
      </div>
      <div v-else>
        <div 
          v-for="scoreEntry in registeredScores" 
          :key="scoreEntry.date"
          class="card mb-2"
        >
          <div class="card-body py-2">
            <div class="d-flex justify-content-between">
              <strong>{{ scoreEntry.playerName }}</strong>
              <span class="badge bg-primary">{{ scoreEntry.score }}</span>
            </div>
            <small class="text-muted">{{ scoreEntry.date }}</small>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>