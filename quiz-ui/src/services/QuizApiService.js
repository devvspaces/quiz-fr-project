import axios from "axios";

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL || 'http://localhost:5000'}`,
  json: true
});

export default {
  async call(method, resource, data = null, token = null) {
    var headers = {
      "Content-Type": "application/json",
    };
    if (token != null) {
      headers.authorization = "Bearer " + token;
    }

    return instance({
      method,
      headers: headers,
      url: resource,
      data,
    })
      .then((response) => {
        return { status: response.status, data: response.data };
      })
      .catch((error) => {
        console.error(error);
        throw error;
      });
  },
  
  getQuizInfo() {
    return this.call("get", "quiz-info");
  },
  
  getQuestion(position) {
    return this.call("get", `questions?position=${position}`);
  },
  
  submitParticipation(playerName, answers) {
    return this.call("post", "participations", { playerName, answers });
  },
  
  login(password) {
    return this.call("post", "login", { password });
  },
  
  createQuestion(question, token) {
    return this.call("post", "questions", question, token);
  },
  
  updateQuestion(questionId, question, token) {
    return this.call("put", `questions/${questionId}`, question, token);
  },
  
  deleteQuestion(questionId, token) {
    return this.call("delete", `questions/${questionId}`, null, token);
  },
  
  deleteAllQuestions(token) {
    return this.call("delete", "questions/all", null, token);
  },
  
  deleteAllParticipations(token) {
    return this.call("delete", "participations/all", null, token);
  },
  
  rebuildDb(token) {
    return this.call("post", "rebuild-db", null, token);
  }
};