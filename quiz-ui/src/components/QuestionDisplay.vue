<script setup>
const props = defineProps({
  question: Object
});

const emit = defineEmits(['answer-selected']);

function selectAnswer(answerId) {
  emit('answer-selected', answerId);
}
</script>

<template>
  <div v-if="question" class="question-display">
    <div class="card">
      <div class="card-header">
        <h3>{{ question.title }}</h3>
      </div>
      <div class="card-body">
        <div v-if="question.image" class="text-center mb-3">
          <img :src="question.image" class="img-fluid rounded" style="max-height: 300px;" />
        </div>
        
        <p class="lead">{{ question.text }}</p>
        
        <div class="d-grid gap-2">
          <button 
            v-for="answer in question.possibleAnswers"
            :key="answer.id"
            @click="selectAnswer(answer.id)"
            class="btn btn-outline-primary btn-lg text-start"
          >
            {{ answer.text }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.question-display .btn {
  transition: all 0.2s;
}

.question-display .btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}
</style>