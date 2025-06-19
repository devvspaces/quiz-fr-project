<script setup>
import { ref, onMounted, watch } from 'vue';
import ImageUpload from './ImageUpload.vue';

const props = defineProps({
  question: Object,
  questionsCount: Number
});

const emit = defineEmits(['save-question', 'cancel-edit']);

const questionData = ref({
  title: '',
  text: '',
  image: '',
  position: 1,
  possibleAnswers: [
    { text: '', isCorrect: false },
    { text: '', isCorrect: false },
    { text: '', isCorrect: false },
    { text: '', isCorrect: false }
  ]
});

onMounted(() => {
  if (props.question) {
    questionData.value = {
      title: props.question.title,
      text: props.question.text,
      image: props.question.image || '',
      position: props.question.position,
      possibleAnswers: [...props.question.possibleAnswers]
    };
  } else {
    questionData.value.position = props.questionsCount + 1;
  }
});

function setCorrectAnswer(index) {
  questionData.value.possibleAnswers.forEach((answer, i) => {
    answer.isCorrect = i === index;
  });
}

function saveQuestion() {
  // Validation
  if (!questionData.value.title.trim() || !questionData.value.text.trim()) {
    alert('Please fill in the title and question text.');
    return;
  }
  
  const hasAnswers = questionData.value.possibleAnswers.every(answer => answer.text.trim());
  if (!hasAnswers) {
    alert('Please fill in all answer options.');
    return;
  }
  
  const hasCorrectAnswer = questionData.value.possibleAnswers.some(answer => answer.isCorrect);
  if (!hasCorrectAnswer) {
    alert('Please select the correct answer.');
    return;
  }
  
  emit('save-question', questionData.value);
}

function cancelEdit() {
  emit('cancel-edit');
}

function onImageChange(imageData) {
  questionData.value.image = imageData;
}
</script>

<template>
  <div>
    <h2>{{ question ? 'Edit Question' : 'Create New Question' }}</h2>
    
    <form @submit.prevent="saveQuestion">
      <div class="row">
        <div class="col-md-8">
          <div class="mb-3">
            <label for="position" class="form-label">Position:</label>
            <input 
              type="number" 
              id="position"
              v-model.number="questionData.position" 
              class="form-control"
              min="1"
              required
            />
          </div>
          
          <div class="mb-3">
            <label for="title" class="form-label">Title:</label>
            <input 
              type="text" 
              id="title"
              v-model="questionData.title" 
              class="form-control"
              required
            />
          </div>
          
          <div class="mb-3">
            <label for="text" class="form-label">Question Text:</label>
            <textarea 
              id="text"
              v-model="questionData.text" 
              class="form-control"
              rows="3"
              required
            ></textarea>
          </div>
          
          <div class="mb-3">
            <label class="form-label">Image:</label>
            <ImageUpload 
              :file-data-url="questionData.image"
              @file-change="onImageChange"
            />
          </div>
        </div>
        
        <div class="col-md-4">
          <h5>Answers:</h5>
          <div v-for="(answer, index) in questionData.possibleAnswers" :key="index" class="mb-3">
            <div class="input-group">
              <input 
                type="text" 
                v-model="answer.text" 
                class="form-control"
                :placeholder="`Answer ${index + 1}`"
                required
              />
              <div class="input-group-text">
                <input 
                  type="radio" 
                  :name="'correct-answer'"
                  :checked="answer.isCorrect"
                  @change="setCorrectAnswer(index)"
                />
              </div>
            </div>
            <small class="text-muted">{{ answer.isCorrect ? 'Correct answer' : 'Incorrect answer' }}</small>
          </div>
        </div>
      </div>
      
      <div class="mt-4">
        <button type="submit" class="btn btn-success me-2">Save Question</button>
        <button type="button" @click="cancelEdit" class="btn btn-secondary">Cancel</button>
      </div>
    </form>
  </div>
</template>