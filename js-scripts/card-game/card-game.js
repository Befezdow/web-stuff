const cards = document.querySelectorAll('.memory-card');
let finishedPairsCount = 0;
let lastSelectedCard = null;

function flipCard() {
    this.classList.toggle('flip');

    if (lastSelectedCard !== null) {
    	let lastCardType = lastSelectedCard.getAttribute('data-framework');
    	let currentCardType = this.getAttribute('data-framework');

    	if (lastCardType === currentCardType) {
    		if (finishedPairsCount >= 5) {
    			setTimeout(() => {
    				alert('You win!');
    			}, 1000);
    		} else {
    			finishedPairsCount++;
    			lastSelectedCard.removeEventListener('click', flipCard);
    			this.removeEventListener('click', flipCard);
    			lastSelectedCard = null;
    		}
    	} else {
    		blockClicks();
    		setTimeout(() => {
    			this.classList.toggle('flip');
    			lastSelectedCard.classList.toggle('flip');
    			lastSelectedCard = null;
    			unblockClicks();
    		}, 1000);
    	}
    } else {
    	lastSelectedCard = this;
    }
}

function blockClicks() {
	document.addEventListener('click', clickBlocker, true);
}

function unblockClicks() {
	document.removeEventListener('click', clickBlocker, true);
}

function clickBlocker(e) {
	e.stopPropagation();
	e.preventDefault();
}

cards.forEach(card => card.addEventListener('click', flipCard));
cards.forEach(card => {
	let ramdomPos = Math.floor(Math.random() * 12);
    card.style.order = ramdomPos;
 });