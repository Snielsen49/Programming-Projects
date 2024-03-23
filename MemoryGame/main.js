const gridcontainer = document.querySelector(".grid-container");
let cards = [];
let card1, card2;
let score = 0;
let freezeboard = false;

document.querySelector(".score").textContent = score;

//populates the cards array with two data values from the json file 
fetch("./Data/cards.json")
    .then((res) => res.json())
    .then((Pics) => {
        cards = [...Pics, ...Pics];// double pics so there are matches 
        mixcards();
        generatecards();
    });

    //mixes the cards using the fisher yates shuffle
function mixcards() {
    let current = cards.length, randomindex, tempval;
    while (current !== 0) {
        randomindex = Math.floor(Math.random() * current);
        current -= 1;
        tempval = cards[current];
        cards[current] = cards[randomindex];
        cards[randomindex] = tempval;
    }
}

function generatecards() {
    gridcontainer.innerHTML = ''; // Clear the grid container before generating cards

    //iterates through cards and generats the front and back 
    for (let card of cards) {
        const cardelm = document.createElement("div");
        cardelm.classList.add("card");
        //this sets the name of the card to the one in the json file to compair them
        cardelm.setAttribute("data-name", card.name);
        cardelm.innerHTML = `
        <div class="front">
            <img class="frontimg" src=${card.image} />
        </div>
        <div class="back"></div>
        `;
        gridcontainer.appendChild(cardelm);
        //sets buttons 
        cardelm.addEventListener("click", flipcard);
    }
}

//a card was fliped by user 
function flipcard(event) {
    //board is frozen so no move can be made 
    if (freezeboard) return;

    const clickedCard = event.currentTarget;

    //clicked card has already been clicked
    if (clickedCard === card1) return;

    clickedCard.classList.add("flipped");

    if (!card1) {
        card1 = clickedCard;
        return;
    }
    card2 = clickedCard;
    score++;
    document.querySelector(".score").textContent = score;
    freezeboard = true;

    checkmatch();
}

function checkmatch() {
    let match = card1.dataset.name === card2.dataset.name;
    //if its a match it will disable the card if not it will hide the cards
    match ? disable() : unflipcards();
}

//removes the buttons 
function disable() {
    card1.removeEventListener("click", flipcard);
    card2.removeEventListener("click", flipcard);
    resetboard();
}

//hides the cards 
function unflipcards() {
    //gives animations time
    setTimeout(() => {
        card1.classList.remove("flipped");
        card2.classList.remove("flipped");
        resetboard();
    }, 1000);
}

function resetboard() {
    [card1, card2] = [null, null];
    freezeboard = false;
}

function restart() {
    resetboard();
    mixcards();
    score = 0;
    document.querySelector(".score").textContent = score;
    generatecards();
}
