// Questions and answers
const questions = [
    {
        question: "What is the purpose of HTML?",
        answers: [
            "Structure of a webpage", 
            "Make webpages interactive", 
            "Create style rules", 
            "None of the above"
        ],
        correctAnswer: 1,
        image: "Top-10-Uses-of-HTML-in-the-Real-World.png" // Optional image URL
    },
    {
        question: "What does CSS stand for?",
        answers: [
            "Cascading Style Sheets", 
            "Computer Style Sheets", 
            "Creative Style Sheets", 
            "None of the above"
        ],
        correctAnswer: 1,
        image: "CSS-Stands-for-question.png" // Optional image URL
    },
    {
        question: "What is the main function of JavaScript?",
        answers: [
            "Structure of a webpage", 
            "Make webpages interactive", 
            "Create style rules", 
            "None of the above"
        ],
        correctAnswer: 2,
        image: "Javascript-functions.png" // Optional image URL
    },
    {
        question: "Which HTML tag is used to define an internal style sheet?",
        answers: [
            "<css>", 
            "<script>", 
            "<style>", 
            "<link>"
        ],
        correctAnswer: 3,
        image: "css-internal-stylesheet.png" // Optional image URL
    },
    {
        question: "Which property is used to change the background color in CSS?",
        answers: [
            "color", 
            "bgcolor", 
            "background-color", 
            "background"
        ],
        correctAnswer: 3,
        image: "css-background-color-example.png" // Optional image URL
    },
    {
        question: "What does DOM stand for?",
        answers: [
            "Document Object Model", 
            "Display Object Management", 
            "Digital Ordinance Model", 
            "Desktop Oriented Mode"
        ],
        correctAnswer: 1,
        image: "Document.jpg" // Optional image URL
    },
    {
        question: "Which HTML attribute is used to define inline styles?",
        answers: [
            "class", 
            "style", 
            "font", 
            "styles"
        ],
        correctAnswer: 2,
        image: "HTML-Inline-Styles.png" // Optional image URL
    },
    // New questions
    {
        question: "What is a MAC address used for in computer networks?",
        answers: [
            "Identifying devices on a network",
            "Encrypting data",
            "Routing packets",
            "None of the above"
        ],
        correctAnswer: 1,
        image: "mac-address.png" // Optional image URL
    },
    {
        question: "What does an IP address represent?",
        answers: [
            "A unique identifier for a device on a network",
            "A type of encryption",
            "A physical address",
            "None of the above"
        ],
        correctAnswer: 1,
        image: "ip-address.png" // Optional image URL
    },
    {
        question: "Which layer of the TCP/IP model is responsible for routing?",
        answers: [
            "Application layer",
            "Transport layer",
            "Internet layer",
            "Network Access layer"
        ],
        correctAnswer: 3,
        image: "tcp-ip-model.png" // Optional image URL
    },
    {
        question: "What does HTTP stand for?",
        answers: [
            "HyperText Transfer Protocol",
            "HyperText Transmission Protocol",
            "HyperText Transfer Process",
            "None of the above"
        ],
        correctAnswer: 1,
        image: "http-protocol.png" // Optional image URL
    },
    {
        question: "What is the primary function of DNS?",
        answers: [
            "Translating domain names to IP addresses",
            "Encrypting data",
            "Routing packets",
            "None of the above"
        ],
        correctAnswer: 1,
        image: "dns.png" // Optional image URL
    },
    {
        question: "Which network topology connects all devices to a central hub?",
        answers: [
            "Bus topology",
            "Star topology",
            "Ring topology",
            "Mesh topology"
        ],
        correctAnswer: 2,
        image: "network-topologies.png" // Optional image URL
    },
    {
        question: "How many layers are there in the OSI model?",
        answers: [
            "5",
            "6",
            "7",
            "8"
        ],
        correctAnswer: 3,
        image: "osi-model.png" // Optional image URL
    },
    {
        question: "What is the purpose of a firewall in a network?",
        answers: [
            "To block unauthorized access",
            "To encrypt data",
            "To route packets",
            "None of the above"
        ],
        correctAnswer: 1,
        image: "firewall.png" // Optional image URL
    },
    {
        question: "What is the purpose of a subnet mask in networking?",
        answers: [
            "To divide an IP address into network and host portions",
            "To encrypt data",
            "To route packets",
            "None of the above"
        ],
        correctAnswer: 1,
        image: "subnet-mask.png" // Optional image URL
    },
    {
        question: "Which protocol is used to send emails?",
        answers: [
            "HTTP",
            "SMTP",
            "FTP",
            "IMAP"
        ],
        correctAnswer: 2,
        image: "smtp.png" // Optional image URL
    },
    {
        question: "What does SSL stand for?",
        answers: [
            "Secure Sockets Layer",
            "Secure Software Layer",
            "System Sockets Layer",
            "None of the above"
        ],
        correctAnswer: 1,
        image: "ssl.png" // Optional image URL
    },
    {
        question: "What is the primary purpose of the ARP protocol?",
        answers: [
            "To map IP addresses to MAC addresses",
            "To encrypt data",
            "To route packets",
            "None of the above"
        ],
        correctAnswer: 1,
        image: "arp-protocol.png" // Optional image URL
    },
    {
        question: "Which protocol is used for secure communication over a computer network?",
        answers: [
            "HTTP",
            "FTP",
            "SSH",
            "SMTP"
        ],
        correctAnswer: 3,
        image: "ssh.png" // Optional image URL
    },
    {
        question: "What does DHCP stand for?",
        answers: [
            "Dynamic Host Configuration Protocol",
            "Dynamic Hypertext Configuration Protocol",
            "Dynamic Host Control Protocol",
            "None of the above"
        ],
        correctAnswer: 1,
        image: "dhcp.png" // Optional image URL
    },
    {
        question: "Which layer of the OSI model is responsible for error detection and correction?",
        answers: [
            "Physical layer",
            "Data Link layer",
            "Network layer",
            "Transport layer"
        ],
        correctAnswer: 2,
        image: "osi-data-link-layer.png" // Optional image URL
    },
    {
        question: "What is the purpose of a VPN?",
        answers: [
            "To create a secure connection over a public network",
            "To encrypt data",
            "To route packets",
            "None of the above"
        ],
        correctAnswer: 1,
        image: "vpn.png" // Optional image URL
    },
    {
        question: "Which protocol is used to retrieve emails from a mail server?",
        answers: [
            "HTTP",
            "SMTP",
            "POP3",
            "FTP"
        ],
        correctAnswer: 3,
        image: "smtp.png" // Optional image URL
    },
    {
        question: "What does NAT stand for in networking?",
        answers: [
            "Network Address Translation",
            "Network Access Translation",
            "Network Address Transmission",
            "None of the above"
        ],
        correctAnswer: 1,
        image: "nat.png" // Optional image URL
    }
];

