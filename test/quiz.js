const quizData = [
    {
      frage: "Was ist 6*6?",
      optionen: ["36", "100", "456", "45678"],
      loesung: "36"
    },
    {
      frage: "Welche davon ist kein Farbe?",
      optionen: ["Gelb", "100", "Rot", "Blau"],
      loesung: "100"
    },
    // Add more questions here...
  ];
  
  const questionElement = document.getElementById("frage");
  const optionsElement = document.getElementById("optionen");
  const submitButton = document.getElementById("abgeben");
  
  let currentQuestion = 0;
  let score = 0;
  
  function showQuestion() {
    const frage = quizData[currentQuestion];
    questionElement.innerText = frage.frage;
  
    optionsElement.innerHTML = "";
    question.options.forEach(optionen => {
      const button = document.createElement("button");
      button.innerText = optionen;
      optionsElement.appendChild(button);
      button.addEventListener("click", selectAnswer);
    });
  }
  
  function selectAnswer(e) {
    const selectedButton = e.target;
    const loesung = quizData[currentQuestion].loesung;
  
    if (selectedButton.innerText === loesung) {
      score++;
    }
  
    currentQuestion++;
  
    if (currentQuestion < quizData.length) {
      showQuestion();
    } else {
      showResult();
    }
  }
  
  function showResult() {
    quiz.innerHTML = `
      <h1>Fertig!</h1>
      <p>Punkte: ${score}/${quizData.length}</p>
    `;
  }
  
  showQuestion();
