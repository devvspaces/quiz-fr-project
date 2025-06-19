<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import QuestionDisplay from '../components/QuestionDisplay.vue';
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

const router = useRouter();
const currentQuestion = ref(null);
const currentQuestionPosition = ref(1);
const totalNumberOfQuestions = ref(0);
const answers = ref([]);

onMounted(async () => {
  try {
    const quizInfo = await quizApiService.getQuizInfo();
    totalNumberOfQuestions.value = quizInfo.data.size;
    
    if (totalNumberOfQuestions.value > 0) {
      await loadQuestionByPosition(1);
    }
  } catch (error) {
    console.error("Failed to initialize quiz:", error);
  }
});

async function loadQuestionByPosition(position) {
  try {
    const response = await quizApiService.getQuestion(position);
    currentQuestion.value = response.data;
    currentQuestionPosition.value = position;
  } catch (error) {
    console.error("Failed to load question:", error);
  }
}

async function answerSelectedHandler(answerId) {
  answers.value.push(answerId);
  
  if (currentQuestionPosition.value < totalNumberOfQuestions.value) {
    await loadQuestionByPosition(currentQuestionPosition.value + 1);
  } else {
    await endQuiz();
  }
}

async function endQuiz() {
  try {
    const playerName = participationStorageService.getPlayerName();
    const response = await quizApiService.submitParticipation(playerName, answers.value);
    
    participationStorageService.saveParticipationScore(response.data);
    router.push('/score');
  } catch (error) {
    console.error("Failed to submit quiz:", error);
  }
}
</script>

<template>
  <div>
    <div class="row mb-3">
      <div class="col">
        <div class="progress">
          <div 
            class="progress-bar" 
            role="progressbar" 
            :style="`width: ${(currentQuestionPosition / totalNumberOfQuestions) * 100}%`"
          ></div>
        </div>
        <small class="text-muted">
          Question {{ currentQuestionPosition }} / {{ totalNumberOfQuestions }}
        </small>
      </div>
    </div>
    
    <QuestionDisplay 
      :question="currentQuestion" 
      @answer-selected="answerSelectedHandler" 
    />
  </div>
</template>