let currentQuestionIndex = 0;
let isFlipped = false;

// Function to return the current question index
function getCurrentQuestionIndex() {
    return currentQuestionIndex;
}

// Function to return the total number of questions
function getTotalQuestions() {
    return questions.length;
}

// Function to set the element with id 'question-num' to display the current question number out of the total number of questions
function displayQuestionNumber() {
    const questionNumElement = document.getElementById("question-num");
    let questionString = "";
    if (getCurrentQuestionIndex() + 1 < 10) {
        questionNumElement.style.marginLeft = 20 + "px";
        document.getElementById("next-button").style.marginLeft = 7 + "%";
    } else {
        questionNumElement.style.marginLeft = 10 + "px";
        document.getElementById("next-button").style.marginLeft = 5 + "%";
    }
    questionString = "Q" + (getCurrentQuestionIndex() + 1) + "/" + getTotalQuestions();
    questionNumElement.innerHTML = questionString;
}

document.addEventListener("DOMContentLoaded", function() {
    // Display the current question number when the page loads
    displayQuestionNumber();
});

// Function to read out the question and answers with a specific voice
function readOutLoud(text) {
    const speech = new SpeechSynthesisUtterance(text);
    const voices = speechSynthesis.getVoices();
    const selectedVoice = voices.find(voice => voice.name === 'Google UK English Male') || voices[0];
    speech.voice = selectedVoice;
    speechSynthesis.speak(speech);
}

// Call this function whenever a question is displayed
function displayQuestion() {
    const questionData = questions[currentQuestionIndex];
    document.getElementById("question").innerText = questionData.question;

    const answerButtons = document.querySelectorAll('.answer-btn');
    answerButtons.forEach((button, index) => {
        button.innerText = questionData.answers[index];
        button.onclick = function(event) {
            event.stopPropagation(); // Prevent the flipCard function from being called
            checkAnswer(index + 1);
        };
    });

    // Set the question image if available
    const questionImage = document.getElementById("question-image");
    if (questionData.image) {
        questionImage.src = questionData.image;
        questionImage.style.display = "block";
    } else {
        questionImage.style.display = "none";
    }

    // Clear the result message
    document.getElementById("result").innerText = '';
}

// Function to check the answer
function checkAnswer(selectedAnswer) {
    const questionData = questions[currentQuestionIndex];
    const correctAnswer = questionData.correctAnswer;
    
    if (selectedAnswer === correctAnswer) {
        document.getElementById("result").innerText = "Correct!";
    } else {
        document.getElementById("result").innerText = "Incorrect. Try again!";
    }
}

// Move to next question
function nextQuestion() {
    if (currentQuestionIndex < questions.length - 1) {
        currentQuestionIndex++;
        isFlipped = false;
        document.querySelector('.flashcard').classList.remove('flipped');
        displayQuestionNumber();
        displayQuestion();
    } else {
        document.getElementById("result").innerText = "Flashcards Completed!";
        document.getElementById("next-button").disabled = true;
    }
    if (document.getElementById("prev-button").disabled == true) {
        document.getElementById("prev-button").disabled = false;
    }
}

// Move to previous question
function prevQuestion() {
    if (currentQuestionIndex > 0) {
        currentQuestionIndex--;
        isFlipped = false;
        document.querySelector('.flashcard').classList.remove('flipped');
        displayQuestionNumber();
        displayQuestion();
    } else {
        document.getElementById("result").innerText = "This is the first question!";
        document.getElementById("prev-button").disabled = true;
    }
    if (document.getElementById("next-button").disabled == true) {
        document.getElementById("next-button").disabled = false;
    }
}

// Function to flip the card
function flipCard() {
    const flashcard = document.querySelector('.flashcard');
    if (!isFlipped) {
        flashcard.classList.add('flipped');
        isFlipped = true;
    } else {
        flashcard.classList.remove('flipped');
        isFlipped = false;
    }
}

// Function to read aloud based on the current state
function readAloud() {
    const flashcard = document.querySelector('.flashcard');
    if (!isFlipped) {
        const questionText = document.getElementById("question").innerText;
        readOutLoud(questionText);
    } else {
        const resultText = document.getElementById("result").innerText;
        if (resultText) {
            readOutLoud(resultText);
        }
        const answerButtons = document.querySelectorAll('.answer-btn');
        answerButtons.forEach(button => {
            readOutLoud(button.innerText);
        });
    }
}

// Initialize quiz
displayQuestion();