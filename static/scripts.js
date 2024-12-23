function flipCoin(choice) {
    const coin = document.getElementById("coin");
    const outcome = document.getElementById("outcome");
    const wins = document.getElementById("wins");
    const losses = document.getElementById("losses");
    const encryptedUserChoice = document.getElementById("encryptedUserChoice");
    const encryptedCoinFlip = document.getElementById("encryptedCoinFlip");
    const encryptedResult = document.getElementById("encryptedResult");

    // Start the flip animation
    coin.style.animation = "flip 1s infinite";

    // Send the choice to the backend
    setTimeout(() => {
        fetch("/flip_coin", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: `choice=${choice}`
        })
        .then(res => res.json())
        .then(data => {
            // Stop the flip animation
            coin.style.animation = "none";

            // Display coin flip result
            coin.textContent = data.coinFlip === 0 ? "Head" : "Tail";

            // Display outcome
            outcome.textContent = `You ${data.outcome}!`;

            // Update wins and losses
            wins.textContent = data.wins;
            losses.textContent = data.losses;

            // Display encrypted data
            encryptedUserChoice.textContent = data.encryptedUserChoice;
            encryptedCoinFlip.textContent = data.encryptedCoinFlip;
            encryptedResult.textContent = data.encryptedResult;
        })
        .catch(err => console.error(err));
    }, 1000);
}
