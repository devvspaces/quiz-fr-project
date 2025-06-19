<script setup>
const props = defineProps({
  questions: Array
});

const emit = defineEmits(['edit-question', 'delete-question']);

function editQuestion(question) {
  emit('edit-question', question);
}

function deleteQuestion(questionId) {
  emit('delete-question', questionId);
}
</script>

<template>
  <div>
    <h2>Questions List</h2>
    
    <div v-if="questions.length === 0" class="text-muted">
      No questions available. Create your first question!
    </div>
    
    <div v-else>
      <div class="row">
        <div 
          v-for="question in questions"
          :key="question.id"
          class="col-md-6 mb-3"
        >
          <div class="card">
            <div class="card-header d-flex justify-content-between align-items-center">
              <span class="badge bg-secondary">Position {{ question.position }}</span>
              <div>
                <button 
                  @click="editQuestion(question)"
                  class="btn btn-sm btn-outline-primary me-2"
                >
                  Edit
                </button>
                <button 
                  @click="deleteQuestion(question.id)"
                  class="btn btn-sm btn-outline-danger"
                >
                  Delete
                </button>
              </div>
            </div>
            <div class="card-body">
              <h5 class="card-title">{{ question.title }}</h5>
              <p class="card-text">{{ question.text }}</p>
              
              <div v-if="question.image" class="mb-2">
                <img :src="question.image" class="img-thumbnail" style="max-height: 100px;" />
              </div>
              
              <div>
                <h6>Answers:</h6>
                <ul class="list-unstyled">
                  <li 
                    v-for="answer in question.possibleAnswers"
                    :key="answer.id"
                    :class="answer.isCorrect ? 'text-success fw-bold' : ''"
                  >
                    {{ answer.isCorrect ? '✓' : '○' }} {{ answer.text }}
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>