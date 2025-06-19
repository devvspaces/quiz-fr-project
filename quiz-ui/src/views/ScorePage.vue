<script setup>
import { ref, onMounted } from 'vue';
import participationStorageService from "@/services/ParticipationStorageService";
import quizApiService from "@/services/QuizApiService";

const participationScore = ref(null);
const updatedScores = ref([]);

onMounted(async () => {
  participationScore.value = participationStorageService.getParticipationScore();
  
  try {
    const response = await quizApiService.getQuizInfo();
    updatedScores.value = response.data.scores;
  } catch (error) {
    console.error("Failed to load updated scores:", error);
  }
});

function goHome() {
  participationStorageService.clear();
}
</script>

<template>
  <div class="row justify-content-center">
    <div class="col-md-8">
      <div class="text-center">
        <h1 class="display-4 mb-4">Quiz Complete!</h1>
        
        <div v-if="participationScore" class="card mb-4">
          <div class="card-body">
            <h2 class="card-title">{{ participationScore.playerName }}</h2>
            <div class="display-1 text-primary">
              {{ participationScore.score }}
            </div>
            <p class="lead">out of {{ participationScore.answersSummaries.length }} questions</p>
            
            <div class="row mt-4">
              <div class="col">
                <h5>Your Answers:</h5>
                <div class="d-flex flex-wrap justify-content-center gap-2">
                  <span 
                    v-for="(summary, index) in participationScore.answersSummaries"
                    :key="index"
                    :class="summary.wasCorrect ? 'badge bg-success' : 'badge bg-danger'"
                  >
                    Q{{ index + 1 }}: {{ summary.wasCorrect ? '✓' : '✗' }}
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <div class="card mb-4">
          <div class="card-header">
            <h3>Updated Leaderboard</h3>
          </div>
          <div class="card-body">
            <div v-if="updatedScores.length === 0" class="text-muted">
              No scores available
            </div>
            <div v-else>
              <div 
                v-for="(score, index) in updatedScores.slice(0, 10)"
                :key="score.date"
                class="d-flex justify-content-between align-items-center py-2"
                :class="{ 'bg-light': index % 2 === 0 }"
              >
                <div>
                  <strong>{{ index + 1 }}. {{ score.playerName }}</strong>
                  <small class="text-muted ms-2">{{ score.date }}</small>
                </div>
                <span class="badge bg-primary">{{ score.score }}</span>
              </div>
            </div>
          </div>
        </div>
        
        <router-link to="/" @click="goHome" class="btn btn-primary btn-lg">
          Back to Home
        </router-link>
      </div>
    </div>
  </div>
</template>