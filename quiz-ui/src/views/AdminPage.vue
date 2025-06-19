<script setup>
import { ref, onMounted } from 'vue';
import QuestionsList from '../components/QuestionsList.vue';
import QuestionEdition from '../components/QuestionEdition.vue';
import quizApiService from "@/services/QuizApiService";
import participationStorageService from "@/services/ParticipationStorageService";

const isLoggedIn = ref(false);
const password = ref('');
const adminMode = ref('list'); // 'list' or 'edit'
const editingQuestion = ref(null);
const questions = ref([]);

onMounted(() => {
  const token = participationStorageService.getAuthToken();
  if (token) {
    isLoggedIn.value = true;
    loadQuestions();
  }
});

async function login() {
  try {
    const response = await quizApiService.login(password.value);
    participationStorageService.saveAuthToken(response.data.token);
    isLoggedIn.value = true;
    adminMode.value = 'list';
    await loadQuestions();
  } catch (error) {
    alert('Invalid password');
  }
}

function logout() {
  participationStorageService.removeAuthToken();
  isLoggedIn.value = false;
  password.value = '';
}

async function loadQuestions() {
  try {
    const response = await quizApiService.getQuizInfo();
    // Load all questions by getting them one by one
    const questionPromises = [];
    for (let i = 1; i <= response.data.size; i++) {
      questionPromises.push(quizApiService.getQuestion(i));
    }
    const questionResponses = await Promise.all(questionPromises);
    questions.value = questionResponses.map(r => r.data).sort((a, b) => a.position - b.position);
  } catch (error) {
    console.error('Failed to load questions:', error);
  }
}

function editQuestion(question) {
  editingQuestion.value = question;
  adminMode.value = 'edit';
}

function createNewQuestion() {
  editingQuestion.value = null;
  adminMode.value = 'edit';
}

async function saveQuestion(questionData) {
  try {
    const token = participationStorageService.getAuthToken();
    
    if (editingQuestion.value) {
      await quizApiService.updateQuestion(editingQuestion.value.id, questionData, token);
    } else {
      await quizApiService.createQuestion(questionData, token);
    }
    
    adminMode.value = 'list';
    await loadQuestions();
  } catch (error) {
    console.error('Failed to save question:', error);
    alert('Failed to save question');
  }
}

async function deleteQuestion(questionId) {
  if (confirm('Are you sure you want to delete this question?')) {
    try {
      const token = participationStorageService.getAuthToken();
      await quizApiService.deleteQuestion(questionId, token);
      await loadQuestions();
    } catch (error) {
      console.error('Failed to delete question:', error);
      alert('Failed to delete question');
    }
  }
}

function cancelEdit() {
  adminMode.value = 'list';
}
</script>

<template>
  <div>
    <!-- Login Form -->
    <div v-if="!isLoggedIn" class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-header">
            <h2>Admin Login</h2>
          </div>
          <div class="card-body">
            <form @submit.prevent="login">
              <div class="mb-3">
                <label for="password" class="form-label">Password:</label>
                <input 
                  type="password" 
                  id="password"
                  v-model="password" 
                  class="form-control"
                  required
                />
              </div>
              <button type="submit" class="btn btn-primary">Login</button>
            </form>
          </div>
        </div>
      </div>
    </div>

    <!-- Admin Interface -->
    <div v-else>
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h1>Quiz Administration</h1>
        <button @click="logout" class="btn btn-outline-secondary">Logout</button>
      </div>

      <!-- Navigation -->
      <div class="mb-3">
        <button 
          @click="adminMode = 'list'" 
          :class="adminMode === 'list' ? 'btn btn-primary' : 'btn btn-outline-primary'"
          class="me-2"
        >
          Questions List
        </button>
        <button 
          @click="createNewQuestion" 
          class="btn btn-success"
        >
          Create New Question
        </button>
      </div>

      <!-- Questions List -->
      <QuestionsList 
        v-if="adminMode === 'list'"
        :questions="questions"
        @edit-question="editQuestion"
        @delete-question="deleteQuestion"
      />

      <!-- Question Edition -->
      <QuestionEdition 
        v-if="adminMode === 'edit'"
        :question="editingQuestion"
        :questions-count="questions.length"
        @save-question="saveQuestion"
        @cancel-edit="cancelEdit"
      />
    </div>
  </div>
</template>